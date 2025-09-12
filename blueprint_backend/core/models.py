from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Expedition(models.Model):
    """Represents a deep-sea expedition for eDNA collection"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    vessel_name = models.CharField(max_length=100)
    principal_investigator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} ({self.start_date.year})"


class SamplingLocation(models.Model):
    """Geographic location for eDNA sampling"""
    HABITAT_CHOICES = [
        ('abyssal_plain', 'Abyssal Plain'),
        ('hydrothermal_vent', 'Hydrothermal Vent'),
        ('seamount', 'Seamount'),
        ('deep_sea_trench', 'Deep Sea Trench'),
        ('continental_slope', 'Continental Slope'),
        ('mid_ocean_ridge', 'Mid Ocean Ridge'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    depth_meters = models.FloatField(validators=[MinValueValidator(0)])
    habitat_type = models.CharField(max_length=50, choices=HABITAT_CHOICES)
    expedition = models.ForeignKey(Expedition, on_delete=models.CASCADE, related_name='locations')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.depth_meters}m)"


class EnvironmentalData(models.Model):
    """Environmental parameters at sampling location"""
    location = models.ForeignKey(SamplingLocation, on_delete=models.CASCADE, related_name='environmental_data')
    measurement_datetime = models.DateTimeField()
    temperature_celsius = models.FloatField(null=True, blank=True)
    salinity_psu = models.FloatField(null=True, blank=True)  # Practical Salinity Units
    ph = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(14)])
    dissolved_oxygen_mg_l = models.FloatField(null=True, blank=True)
    pressure_dbar = models.FloatField(null=True, blank=True)
    turbidity_ntu = models.FloatField(null=True, blank=True)
    chlorophyll_a_mg_m3 = models.FloatField(null=True, blank=True)
    nitrate_umol_l = models.FloatField(null=True, blank=True)
    phosphate_umol_l = models.FloatField(null=True, blank=True)
    silicate_umol_l = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-measurement_datetime']

    def __str__(self):
        return f"Environmental data for {self.location.name} at {self.measurement_datetime}"


class Sample(models.Model):
    """Represents an eDNA sample collected from the deep sea"""
    SAMPLE_TYPE_CHOICES = [
        ('sediment', 'Sediment'),
        ('water', 'Water'),
        ('both', 'Both Sediment and Water'),
    ]

    EXTRACTION_METHOD_CHOICES = [
        ('DNeasy', 'DNeasy PowerSoil Kit'),
        ('phenol_chloroform', 'Phenol-Chloroform'),
        ('ctab', 'CTAB Method'),
        ('commercial_kit', 'Commercial Kit (Other)'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sample_id = models.CharField(max_length=100, unique=True)
    location = models.ForeignKey(SamplingLocation, on_delete=models.CASCADE, related_name='samples')
    collection_datetime = models.DateTimeField()
    sample_type = models.CharField(max_length=20, choices=SAMPLE_TYPE_CHOICES)
    volume_ml = models.FloatField(validators=[MinValueValidator(0)])
    extraction_method = models.CharField(max_length=50, choices=EXTRACTION_METHOD_CHOICES)
    dna_concentration_ng_ul = models.FloatField(null=True, blank=True)
    amplicon_region = models.CharField(max_length=50, default='18S_V4')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-collection_datetime']

    def __str__(self):
        return f"{self.sample_id} - {self.location.name}"


class SequencingRun(models.Model):
    """Represents a sequencing run for eDNA samples"""
    PLATFORM_CHOICES = [
        ('illumina_miseq', 'Illumina MiSeq'),
        ('illumina_hiseq', 'Illumina HiSeq'),
        ('illumina_novaseq', 'Illumina NovaSeq'),
        ('ion_torrent', 'Ion Torrent'),
        ('nanopore', 'Oxford Nanopore'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    run_id = models.CharField(max_length=100, unique=True)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    run_date = models.DateTimeField()
    samples = models.ManyToManyField(Sample, related_name='sequencing_runs')
    total_reads = models.BigIntegerField(null=True, blank=True)
    quality_score_mean = models.FloatField(null=True, blank=True)
    read_length_bp = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-run_date']

    def __str__(self):
        return f"{self.run_id} ({self.platform})"


class TaxonomicAssignment(models.Model):
    """Represents a taxonomic assignment for a sequence"""
    CONFIDENCE_LEVELS = [
        ('high', 'High (>90%)'),
        ('medium', 'Medium (70-90%)'),
        ('low', 'Low (50-70%)'),
        ('uncertain', 'Uncertain (<50%)'),
    ]

    DATABASE_CHOICES = [
        ('SSU_eukaryote_rRNA', 'SSU Eukaryote rRNA'),
        ('LSU_eukaryote_rRNA', 'LSU Eukaryote rRNA'),
        ('ITS_eukaryote_sequences', 'ITS Eukaryote Sequences'),
        ('nt_euk', 'NCBI Eukaryotic Nucleotide'),
        ('ai_classification', 'AI Classification'),
        ('phylogenetic_placement', 'Phylogenetic Placement'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='taxonomic_assignments')
    sequence_id = models.CharField(max_length=200)
    sequence_data = models.TextField()
    
    # Taxonomic hierarchy
    kingdom = models.CharField(max_length=100, default='Eukaryota')
    phylum = models.CharField(max_length=100, null=True, blank=True)
    class_name = models.CharField(max_length=100, null=True, blank=True)
    order = models.CharField(max_length=100, null=True, blank=True)
    family = models.CharField(max_length=100, null=True, blank=True)
    genus = models.CharField(max_length=100, null=True, blank=True)
    species = models.CharField(max_length=200, null=True, blank=True)
    
    # Assignment metadata
    database_source = models.CharField(max_length=50, choices=DATABASE_CHOICES)
    confidence_level = models.CharField(max_length=20, choices=CONFIDENCE_LEVELS)
    confidence_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    identity_percent = models.FloatField(null=True, blank=True)
    coverage_percent = models.FloatField(null=True, blank=True)
    e_value = models.FloatField(null=True, blank=True)
    best_match_accession = models.CharField(max_length=50, null=True, blank=True)
    
    # Novel taxa indicators
    is_novel_taxon = models.BooleanField(default=False)
    novel_cluster_id = models.CharField(max_length=100, null=True, blank=True)
    
    read_count = models.IntegerField(default=1)
    relative_abundance = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-confidence_score', '-read_count']
        unique_together = ['sample', 'sequence_id']

    def __str__(self):
        return f"{self.sequence_id} - {self.species or self.genus or self.family or 'Unknown'}"

    @property
    def full_taxonomy(self):
        """Return the full taxonomic classification as a string"""
        taxonomy_levels = [
            self.kingdom, self.phylum, self.class_name, 
            self.order, self.family, self.genus, self.species
        ]
        return ' > '.join([level for level in taxonomy_levels if level])


class BiodiversityMetrics(models.Model):
    """Calculated biodiversity metrics for samples"""
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE, related_name='biodiversity_metrics')
    
    # Alpha diversity metrics
    shannon_diversity = models.FloatField(null=True, blank=True)
    simpson_diversity = models.FloatField(null=True, blank=True)
    chao1_richness = models.FloatField(null=True, blank=True)
    observed_otus = models.IntegerField(null=True, blank=True)
    faith_pd = models.FloatField(null=True, blank=True)  # Faith's Phylogenetic Diversity
    
    # Community composition
    total_sequences = models.IntegerField()
    assigned_sequences = models.IntegerField()
    novel_sequences = models.IntegerField(default=0)
    assignment_rate = models.FloatField()
    
    # Dominant taxa percentages
    protist_percentage = models.FloatField(null=True, blank=True)
    metazoan_percentage = models.FloatField(null=True, blank=True)
    cnidarian_percentage = models.FloatField(null=True, blank=True)
    fungi_percentage = models.FloatField(null=True, blank=True)
    
    calculation_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Biodiversity metrics for {self.sample.sample_id}"


class AnalysisPipeline(models.Model):
    """Represents an analysis pipeline execution"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    samples = models.ManyToManyField(Sample, related_name='analysis_pipelines')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Pipeline configuration
    databases_used = models.JSONField(default=list)
    ai_models_used = models.JSONField(default=list)
    parameters = models.JSONField(default=dict)
    
    # Execution metadata
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_runtime_minutes = models.FloatField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    # Results summary
    total_sequences_processed = models.IntegerField(null=True, blank=True)
    sequences_assigned = models.IntegerField(null=True, blank=True)
    novel_taxa_discovered = models.IntegerField(null=True, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.status}"
