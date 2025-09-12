from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
import pandas as pd
import numpy as np
from datetime import datetime
import json
import random

from .models import (
    Sample, TaxonomicAssignment, BiodiversityMetrics, AnalysisPipeline
)


@shared_task
def calculate_biodiversity_metrics(sample_id):
    """Calculate biodiversity metrics for a sample"""
    try:
        sample = Sample.objects.get(id=sample_id)
        assignments = sample.taxonomic_assignments.all()
        
        if not assignments.exists():
            return {'error': 'No taxonomic assignments found for sample'}
        
        # Prepare data for calculations
        species_counts = {}
        total_reads = 0
        
        for assignment in assignments:
            species = assignment.species or f"{assignment.genus}_sp" or "Unknown"
            reads = assignment.read_count
            
            if species in species_counts:
                species_counts[species] += reads
            else:
                species_counts[species] = reads
            
            total_reads += reads
        
        # Calculate metrics
        observed_otus = len(species_counts)
        
        # Shannon diversity
        shannon_diversity = 0
        for count in species_counts.values():
            if count > 0:
                p = count / total_reads
                shannon_diversity -= p * np.log(p)
        
        # Simpson diversity
        simpson_diversity = 0
        for count in species_counts.values():
            if count > 0:
                p = count / total_reads
                simpson_diversity += p * p
        simpson_diversity = 1 - simpson_diversity
        
        # Chao1 richness estimator
        singletons = sum(1 for count in species_counts.values() if count == 1)
        doubletons = sum(1 for count in species_counts.values() if count == 2)
        
        if doubletons > 0:
            chao1_richness = observed_otus + (singletons * singletons) / (2 * doubletons)
        else:
            chao1_richness = observed_otus
        
        # Calculate taxonomic composition percentages
        protist_phylums = ['Foraminifera', 'Radiolaria', 'Ciliophora', 'Dinoflagellata']
        metazoan_phylums = ['Nematoda', 'Arthropoda', 'Mollusca', 'Annelida']
        cnidarian_phylums = ['Cnidaria']
        fungi_phylums = ['Ascomycota', 'Basidiomycota']
        
        protist_reads = assignments.filter(phylum__in=protist_phylums).aggregate(
            total=models.Sum('read_count'))['total'] or 0
        metazoan_reads = assignments.filter(phylum__in=metazoan_phylums).aggregate(
            total=models.Sum('read_count'))['total'] or 0
        cnidarian_reads = assignments.filter(phylum__in=cnidarian_phylums).aggregate(
            total=models.Sum('read_count'))['total'] or 0
        fungi_reads = assignments.filter(phylum__in=fungi_phylums).aggregate(
            total=models.Sum('read_count'))['total'] or 0
        
        assigned_sequences = assignments.count()
        novel_sequences = assignments.filter(is_novel_taxon=True).count()
        assignment_rate = assigned_sequences / total_reads if total_reads > 0 else 0
        
        # Create or update biodiversity metrics
        metrics, created = BiodiversityMetrics.objects.update_or_create(
            sample=sample,
            defaults={
                'shannon_diversity': shannon_diversity,
                'simpson_diversity': simpson_diversity,
                'chao1_richness': chao1_richness,
                'observed_otus': observed_otus,
                'total_sequences': total_reads,
                'assigned_sequences': assigned_sequences,
                'novel_sequences': novel_sequences,
                'assignment_rate': assignment_rate,
                'protist_percentage': (protist_reads / total_reads * 100) if total_reads > 0 else 0,
                'metazoan_percentage': (metazoan_reads / total_reads * 100) if total_reads > 0 else 0,
                'cnidarian_percentage': (cnidarian_reads / total_reads * 100) if total_reads > 0 else 0,
                'fungi_percentage': (fungi_reads / total_reads * 100) if total_reads > 0 else 0,
            }
        )
        
        return {
            'success': True,
            'sample_id': str(sample_id),
            'metrics': {
                'shannon_diversity': shannon_diversity,
                'simpson_diversity': simpson_diversity,
                'observed_otus': observed_otus,
                'total_sequences': total_reads
            }
        }
        
    except Sample.DoesNotExist:
        return {'error': f'Sample {sample_id} not found'}
    except Exception as e:
        return {'error': str(e)}


@shared_task
def process_sequence_file(sample_id, file_path, file_type='fastq'):
    """Process uploaded sequence files"""
    try:
        sample = Sample.objects.get(id=sample_id)
        
        # This would implement actual sequence processing
        # For now, we'll simulate the process
        
        # Simulated processing steps:
        # 1. Quality control
        # 2. Sequence trimming
        # 3. Database search
        # 4. AI classification
        # 5. Create taxonomic assignments
        
        # Simulate some taxonomic assignments
        import random
        
        sample_taxa = [
            {'kingdom': 'Eukaryota', 'phylum': 'Foraminifera', 'genus': 'Globigerina', 'species': 'Globigerina bulloides'},
            {'kingdom': 'Eukaryota', 'phylum': 'Radiolaria', 'genus': 'Spongaster', 'species': 'Spongaster tetras'},
            {'kingdom': 'Eukaryota', 'phylum': 'Ciliophora', 'genus': 'Paramecium', 'species': 'Paramecium aurelia'},
            {'kingdom': 'Eukaryota', 'phylum': 'Nematoda', 'genus': 'Caenorhabditis', 'species': 'Caenorhabditis elegans'},
        ]
        
        assignments_created = 0
        for i in range(random.randint(50, 200)):
            taxon = random.choice(sample_taxa)
            
            assignment = TaxonomicAssignment.objects.create(
                sample=sample,
                sequence_id=f"seq_{sample.sample_id}_{i:04d}",
                sequence_data="ATCGATCGATCGATCG...",  # Placeholder
                kingdom=taxon['kingdom'],
                phylum=taxon['phylum'],
                genus=taxon['genus'],
                species=taxon['species'],
                database_source='SSU_eukaryote_rRNA',
                confidence_level='high' if random.random() > 0.3 else 'medium',
                confidence_score=random.uniform(0.7, 0.98),
                read_count=random.randint(1, 50),
                is_novel_taxon=random.random() < 0.1  # 10% chance of novel taxon
            )
            assignments_created += 1
        
        # Calculate biodiversity metrics after processing
        calculate_biodiversity_metrics.delay(sample_id)
        
        return {
            'success': True,
            'sample_id': str(sample_id),
            'assignments_created': assignments_created,
            'file_processed': file_path
        }
        
    except Sample.DoesNotExist:
        return {'error': f'Sample {sample_id} not found'}
    except Exception as e:
        return {'error': str(e)}


