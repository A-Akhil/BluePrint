#!/usr/bin/env python
"""
Sample data creation script for Blueprint Backend
"""
import os
import sys
import django
from datetime import datetime, date
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blueprint_backend.settings')
django.setup()

from core.models import (
    Expedition, SamplingLocation, EnvironmentalData, Sample,
    SequencingRun, TaxonomicAssignment, BiodiversityMetrics, AnalysisPipeline
)
from django.contrib.auth.models import User

def create_sample_data():
    print("Creating sample data for Blueprint Backend...")
    
    # Clear existing data to avoid conflicts
    print("Clearing existing data...")
    TaxonomicAssignment.objects.all().delete()
    BiodiversityMetrics.objects.all().delete()
    Sample.objects.all().delete()
    EnvironmentalData.objects.all().delete()
    SamplingLocation.objects.all().delete()
    AnalysisPipeline.objects.all().delete()
    SequencingRun.objects.all().delete()
    Expedition.objects.all().delete()
    
    # Get the existing superuser
    pi_user = User.objects.get(username='hariharan')
    
    # Create a second user for the second expedition
    pi_user2, created = User.objects.get_or_create(
        username='marine_bio',
        defaults={
            'email': 'marine.bio@cmlre.gov.in',
            'first_name': 'Marine',
            'last_name': 'Biologist'
        }
    )
    
    # Create Expeditions
    expedition1 = Expedition.objects.create(
        name="Deep Sea Arabian Sea Expedition 2024",
        description="Comprehensive eDNA sampling expedition in the Arabian Sea. PI: Dr. Hariharan M, Institution: CMLRE, Funding: Ministry of Earth Sciences",
        start_date=datetime(2024, 6, 1),
        end_date=datetime(2024, 6, 15),
        principal_investigator=pi_user,
        vessel_name="ORV Sagar Manjusha"
    )
    
    expedition2 = Expedition.objects.create(
        name="Bay of Bengal Biodiversity Survey 2024",
        description="Marine biodiversity assessment using environmental DNA. PI: Dr. Marine Biologist, Institution: CMLRE, Funding: Ministry of Earth Sciences",
        start_date=datetime(2024, 8, 10),
        end_date=datetime(2024, 8, 25),
        principal_investigator=pi_user2,
        vessel_name="ORV Sagar Sampada"
    )
    
    print(f"Created expeditions: {expedition1.name}, {expedition2.name}")
    
    # Create Sampling Locations
    locations = [
        {
            'name': 'Station AS-01',
            'latitude': 15.5000,
            'longitude': 68.7500,
            'depth_meters': 2500.0,
            'habitat_type': 'deep_sea_trench',
            'expedition': expedition1
        },
        {
            'name': 'Station AS-02', 
            'latitude': 16.2500,
            'longitude': 69.1250,
            'depth_meters': 3200.0,
            'habitat_type': 'deep_sea_trench',
            'expedition': expedition1
        },
        {
            'name': 'Station BB-01',
            'latitude': 13.0833,
            'longitude': 80.2785,
            'depth_meters': 1800.0,
            'habitat_type': 'continental_slope',
            'expedition': expedition2
        },
        {
            'name': 'Station BB-02',
            'latitude': 14.5000,
            'longitude': 81.5000,
            'depth_meters': 2100.0,
            'habitat_type': 'deep_sea_trench',
            'expedition': expedition2
        }
    ]
    
    sampling_locations = []
    for loc_data in locations:
        location = SamplingLocation.objects.create(**loc_data)
        sampling_locations.append(location)
    
    print(f"Created {len(sampling_locations)} sampling locations")
    
    # Create Environmental Data
    for i, location in enumerate(sampling_locations):
        EnvironmentalData.objects.create(
            location=location,
            measurement_datetime=datetime(2024, 6, 5 + i, 10, 30),
            temperature_celsius=4.5 + (i * 0.3),
            salinity_psu=34.8 + (i * 0.1),
            dissolved_oxygen_mg_l=6.2 - (i * 0.2),
            ph=8.1 - (i * 0.05),
            pressure_dbar=location.depth_meters * 1.02,
            turbidity_ntu=0.5 + (i * 0.1)
        )
    
    print("Created environmental data for all locations")
    
    # Create Samples
    sample_types = ['sediment', 'water']
    samples = []
    
    for i, location in enumerate(sampling_locations):
        for j, sample_type in enumerate(sample_types):
            sample = Sample.objects.create(
                sample_id=f"{location.name}-{sample_type.upper()}-{i+1:03d}",
                location=location,
                sample_type=sample_type,
                collection_datetime=datetime(2024, 6, 5 + i, 14, 30),
                volume_ml=1000.0 if sample_type == 'water' else 50.0,
                extraction_method='DNeasy',
                dna_concentration_ng_ul=25.5 + (i * 2.3),
                notes=f"{sample_type} sample from {location.name}"
            )
            samples.append(sample)
    
    print(f"Created {len(samples)} samples")
    
    # Create Analysis Pipeline
    pipeline = AnalysisPipeline.objects.create(
        name="18S rRNA Metabarcoding Pipeline v2.1",
        status='completed',
        databases_used=['SILVA_138', 'PR2', 'EukRef'],
        ai_models_used=['BLAST', 'RDP_Classifier'],
        parameters={
            'target_gene': '18S rRNA',
            'primer_forward': 'CCAGCASCYGCGGTAATTCC',
            'primer_reverse': 'ACTTTCGTTCTTGATYRA',
            'sequencing_platform': 'illumina_miseq',
            'reference_database': 'SILVA_138',
            'quality_threshold': 30.0,
            'identity_threshold': 97.0
        },
        started_at=datetime(2024, 7, 1, 9, 0),
        completed_at=datetime(2024, 7, 3, 15, 30),
        total_runtime_minutes=2850.0,
        total_sequences_processed=250000,
        sequences_assigned=235000,
        novel_taxa_discovered=12,
        created_by=pi_user
    )
    
    # Add samples to the pipeline
    pipeline.samples.set(samples)
    
    print(f"Created analysis pipeline: {pipeline.name}")
    
    # Create Sequencing Runs
    sequencing_runs = []
    for i in range(2):  # Create 2 sequencing runs
        run = SequencingRun.objects.create(
            run_id=f"MiSeq_Run_{i+1:03d}_2024",
            platform='illumina_miseq',
            run_date=datetime(2024, 7, 1 + i*2, 9, 0),
            total_reads=500000 + (i * 100000),
            quality_score_mean=32.5 + (i * 0.5),
            read_length_bp=300,
            notes=f"Sequencing run {i+1} for eDNA samples"
        )
        # Add some samples to each run
        run.samples.set(samples[i*4:(i+1)*4])  # 4 samples per run
        sequencing_runs.append(run)
    
    print(f"Created {len(sequencing_runs)} sequencing runs")
    
    # Create Taxonomic Assignments
    taxa_data = [
        ('Copepoda', 'Eukaryota', 'Arthropoda', 'Crustacea', 'Copepoda', '', '', ''),
        ('Chaetognatha', 'Eukaryota', 'Chaetognatha', 'Sagittoidea', 'Chaetognatha', '', '', ''),
        ('Cnidaria', 'Eukaryota', 'Cnidaria', 'Anthozoa', 'Scleractinia', 'Fungiidae', 'Fungia', 'scutaria'),
        ('Foraminifera', 'Eukaryota', 'Foraminifera', 'Globothalamea', 'Rotaliida', 'Planorbulinidae', 'Planorbulina', 'mediterranensis'),
        ('Radiolaria', 'Eukaryota', 'Radiolaria', 'Polycystinea', 'Spumellarida', 'Actinommidae', 'Actinomma', 'antarcticum')
    ]
    
    taxonomic_assignments = []
    for i, sample in enumerate(samples):
        for j, (common_name, kingdom, phylum, class_name, order, family, genus, species) in enumerate(taxa_data):
            assignment = TaxonomicAssignment.objects.create(
                sample=sample,
                sequence_id=f"SEQ_{i+1:03d}_{j+1:03d}",
                sequence_data="ATCGATCGATCG" * 20,  # Mock sequence data
                kingdom=kingdom,
                phylum=phylum,
                class_name=class_name,
                order=order,
                family=family,
                genus=genus,
                species=species,
                database_source='SSU_eukaryote_rRNA',
                confidence_level='high' if j < 3 else 'medium',
                confidence_score=0.85 + (j * 0.02),
                identity_percent=95.5 + (j * 0.8),
                coverage_percent=88.0 + (j * 1.5),
                e_value=1e-50,
                best_match_accession=f"ABC{12345+j:05d}"
            )
            taxonomic_assignments.append(assignment)
    
    print(f"Created {len(taxonomic_assignments)} taxonomic assignments")
    
    # Create Biodiversity Metrics
    for i, sample in enumerate(samples):
        BiodiversityMetrics.objects.create(
            sample=sample,
            shannon_diversity=2.45 + (i * 0.1),
            simpson_diversity=0.85 - (i * 0.02),
            chao1_richness=45.2 + (i * 2.3),
            observed_otus=38 + i,
            faith_pd=12.8 + (i * 0.5),
            total_sequences=10000 + (i * 500),
            assigned_sequences=9200 + (i * 450),
            novel_sequences=12 + i,
            assignment_rate=0.92 + (i * 0.005),
            protist_percentage=45.5 + (i * 1.2),
            metazoan_percentage=32.1 - (i * 0.8),
            cnidarian_percentage=8.3 + (i * 0.3),
            fungi_percentage=2.1 + (i * 0.1)
        )
    
    print("Created biodiversity metrics for all samples")
    print("\n✅ Sample data creation completed successfully!")
    print(f"📊 Summary:")
    print(f"   - Expeditions: {Expedition.objects.count()}")
    print(f"   - Sampling Locations: {SamplingLocation.objects.count()}")
    print(f"   - Environmental Data: {EnvironmentalData.objects.count()}")
    print(f"   - Samples: {Sample.objects.count()}")
    print(f"   - Sequencing Runs: {SequencingRun.objects.count()}")
    print(f"   - Taxonomic Assignments: {TaxonomicAssignment.objects.count()}")
    print(f"   - Biodiversity Metrics: {BiodiversityMetrics.objects.count()}")
    print(f"\n🌐 Access the admin at: http://127.0.0.1:8001/admin/")
    print(f"🔌 API endpoints at: http://127.0.0.1:8001/api/v1/")

if __name__ == '__main__':
    create_sample_data()
