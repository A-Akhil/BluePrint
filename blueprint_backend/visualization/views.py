from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum, Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import folium
from folium.plugins import HeatMap
import base64
import io
from datetime import datetime

from core.models import (
    SamplingLocation, TaxonomicAssignment, BiodiversityMetrics, Sample
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def species_diversity_map(request):
    """Generate interactive map with species diversity hotspots"""
    # Get locations with biodiversity data
    locations = SamplingLocation.objects.annotate(
        shannon_diversity=Avg('samples__biodiversity_metrics__shannon_diversity'),
        species_count=Count('samples__taxonomic_assignments__species', distinct=True),
        novel_taxa_count=Count('samples__taxonomic_assignments', 
                              filter=Q(samples__taxonomic_assignments__is_novel_taxon=True))
    ).filter(shannon_diversity__isnull=False)

    # Create base map
    if locations.exists():
        center_lat = locations.aggregate(avg_lat=Avg('location__y'))['avg_lat']
        center_lng = locations.aggregate(avg_lng=Avg('location__x'))['avg_lng']
    else:
        center_lat, center_lng = 0, 0

    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=6,
        tiles='OpenStreetMap'
    )

    # Add diversity hotspot markers
    heat_data = []
    for location in locations:
        lat, lng = location.latitude, location.longitude
        diversity_score = location.shannon_diversity or 0
        
        # Create popup content
        popup_content = f"""
        <div style="width: 200px;">
            <h4>{location.name}</h4>
            <p><strong>Depth:</strong> {location.depth_meters}m</p>
            <p><strong>Habitat:</strong> {location.get_habitat_type_display()}</p>
            <p><strong>Shannon Diversity:</strong> {diversity_score:.2f}</p>
            <p><strong>Species Count:</strong> {location.species_count}</p>
            <p><strong>Novel Taxa:</strong> {location.novel_taxa_count}</p>
        </div>
        """
        
        # Color code by diversity level
        if diversity_score > 3.0:
            color = 'red'  # High diversity
        elif diversity_score > 2.0:
            color = 'orange'  # Medium diversity
        else:
            color = 'green'  # Lower diversity
        
        folium.CircleMarker(
            location=[lat, lng],
            radius=8 + (diversity_score * 2),  # Size based on diversity
            popup=folium.Popup(popup_content, max_width=250),
            color=color,
            fill=True,
            fillOpacity=0.7,
            weight=2
        ).add_to(m)
        
        # Add to heat map data
        heat_data.append([lat, lng, diversity_score])

    # Add heat map layer
    if heat_data:
        HeatMap(heat_data, radius=15, blur=10, max_zoom=18).add_to(m)

    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 150px; height: 90px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <h4>Diversity Level</h4>
    <p><i class="fa fa-circle" style="color:red"></i> High (>3.0)</p>
    <p><i class="fa fa-circle" style="color:orange"></i> Medium (2.0-3.0)</p>
    <p><i class="fa fa-circle" style="color:green"></i> Lower (<2.0)</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Return map as HTML
    map_html = m._repr_html_()
    
    return Response({
        'map_html': map_html,
        'total_locations': locations.count(),
        'avg_diversity': locations.aggregate(avg=Avg('shannon_diversity'))['avg']
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taxonomic_composition_chart(request):
    """Generate taxonomic composition charts"""
    sample_id = request.GET.get('sample_id')
    expedition_id = request.GET.get('expedition_id')
    
    if sample_id:
        # Single sample composition
        assignments = TaxonomicAssignment.objects.filter(sample__id=sample_id)
        title = f"Taxonomic Composition - Sample {assignments.first().sample.sample_id if assignments else 'Unknown'}"
    elif expedition_id:
        # Expedition-wide composition
        assignments = TaxonomicAssignment.objects.filter(
            sample__location__expedition__id=expedition_id
        )
        title = "Taxonomic Composition - Expedition"
    else:
        # Overall composition
        assignments = TaxonomicAssignment.objects.all()
        title = "Overall Taxonomic Composition"

    # Group by phylum and calculate metrics
    phylum_data = assignments.values('phylum').annotate(
        species_count=Count('species', distinct=True),
        read_count=Sum('read_count'),
        avg_confidence=Avg('confidence_score')
    ).order_by('-read_count')

    # Prepare data for visualization
    phylums = []
    read_counts = []
    species_counts = []
    confidences = []
    
    for item in phylum_data:
        phylum_name = item['phylum'] or 'Unknown'
        phylums.append(phylum_name)
        read_counts.append(item['read_count'])
        species_counts.append(item['species_count'])
        confidences.append(item['avg_confidence'])

    # Create pie chart for read count distribution
    pie_fig = go.Figure(data=[go.Pie(
        labels=phylums,
        values=read_counts,
        hole=0.3,
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Reads: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    pie_fig.update_layout(
        title=f"{title} - Read Distribution",
        font=dict(size=12),
        height=500
    )

    # Create bar chart for species richness
    bar_fig = go.Figure(data=[go.Bar(
        x=phylums,
        y=species_counts,
        text=species_counts,
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Species Count: %{y}<br>Avg Confidence: %{customdata:.2f}<extra></extra>',
        customdata=confidences,
        marker_color='lightblue'
    )])
    
    bar_fig.update_layout(
        title=f"{title} - Species Richness",
        xaxis_title="Phylum",
        yaxis_title="Number of Species",
        height=500,
        xaxis_tickangle=-45
    )

    # Convert to JSON for frontend
    pie_json = pie_fig.to_json()
    bar_json = bar_fig.to_json()

    return Response({
        'pie_chart': json.loads(pie_json),
        'bar_chart': json.loads(bar_json),
        'summary': {
            'total_phylums': len(phylums),
            'total_species': sum(species_counts),
            'total_reads': sum(read_counts),
            'avg_confidence': sum(confidences) / len(confidences) if confidences else 0
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def confidence_distribution(request):
    """Generate confidence score distribution visualization"""
    expedition_id = request.GET.get('expedition_id')
    
    queryset = TaxonomicAssignment.objects.all()
    if expedition_id:
        queryset = queryset.filter(sample__location__expedition__id=expedition_id)

    # Create confidence bins
    confidence_bins = {
        'High (≥90%)': queryset.filter(confidence_score__gte=0.9).count(),
        'Medium-High (70-89%)': queryset.filter(confidence_score__gte=0.7, confidence_score__lt=0.9).count(),
        'Medium (50-69%)': queryset.filter(confidence_score__gte=0.5, confidence_score__lt=0.7).count(),
        'Low (<50%)': queryset.filter(confidence_score__lt=0.5).count(),
    }

    # Create histogram
    fig = go.Figure(data=[go.Bar(
        x=list(confidence_bins.keys()),
        y=list(confidence_bins.values()),
        text=list(confidence_bins.values()),
        textposition='auto',
        marker_color=['green', 'lightgreen', 'orange', 'red']
    )])

    fig.update_layout(
        title="Confidence Score Distribution",
        xaxis_title="Confidence Level",
        yaxis_title="Number of Assignments",
        height=400
    )

    # Add annotations
    total_assignments = sum(confidence_bins.values())
    fig.add_annotation(
        text=f"Total Assignments: {total_assignments}",
        xref="paper", yref="paper",
        x=1, y=1, xanchor='right', yanchor='bottom',
        showarrow=False
    )

    return Response({
        'chart': json.loads(fig.to_json()),
        'statistics': {
            'total_assignments': total_assignments,
            'high_confidence_percentage': (confidence_bins['High (≥90%)'] / total_assignments * 100) if total_assignments > 0 else 0,
            'distribution': confidence_bins
        }
    })
