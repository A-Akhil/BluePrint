import django_filters
from django.db.models import Q
from core.models import (
    Sample, TaxonomicAssignment, SamplingLocation, Expedition
)


class SampleFilter(django_filters.FilterSet):
    """Filter for Sample model with advanced options"""
    expedition = django_filters.ModelChoiceFilter(
        queryset=Expedition.objects.all(),
        field_name='location__expedition'
    )
    location_name = django_filters.CharFilter(
        field_name='location__name',
        lookup_expr='icontains'
    )
    habitat_type = django_filters.ChoiceFilter(
        field_name='location__habitat_type',
        choices=SamplingLocation.HABITAT_CHOICES
    )
    collection_date_from = django_filters.DateTimeFilter(
        field_name='collection_datetime',
        lookup_expr='gte'
    )
    collection_date_to = django_filters.DateTimeFilter(
        field_name='collection_datetime',
        lookup_expr='lte'
    )
    depth_min = django_filters.NumberFilter(
        field_name='location__depth_meters',
        lookup_expr='gte'
    )
    depth_max = django_filters.NumberFilter(
        field_name='location__depth_meters',
        lookup_expr='lte'
    )
    sample_type = django_filters.ChoiceFilter(
        choices=Sample.SAMPLE_TYPE_CHOICES
    )
    extraction_method = django_filters.ChoiceFilter(
        choices=Sample.EXTRACTION_METHOD_CHOICES
    )
    has_taxonomy = django_filters.BooleanFilter(
        field_name='taxonomic_assignments',
        lookup_expr='isnull',
        exclude=True
    )

    class Meta:
        model = Sample
        fields = [
            'expedition', 'location_name', 'habitat_type', 
            'collection_date_from', 'collection_date_to',
            'depth_min', 'depth_max', 'sample_type', 
            'extraction_method', 'has_taxonomy'
        ]


class TaxonomicAssignmentFilter(django_filters.FilterSet):
    """Filter for TaxonomicAssignment model with taxonomic hierarchy"""
    sample_id = django_filters.CharFilter(
        field_name='sample__sample_id',
        lookup_expr='icontains'
    )
    expedition = django_filters.ModelChoiceFilter(
        queryset=Expedition.objects.all(),
        field_name='sample__location__expedition'
    )
    location = django_filters.ModelChoiceFilter(
        queryset=SamplingLocation.objects.all(),
        field_name='sample__location'
    )
    kingdom = django_filters.CharFilter(lookup_expr='icontains')
    phylum = django_filters.CharFilter(lookup_expr='icontains')
    class_name = django_filters.CharFilter(lookup_expr='icontains')
    order = django_filters.CharFilter(lookup_expr='icontains')
    family = django_filters.CharFilter(lookup_expr='icontains')
    genus = django_filters.CharFilter(lookup_expr='icontains')
    species = django_filters.CharFilter(lookup_expr='icontains')
    
    database_source = django_filters.ChoiceFilter(
        choices=TaxonomicAssignment.DATABASE_CHOICES
    )
    confidence_level = django_filters.ChoiceFilter(
        choices=TaxonomicAssignment.CONFIDENCE_LEVELS
    )
    confidence_min = django_filters.NumberFilter(
        field_name='confidence_score',
        lookup_expr='gte'
    )
    confidence_max = django_filters.NumberFilter(
        field_name='confidence_score',
        lookup_expr='lte'
    )
    is_novel_taxon = django_filters.BooleanFilter()
    
    read_count_min = django_filters.NumberFilter(
        field_name='read_count',
        lookup_expr='gte'
    )
    read_count_max = django_filters.NumberFilter(
        field_name='read_count',
        lookup_expr='lte'
    )
    
    # Date range filters
    assigned_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    assigned_before = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte'
    )
    
    # Geographic filters
    latitude_min = django_filters.NumberFilter(
        method='filter_latitude_min'
    )
    latitude_max = django_filters.NumberFilter(
        method='filter_latitude_max'
    )
    longitude_min = django_filters.NumberFilter(
        method='filter_longitude_min'
    )
    longitude_max = django_filters.NumberFilter(
        method='filter_longitude_max'
    )
    
    # Environmental filters
    depth_min = django_filters.NumberFilter(
        field_name='sample__location__depth_meters',
        lookup_expr='gte'
    )
    depth_max = django_filters.NumberFilter(
        field_name='sample__location__depth_meters',
        lookup_expr='lte'
    )
    habitat_type = django_filters.ChoiceFilter(
        field_name='sample__location__habitat_type',
        choices=SamplingLocation.HABITAT_CHOICES
    )
    
    # Common vs rare species filter
    common_taxa = django_filters.BooleanFilter(
        method='filter_common_taxa'
    )
    rare_taxa = django_filters.BooleanFilter(
        method='filter_rare_taxa'
    )

    class Meta:
        model = TaxonomicAssignment
        fields = [
            'sample_id', 'expedition', 'location', 'kingdom', 'phylum',
            'class_name', 'order', 'family', 'genus', 'species',
            'database_source', 'confidence_level', 'confidence_min', 'confidence_max',
            'is_novel_taxon', 'read_count_min', 'read_count_max',
            'assigned_after', 'assigned_before', 'latitude_min', 'latitude_max',
            'longitude_min', 'longitude_max', 'depth_min', 'depth_max',
            'habitat_type', 'common_taxa', 'rare_taxa'
        ]

    def filter_latitude_min(self, queryset, name, value):
        return queryset.filter(sample__location__location__y__gte=value)

    def filter_latitude_max(self, queryset, name, value):
        return queryset.filter(sample__location__location__y__lte=value)

    def filter_longitude_min(self, queryset, name, value):
        return queryset.filter(sample__location__location__x__gte=value)

    def filter_longitude_max(self, queryset, name, value):
        return queryset.filter(sample__location__location__x__lte=value)

    def filter_common_taxa(self, queryset, name, value):
        """Filter for common taxa (appear in >10% of samples)"""
        if value:
            total_samples = Sample.objects.count()
            threshold = total_samples * 0.1
            
            common_species = TaxonomicAssignment.objects.values('species').annotate(
                sample_count=django_filters.Count('sample', distinct=True)
            ).filter(sample_count__gte=threshold).values_list('species', flat=True)
            
            return queryset.filter(species__in=common_species)
        return queryset

    def filter_rare_taxa(self, queryset, name, value):
        """Filter for rare taxa (appear in <5% of samples)"""
        if value:
            total_samples = Sample.objects.count()
            threshold = total_samples * 0.05
            
            rare_species = TaxonomicAssignment.objects.values('species').annotate(
                sample_count=django_filters.Count('sample', distinct=True)
            ).filter(sample_count__lte=threshold).values_list('species', flat=True)
            
            return queryset.filter(species__in=rare_species)
        return queryset