@shared_task
def run_analysis_pipeline(pipeline_id):
    """Execute an analysis pipeline"""
    try:
        pipeline = AnalysisPipeline.objects.get(id=pipeline_id)
        pipeline.status = 'running'
        pipeline.started_at = datetime.now()
        pipeline.save()
        
        total_sequences = 0
        sequences_assigned = 0
        novel_taxa = 0
        
        # Process each sample in the pipeline
        for sample in pipeline.samples.all():
            # Process the sample (this would call actual analysis tools)
            result = process_sequence_file.delay(sample.id, f"/temp/{sample.sample_id}.fastq")
            
            # Simulate processing time
            import time
            time.sleep(2)
            
            # Update counters (these would come from actual processing)
            total_sequences += random.randint(1000, 5000)
            sequences_assigned += random.randint(600, 3000)
            novel_taxa += random.randint(5, 50)
        
        # Update pipeline with results
        pipeline.status = 'completed'
        pipeline.completed_at = datetime.now()
        pipeline.total_runtime_minutes = (pipeline.completed_at - pipeline.started_at).total_seconds() / 60
        pipeline.total_sequences_processed = total_sequences
        pipeline.sequences_assigned = sequences_assigned
        pipeline.novel_taxa_discovered = novel_taxa
        pipeline.save()
        
        # Send notification email
        send_pipeline_completion_email.delay(pipeline_id)
        
        return {
            'success': True,
            'pipeline_id': str(pipeline_id),
            'total_sequences': total_sequences,
            'sequences_assigned': sequences_assigned,
            'novel_taxa': novel_taxa
        }
        
    except AnalysisPipeline.DoesNotExist:
        return {'error': f'Pipeline {pipeline_id} not found'}
    except Exception as e:
        # Mark pipeline as failed
        try:
            pipeline = AnalysisPipeline.objects.get(id=pipeline_id)
            pipeline.status = 'failed'
            pipeline.error_message = str(e)
            pipeline.save()
        except:
            pass
        return {'error': str(e)}


@shared_task
def send_pipeline_completion_email(pipeline_id):
    """Send email notification when pipeline completes"""
    try:
        pipeline = AnalysisPipeline.objects.get(id=pipeline_id)
        
        subject = f"Analysis Pipeline Completed: {pipeline.name}"
        message = f"""
        Your analysis pipeline "{pipeline.name}" has completed successfully.
        
        Results Summary:
        - Total sequences processed: {pipeline.total_sequences_processed}
        - Sequences assigned: {pipeline.sequences_assigned}
        - Novel taxa discovered: {pipeline.novel_taxa_discovered}
        - Runtime: {pipeline.total_runtime_minutes:.1f} minutes
        
        You can view the full results in the Blueprint eDNA platform.
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [pipeline.created_by.email],
            fail_silently=False,
        )
        
        return {'success': True, 'email_sent': True}
        
    except Exception as e:
        return {'error': str(e)}


@shared_task
def generate_expedition_report(expedition_id, report_format='pdf'):
    """Generate comprehensive expedition report"""
    try:
        from core.models import Expedition
        
        expedition = Expedition.objects.get(id=expedition_id)
        
        # Collect expedition data
        locations = expedition.locations.all()
        samples = Sample.objects.filter(location__expedition=expedition)
        assignments = TaxonomicAssignment.objects.filter(sample__location__expedition=expedition)
        
        report_data = {
            'expedition': {
                'name': expedition.name,
                'dates': f"{expedition.start_date} to {expedition.end_date}",
                'vessel': expedition.vessel_name,
                'pi': expedition.principal_investigator.get_full_name()
            },
            'summary': {
                'total_locations': locations.count(),
                'total_samples': samples.count(),
                'total_sequences': assignments.count(),
                'novel_taxa': assignments.filter(is_novel_taxon=True).count()
            },
            'biodiversity': {
                'dominant_phyla': list(assignments.values('phylum').annotate(
                    count=models.Count('id')).order_by('-count')[:10]),
                'depth_range': {
                    'min': locations.aggregate(min_depth=models.Min('depth_meters'))['min_depth'],
                    'max': locations.aggregate(max_depth=models.Max('depth_meters'))['max_depth']
                }
            }
        }
        
        # Generate report file (this would use ReportLab or similar)
        report_filename = f"expedition_{expedition.id}_report.{report_format}"
        
        # For now, just save the data as JSON
        import os
        os.makedirs(settings.MEDIA_ROOT / 'reports', exist_ok=True)
        with open(settings.MEDIA_ROOT / 'reports' / report_filename.replace('.pdf', '.json'), 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        return {
            'success': True,
            'expedition_id': str(expedition_id),
            'report_file': f"reports/{report_filename}",
            'report_data': report_data
        }
        
    except Exception as e:
        return {'error': str(e)}
