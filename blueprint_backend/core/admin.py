from django.contrib import admin
from .models import (
    Expedition, SamplingLocation, EnvironmentalData, Sample,
    SequencingRun, TaxonomicAssignment, BiodiversityMetrics, AnalysisPipeline
)


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ['name', 'vessel_name', 'start_date', 'end_date', 'principal_investigator']
    list_filter = ['start_date', 'vessel_name', 'principal_investigator']
    search_fields = ['name', 'description', 'vessel_name']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SamplingLocation)
class SamplingLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'habitat_type', 'depth_meters', 'expedition', 'latitude', 'longitude']
    list_filter = ['habitat_type', 'expedition']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']


@admin.register(EnvironmentalData)
class EnvironmentalDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'measurement_datetime', 'temperature_celsius', 'salinity_psu', 'ph']
    list_filter = ['location__habitat_type', 'measurement_datetime']
    search_fields = ['location__name']
    date_hierarchy = 'measurement_datetime'


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ['sample_id', 'location', 'collection_datetime', 'sample_type', 'extraction_method']
    list_filter = ['sample_type', 'extraction_method', 'collection_datetime', 'location__habitat_type']
    search_fields = ['sample_id', 'notes', 'location__name']
    date_hierarchy = 'collection_datetime'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SequencingRun)
class SequencingRunAdmin(admin.ModelAdmin):
    list_display = ['run_id', 'platform', 'run_date', 'total_reads', 'quality_score_mean']
    list_filter = ['platform', 'run_date']
    search_fields = ['run_id', 'notes']
    date_hierarchy = 'run_date'
    filter_horizontal = ['samples']


@admin.register(TaxonomicAssignment)
class TaxonomicAssignmentAdmin(admin.ModelAdmin):
    list_display = ['sequence_id', 'sample', 'species', 'confidence_score', 'database_source', 'is_novel_taxon']
    list_filter = ['database_source', 'confidence_level', 'is_novel_taxon', 'kingdom', 'phylum']
    search_fields = ['sequence_id', 'species', 'genus', 'family', 'phylum']
    readonly_fields = ['created_at', 'updated_at', 'full_taxonomy']


@admin.register(BiodiversityMetrics)
class BiodiversityMetricsAdmin(admin.ModelAdmin):
    list_display = ['sample', 'shannon_diversity', 'simpson_diversity', 'observed_otus', 'assignment_rate']
    list_filter = ['calculation_date']
    search_fields = ['sample__sample_id', 'sample__location__name']
    readonly_fields = ['calculation_date']


@admin.register(AnalysisPipeline)
class AnalysisPipelineAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_by', 'started_at', 'completed_at', 'total_runtime_minutes']
    list_filter = ['status', 'created_by', 'created_at']
    search_fields = ['name', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['samples']
