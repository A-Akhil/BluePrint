from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import (
    Expedition, SamplingLocation, EnvironmentalData, Sample,
    SequencingRun, TaxonomicAssignment, BiodiversityMetrics, AnalysisPipeline
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ExpeditionSerializer(serializers.ModelSerializer):
    principal_investigator = UserSerializer(read_only=True)
    locations_count = serializers.SerializerMethodField()
    samples_count = serializers.SerializerMethodField()

    class Meta:
        model = Expedition
        fields = [
            'id', 'name', 'description', 'start_date', 'end_date',
            'vessel_name', 'principal_investigator', 'locations_count',
            'samples_count', 'created_at', 'updated_at'
        ]

    def get_locations_count(self, obj):
        return obj.locations.count()

    def get_samples_count(self, obj):
        return Sample.objects.filter(location__expedition=obj).count()


class EnvironmentalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalData
        fields = [
            'id', 'measurement_datetime', 'temperature_celsius', 'salinity_psu',
            'ph', 'dissolved_oxygen_mg_l', 'pressure_dbar', 'turbidity_ntu',
            'chlorophyll_a_mg_m3', 'nitrate_umol_l', 'phosphate_umol_l',
            'silicate_umol_l', 'created_at'
        ]


class SamplingLocationSerializer(serializers.ModelSerializer):
    expedition = ExpeditionSerializer(read_only=True)
    environmental_data = EnvironmentalDataSerializer(many=True, read_only=True)
    samples_count = serializers.SerializerMethodField()

    class Meta:
        model = SamplingLocation
        fields = [
            'id', 'name', 'latitude', 'longitude', 'depth_meters',
            'habitat_type', 'expedition', 'description', 'environmental_data',
            'samples_count', 'created_at'
        ]

    def get_samples_count(self, obj):
        return obj.samples.count()


class SamplingLocationBasicSerializer(serializers.ModelSerializer):
    """Simplified serializer for nested relationships"""

    class Meta:
        model = SamplingLocation
        fields = [
            'id', 'name', 'latitude', 'longitude', 'depth_meters',
            'habitat_type', 'description'
        ]


class SequencingRunSerializer(serializers.ModelSerializer):
    samples_count = serializers.SerializerMethodField()

    class Meta:
        model = SequencingRun
        fields = [
            'id', 'run_id', 'platform', 'run_date', 'total_reads',
            'quality_score_mean', 'read_length_bp', 'samples_count',
            'notes', 'created_at'
        ]

    def get_samples_count(self, obj):
        return obj.samples.count()


class SampleSerializer(serializers.ModelSerializer):
    location = SamplingLocationBasicSerializer(read_only=True)
    sequencing_runs = SequencingRunSerializer(many=True, read_only=True)
    taxonomic_assignments_count = serializers.SerializerMethodField()
    biodiversity_metrics = serializers.SerializerMethodField()

    class Meta:
        model = Sample
        fields = [
            'id', 'sample_id', 'location', 'collection_datetime', 'sample_type',
            'volume_ml', 'extraction_method', 'dna_concentration_ng_ul',
            'amplicon_region', 'notes', 'sequencing_runs',
            'taxonomic_assignments_count', 'biodiversity_metrics',
            'created_at', 'updated_at'
        ]

    def get_taxonomic_assignments_count(self, obj):
        return obj.taxonomic_assignments.count()

    def get_biodiversity_metrics(self, obj):
        try:
            return BiodiversityMetricsSerializer(obj.biodiversity_metrics).data
        except BiodiversityMetrics.DoesNotExist:
            return None


class TaxonomicAssignmentSerializer(serializers.ModelSerializer):
    sample = serializers.StringRelatedField(read_only=True)
    full_taxonomy = serializers.ReadOnlyField()

    class Meta:
        model = TaxonomicAssignment
        fields = [
            'id', 'sample', 'sequence_id', 'sequence_data', 'kingdom',
            'phylum', 'class_name', 'order', 'family', 'genus', 'species',
            'database_source', 'confidence_level', 'confidence_score',
            'identity_percent', 'coverage_percent', 'e_value',
            'best_match_accession', 'is_novel_taxon', 'novel_cluster_id',
            'read_count', 'relative_abundance', 'full_taxonomy',
            'created_at', 'updated_at'
        ]


class BiodiversityMetricsSerializer(serializers.ModelSerializer):
    sample = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BiodiversityMetrics
        fields = [
            'id', 'sample', 'shannon_diversity', 'simpson_diversity',
            'chao1_richness', 'observed_otus', 'faith_pd', 'total_sequences',
            'assigned_sequences', 'novel_sequences', 'assignment_rate',
            'protist_percentage', 'metazoan_percentage', 'cnidarian_percentage',
            'fungi_percentage', 'calculation_date'
        ]


class AnalysisPipelineSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    samples = SampleSerializer(many=True, read_only=True)
    samples_count = serializers.SerializerMethodField()

    class Meta:
        model = AnalysisPipeline
        fields = [
            'id', 'name', 'status', 'databases_used', 'ai_models_used',
            'parameters', 'started_at', 'completed_at', 'total_runtime_minutes',
            'error_message', 'total_sequences_processed', 'sequences_assigned',
            'novel_taxa_discovered', 'created_by', 'samples', 'samples_count',
            'created_at', 'updated_at'
        ]

    def get_samples_count(self, obj):
        return obj.samples.count()


# Specialized serializers for different views
class TaxonomicSummarySerializer(serializers.Serializer):
    """Serializer for taxonomic composition summaries"""
    phylum = serializers.CharField()
    species_count = serializers.IntegerField()
    read_count = serializers.IntegerField()
    relative_abundance = serializers.FloatField()
    confidence_level = serializers.CharField()


class LocationDiversitySerializer(serializers.Serializer):
    """Serializer for location-based diversity data"""
    location_id = serializers.UUIDField()
    location_name = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    depth_meters = serializers.FloatField()
    shannon_diversity = serializers.FloatField()
    species_richness = serializers.IntegerField()
    novel_taxa_count = serializers.IntegerField()
    sample_count = serializers.IntegerField()


class SpeciesSearchResultSerializer(serializers.Serializer):
    """Serializer for species search results"""
    species = serializers.CharField()
    genus = serializers.CharField()
    family = serializers.CharField()
    phylum = serializers.CharField()
    sample_count = serializers.IntegerField()
    total_reads = serializers.IntegerField()
    confidence_score = serializers.FloatField()
    locations = serializers.ListField(child=serializers.CharField())
    is_novel = serializers.BooleanField()


class ExportDataSerializer(serializers.Serializer):
    """Serializer for data export requests"""
    format = serializers.ChoiceField(choices=['csv', 'json', 'pdf'])
    include_metadata = serializers.BooleanField(default=True)
    include_environmental = serializers.BooleanField(default=True)
    include_taxonomy = serializers.BooleanField(default=True)
    date_range_start = serializers.DateTimeField(required=False)
    date_range_end = serializers.DateTimeField(required=False)
    taxonomic_level = serializers.ChoiceField(
        choices=['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'],
        required=False
    )
    confidence_threshold = serializers.FloatField(min_value=0, max_value=1, required=False)


class FileUploadSerializer(serializers.Serializer):
    """Serializer for file uploads"""
    file = serializers.FileField()
    sample_id = serializers.CharField(max_length=100)
    file_type = serializers.ChoiceField(choices=['fastq', 'fasta', 'metadata'])
    description = serializers.CharField(max_length=500, required=False)