class LocationFilter(django_filters.FilterSet):
    """Filter for SamplingLocation model"""
    expedition = django_filters.ModelChoiceFilter(
        queryset=Expedition.objects.all()
    )
    habitat_type = django_filters.ChoiceFilter(
        choices=SamplingLocation.HABITAT_CHOICES
    )
    depth_min = django_filters.NumberFilter(
        field_name='depth_meters',
        lookup_expr='gte'
    )
    depth_max = django_filters.NumberFilter(
        field_name='depth_meters',
        lookup_expr='lte'
    )
    
    # Bounding box filter
    bbox = django_filters.CharFilter(method='filter_bbox')
    
    # Has samples filter
    has_samples = django_filters.BooleanFilter(
        field_name='samples',
        lookup_expr='isnull',
        exclude=True
    )
    
    # Biodiversity filters
    high_diversity = django_filters.BooleanFilter(
        method='filter_high_diversity'
    )

    class Meta:
        model = SamplingLocation
        fields = [
            'expedition', 'habitat_type', 'depth_min', 'depth_max',
            'bbox', 'has_samples', 'high_diversity'
        ]

    def filter_bbox(self, queryset, name, value):
        """Filter locations within a bounding box"""
        try:
            # Expected format: "lng_min,lat_min,lng_max,lat_max"
            coords = [float(x) for x in value.split(',')]
            if len(coords) != 4:
                return queryset
            
            lng_min, lat_min, lng_max, lat_max = coords
            
            return queryset.filter(
                location__x__gte=lng_min,
                location__x__lte=lng_max,
                location__y__gte=lat_min,
                location__y__lte=lat_max
            )
        except (ValueError, AttributeError):
            return queryset

    def filter_high_diversity(self, queryset, name, value):
        """Filter locations with above-average Shannon diversity"""
        if value:
            from django.db.models import Avg
            avg_diversity = queryset.aggregate(
                avg_shannon=Avg('samples__biodiversity_metrics__shannon_diversity')
            )['avg_shannon']
            
            if avg_diversity:
                return queryset.filter(
                    samples__biodiversity_metrics__shannon_diversity__gte=avg_diversity
                )
        return queryset


class ExpeditionFilter(django_filters.FilterSet):
    """Filter for Expedition model"""
    year = django_filters.NumberFilter(
        field_name='start_date__year'
    )
    start_date_from = django_filters.DateFilter(
        field_name='start_date',
        lookup_expr='gte'
    )
    start_date_to = django_filters.DateFilter(
        field_name='start_date',
        lookup_expr='lte'
    )
    vessel_name = django_filters.CharFilter(
        lookup_expr='icontains'
    )
    principal_investigator = django_filters.ModelChoiceFilter(
        queryset=django_filters.User.objects.all()
    )
    has_locations = django_filters.BooleanFilter(
        field_name='locations',
        lookup_expr='isnull',
        exclude=True
    )
    has_samples = django_filters.BooleanFilter(
        method='filter_has_samples'
    )

    class Meta:
        model = Expedition
        fields = [
            'year', 'start_date_from', 'start_date_to', 'vessel_name',
            'principal_investigator', 'has_locations', 'has_samples'
        ]

    def filter_has_samples(self, queryset, name, value):
        """Filter expeditions that have collected samples"""
        if value:
            return queryset.filter(locations__samples__isnull=False).distinct()
        return queryset
