from rest_framework import generics, viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg, Sum, Q, Min, Max
from django.http import HttpResponse
from django.core.cache import cache
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import csv
import json
import io
import math
from datetime import datetime, timedelta

from core.models import (
    Expedition, SamplingLocation, EnvironmentalData, Sample,
    SequencingRun, TaxonomicAssignment, BiodiversityMetrics, AnalysisPipeline
)
from .serializers import (
    ExpeditionSerializer, SamplingLocationSerializer, EnvironmentalDataSerializer,
    SampleSerializer, SequencingRunSerializer, TaxonomicAssignmentSerializer,
    BiodiversityMetricsSerializer, AnalysisPipelineSerializer,
    TaxonomicSummarySerializer, LocationDiversitySerializer,
    SpeciesSearchResultSerializer, ExportDataSerializer, FileUploadSerializer
)


class ExpeditionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing expeditions"""
    queryset = Expedition.objects.all()
    serializer_class = ExpeditionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'vessel_name']
    ordering_fields = ['start_date', 'name']
    ordering = ['-start_date']

    @action(detail=True, methods=['get'])
    def locations(self, request, pk=None):
        """Get all sampling locations for an expedition"""
        expedition = self.get_object()
        locations = expedition.locations.all()
        serializer = SamplingLocationSerializer(locations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get expedition summary statistics"""
        expedition = self.get_object()
        cache_key = f"expedition_summary_{pk}"
        
        # Try to get from cache first
        summary = cache.get(cache_key)
        if summary is None:
            locations = expedition.locations.all()
            samples = Sample.objects.filter(location__expedition=expedition)
            
            summary = {
                'expedition_id': str(expedition.id),
                'name': expedition.name,
                'total_locations': locations.count(),
                'total_samples': samples.count(),
                'depth_range': {
                    'min_depth': locations.aggregate(min_depth=Min('depth_meters'))['min_depth'],
                    'max_depth': locations.aggregate(max_depth=Max('depth_meters'))['max_depth'],
                },
                'habitat_distribution': dict(
                    locations.values('habitat_type').annotate(count=Count('id')).values_list('habitat_type', 'count')
                ),
                'sample_types': dict(
                    samples.values('sample_type').annotate(count=Count('id')).values_list('sample_type', 'count')
                ),
                'temporal_coverage': {
                    'start_date': expedition.start_date,
                    'end_date': expedition.end_date,
                }
            }
            # Cache for 1 hour
            cache.set(cache_key, summary, 3600)
        
        return Response(summary)


class SamplingLocationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing sampling locations with geographic capabilities"""
    queryset = SamplingLocation.objects.all()
    serializer_class = SamplingLocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description', 'habitat_type']

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Find locations near a given point using bounding box"""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius_km = float(request.query_params.get('radius', 10))
        
        if not lat or not lng:
            return Response(
                {'error': 'lat and lng parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Simple bounding box calculation (approximate)
        lat_f = float(lat)
        lng_f = float(lng)
        
        # Rough approximation: 1 degree ≈ 111 km
        lat_delta = radius_km / 111.0
        lng_delta = radius_km / (111.0 * abs(math.cos(math.radians(lat_f))))
        
        nearby_locations = SamplingLocation.objects.filter(
            latitude__gte=lat_f - lat_delta,
            latitude__lte=lat_f + lat_delta,
            longitude__gte=lng_f - lng_delta,
            longitude__lte=lng_f + lng_delta
        )
        
        serializer = self.get_serializer(nearby_locations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def diversity_hotspots(self, request):
        """Get locations with high biodiversity"""
        locations = SamplingLocation.objects.annotate(
            avg_shannon=Avg('samples__biodiversity_metrics__shannon_diversity'),
            total_species=Count('samples__taxonomic_assignments__species', distinct=True),
            novel_taxa=Count('samples__taxonomic_assignments', filter=Q(samples__taxonomic_assignments__is_novel_taxon=True))
        ).filter(
            avg_shannon__isnull=False
        ).order_by('-avg_shannon', '-total_species')

        diversity_data = []
        for location in locations:
            diversity_data.append({
                'location_id': location.id,
                'location_name': location.name,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'depth_meters': location.depth_meters,
                'shannon_diversity': location.avg_shannon,
                'species_richness': location.total_species,
                'novel_taxa_count': location.novel_taxa,
                'sample_count': location.samples.count()
            })

        serializer = LocationDiversitySerializer(diversity_data, many=True)
        return Response(serializer.data)


class SampleViewSet(viewsets.ModelViewSet):
    """ViewSet for managing eDNA samples"""
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['sample_id', 'notes', 'location__name']
    ordering_fields = ['collection_datetime', 'sample_id']
    ordering = ['-collection_datetime']

    @action(detail=True, methods=['get'])
    def taxonomy(self, request, pk=None):
        """Get taxonomic composition for a sample"""
        sample = self.get_object()
        assignments = sample.taxonomic_assignments.all()
        
        # Group by phylum
        phylum_summary = assignments.values('phylum').annotate(
            species_count=Count('species', distinct=True),
            read_count=Sum('read_count'),
            avg_confidence=Avg('confidence_score')
        ).order_by('-read_count')

        summary_data = []
        total_reads = assignments.aggregate(total=Sum('read_count'))['total'] or 1
        
        for item in phylum_summary:
            summary_data.append({
                'phylum': item['phylum'] or 'Unknown',
                'species_count': item['species_count'],
                'read_count': item['read_count'],
                'relative_abundance': item['read_count'] / total_reads,
                'confidence_level': 'high' if item['avg_confidence'] > 0.8 else 'medium' if item['avg_confidence'] > 0.5 else 'low'
            })

        serializer = TaxonomicSummarySerializer(summary_data, many=True)
        return Response(serializer.data)


class TaxonomicAssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet for taxonomic assignments with advanced filtering"""
    queryset = TaxonomicAssignment.objects.all()
    serializer_class = TaxonomicAssignmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['species', 'genus', 'family', 'phylum', 'sequence_id']
    ordering_fields = ['confidence_score', 'read_count', 'created_at']
    ordering = ['-confidence_score', '-read_count']

    @action(detail=False, methods=['get'])
    def species_search(self, request):
        """Advanced species search with aggregated data"""
        search_term = request.query_params.get('q', '').strip()
        taxonomic_level = request.query_params.get('level', 'species')
        confidence_threshold = float(request.query_params.get('confidence', 0.5))
        
        if not search_term:
            return Response({'error': 'Search query (q) is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Build search query based on taxonomic level
        search_field = f"{taxonomic_level}__icontains"
        assignments = TaxonomicAssignment.objects.filter(
            Q(**{search_field: search_term}) & Q(confidence_score__gte=confidence_threshold)
        )
        
        # Aggregate results
        species_data = assignments.values(
            'species', 'genus', 'family', 'phylum'
        ).annotate(
            sample_count=Count('sample', distinct=True),
            total_reads=Sum('read_count'),
            avg_confidence=Avg('confidence_score'),
            is_novel=Max('is_novel_taxon')
        ).order_by('-total_reads')

        # Get locations for each species
        results = []
        for item in species_data:
            species_assignments = assignments.filter(species=item['species'])
            locations = list(
                species_assignments.values_list('sample__location__name', flat=True).distinct()
            )
            
            results.append({
                'species': item['species'] or 'Unknown',
                'genus': item['genus'] or 'Unknown',
                'family': item['family'] or 'Unknown',
                'phylum': item['phylum'] or 'Unknown',
                'sample_count': item['sample_count'],
                'total_reads': item['total_reads'],
                'confidence_score': round(item['avg_confidence'], 3),
                'locations': locations,
                'is_novel': bool(item['is_novel'])
            })

        serializer = SpeciesSearchResultSerializer(results, many=True)
        return Response(serializer.data)


class DataExportView(generics.GenericAPIView):
    """Handle data export in various formats"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Export data based on filters and format"""
        serializer = ExportDataSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        export_format = serializer.validated_data['format']
        filters = serializer.validated_data
        
        # Build queryset based on filters
        queryset = TaxonomicAssignment.objects.all()
        
        if filters.get('date_range_start'):
            queryset = queryset.filter(created_at__gte=filters['date_range_start'])
        if filters.get('date_range_end'):
            queryset = queryset.filter(created_at__lte=filters['date_range_end'])
        if filters.get('confidence_threshold'):
            queryset = queryset.filter(confidence_score__gte=filters['confidence_threshold'])
        
        if export_format == 'csv':
            return self._export_csv(queryset, filters)
        elif export_format == 'json':
            return self._export_json(queryset, filters)
    
    def _export_csv(self, queryset, filters):
        """Export data as CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="edna_taxonomy_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Sample ID', 'Sequence ID', 'Kingdom', 'Phylum', 'Class', 'Order',
            'Family', 'Genus', 'Species', 'Confidence Score', 'Read Count',
            'Database Source', 'Is Novel', 'Collection Date'
        ])
        
        for assignment in queryset.select_related('sample'):
            writer.writerow([
                assignment.sample.sample_id,
                assignment.sequence_id,
                assignment.kingdom,
                assignment.phylum,
                assignment.class_name,
                assignment.order,
                assignment.family,
                assignment.genus,
                assignment.species,
                assignment.confidence_score,
                assignment.read_count,
                assignment.database_source,
                assignment.is_novel_taxon,
                assignment.sample.collection_datetime.strftime('%Y-%m-%d')
            ])
        
        return response
    
    def _export_json(self, queryset, filters):
        """Export data as JSON"""
        serializer = TaxonomicAssignmentSerializer(queryset, many=True)
        
        export_data = {
            'export_metadata': {
                'generated_at': datetime.now().isoformat(),
                'record_count': queryset.count(),
                'filters_applied': filters
            },
            'data': serializer.data
        }
        
        response = HttpResponse(
            json.dumps(export_data, indent=2),
            content_type='application/json'
        )
        response['Content-Disposition'] = 'attachment; filename="edna_taxonomy_export.json"'
        return response


# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Create a new user account"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    
    if not username or not email or not password:
        return Response(
            {'error': 'Username, email, and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'token': token.key
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to create user: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user and return token"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    from django.contrib.auth import authenticate
    user = authenticate(username=username, password=password)
    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'token': token.key
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout user by deleting token"""
    try:
        request.user.auth_token.delete()
        return Response(
            {'message': 'Logged out successfully'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': f'Logout failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
