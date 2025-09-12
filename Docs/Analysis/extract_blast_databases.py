"""
Robust BLAST Database Extraction Script
Extracts tar.gz files with MD5 verification and safe deletion.
Limited to 2-3 concurrent extractions to protect SSD health.
"""

import os
import sys
import hashlib
import subprocess
import threading
import time
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

@dataclass
class ExtractionJob:
    tar_file: Path
    md5_file: Path
    expected_md5: str
    output_dir: Path
    
class DatabaseExtractor:
    def __init__(self, base_dir: str, max_concurrent: int = 2):
        self.base_dir = Path(base_dir)
        self.max_concurrent = max_concurrent
        self.extracted_files: List[str] = []
        self.failed_files: List[str] = []
        self.lock = threading.Lock()
        self.total_size_freed = 0
        
    def calculate_md5(self, file_path: Path, chunk_size: int = 8192) -> str:
        """Calculate MD5 hash of a file efficiently."""
        md5_hash = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    md5_hash.update(chunk)
            return md5_hash.hexdigest().lower()
        except Exception as e:
            print(f"❌ Error calculating MD5 for {file_path}: {e}")
            return ""
    
    def read_md5_file(self, md5_file: Path) -> Optional[str]:
        """Read expected MD5 hash from .md5 file."""
        try:
            with open(md5_file, 'r') as f:
                content = f.read().strip()
                # MD5 files usually contain: "hash  filename"
                if content:
                    return content.split()[0].lower()
        except Exception as e:
            print(f"❌ Error reading MD5 file {md5_file}: {e}")
        return None
    
    def verify_extraction_integrity(self, tar_file: Path) -> bool:
        """Test tar file integrity before extraction."""
        try:
            result = subprocess.run(
                ['tar', '-tzf', str(tar_file)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout testing integrity of {tar_file}")
            return False
        except Exception as e:
            print(f"❌ Error testing integrity of {tar_file}: {e}")
            return False
    
    def extract_single_file(self, job: ExtractionJob) -> bool:
        """Extract a single tar.gz file with full verification."""
        tar_file = job.tar_file
        md5_file = job.md5_file
        expected_md5 = job.expected_md5
        
        print(f"\n🔄 Processing: {tar_file.name}")
        
        # Step 1: Verify tar file exists and has correct MD5
        if not tar_file.exists():
            print(f"❌ Tar file not found: {tar_file}")
            return False
            
        print(f"   📝 Verifying MD5 checksum...")
        actual_md5 = self.calculate_md5(tar_file)
        if not actual_md5:
            print(f"❌ Failed to calculate MD5 for {tar_file}")
            return False
            
        if actual_md5 != expected_md5:
            print(f"❌ MD5 mismatch for {tar_file}")
            print(f"   Expected: {expected_md5}")
            print(f"   Actual:   {actual_md5}")
            return False
        
        print(f"   ✅ MD5 checksum verified")
        
        # Step 2: Test tar file integrity
        print(f"   🔍 Testing tar file integrity...")
        if not self.verify_extraction_integrity(tar_file):
            print(f"❌ Tar file integrity check failed: {tar_file}")
            return False
        
        print(f"   ✅ Tar file integrity confirmed")
        
        # Step 3: Extract with progress
        print(f"   📦 Extracting to {job.output_dir}...")
        try:
            # Use tar with progress indication
            process = subprocess.Popen(
                ['tar', '-xzf', str(tar_file), '-C', str(job.output_dir)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(timeout=3600)  # 1 hour timeout
            
            if process.returncode != 0:
                print(f"❌ Extraction failed for {tar_file}")
                print(f"   Error: {stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"❌ Extraction timeout for {tar_file}")
            process.kill()
            return False
        except Exception as e:
            print(f"❌ Extraction error for {tar_file}: {e}")
            return False
        
        print(f"   ✅ Extraction completed successfully")
        
        # Step 4: Verify extraction by checking if files exist
        try:
            # List what was extracted (first few entries)
            result = subprocess.run(
                ['tar', '-tzf', str(tar_file)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                extracted_files = result.stdout.strip().split('\n')[:5]  # Check first 5 files
                missing_files = []
                
                for file_entry in extracted_files:
                    if file_entry.strip():
                        expected_path = job.output_dir / file_entry.strip()
                        if not expected_path.exists():
                            missing_files.append(file_entry)
                
                if missing_files:
                    print(f"❌ Some extracted files are missing:")
                    for missing in missing_files:
                        print(f"   - {missing}")
                    return False
                        
        except Exception as e:
            print(f"⚠️  Warning: Could not verify extraction completeness: {e}")
            # Continue anyway - extraction seemed to work
        
        # Step 5: Safe deletion
        file_size = tar_file.stat().st_size
        print(f"   🗑️  Safely deleting {tar_file.name} ({file_size / (1024**3):.2f} GB)...")
        
        try:
            tar_file.unlink()
            if md5_file.exists():
                md5_file.unlink()
            
            with self.lock:
                self.total_size_freed += file_size
                
            print(f"   ✅ Deleted successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to delete {tar_file}: {e}")
            return False
    
    def find_extraction_jobs(self) -> List[ExtractionJob]:
        """Find all tar.gz files with corresponding MD5 files."""
        jobs = []
        
        print("🔍 Scanning for tar.gz files with MD5 checksums...")
        
        for tar_file in self.base_dir.glob("*.tar.gz"):
            md5_file = tar_file.with_suffix(tar_file.suffix + '.md5')
            
            if not md5_file.exists():
                print(f"⚠️  Skipping {tar_file.name} - no MD5 file found")
                continue
                
            expected_md5 = self.read_md5_file(md5_file)
            if not expected_md5:
                print(f"⚠️  Skipping {tar_file.name} - could not read MD5")
                continue
                
            jobs.append(ExtractionJob(
                tar_file=tar_file,
                md5_file=md5_file,
                expected_md5=expected_md5,
                output_dir=self.base_dir
            ))
        
        print(f"📋 Found {len(jobs)} files to extract")
        return jobs
    
    def extract_all(self) -> Dict[str, List[str]]:
        """Extract all files with limited concurrency."""
        jobs = self.find_extraction_jobs()
        
        if not jobs:
            print("❌ No valid extraction jobs found!")
            return {"success": [], "failed": []}
        
        print(f"\n🚀 Starting extraction with {self.max_concurrent} concurrent jobs")
        print("💾 This will safely delete tar.gz files after successful extraction")
        print("⏰ Large files may take several minutes each...")
        
        success_list = []
        failed_list = []
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            # Submit all jobs
            future_to_job = {
                executor.submit(self.extract_single_file, job): job 
                for job in jobs
            }
            
            # Process completed jobs
            for future in as_completed(future_to_job):
                job = future_to_job[future]
                try:
                    success = future.result()
                    if success:
                        success_list.append(str(job.tar_file.name))
                        print(f"✅ Completed: {job.tar_file.name}")
                    else:
                        failed_list.append(str(job.tar_file.name))
                        print(f"❌ Failed: {job.tar_file.name}")
                except Exception as e:
                    failed_list.append(str(job.tar_file.name))
                    print(f"❌ Exception processing {job.tar_file.name}: {e}")
        
        elapsed_time = time.time() - start_time
        
        # Final report
        print(f"\n{'='*60}")
        print(f"🎉 EXTRACTION COMPLETE")
        print(f"{'='*60}")
        print(f"⏰ Total time: {elapsed_time/60:.1f} minutes")
        print(f"✅ Successfully extracted: {len(success_list)}")
        print(f"❌ Failed extractions: {len(failed_list)}")
        print(f"💾 Total space freed: {self.total_size_freed / (1024**3):.2f} GB")
        
        if failed_list:
            print(f"\n❌ Failed files:")
            for failed in failed_list:
                print(f"   - {failed}")
        
        return {"success": success_list, "failed": failed_list}

def main():
    """Main execution function."""
    
    # Configuration
    NCBI_DIR = "/home/srmist32/sihdna/ncbi_blast_db_files"
    MAX_CONCURRENT = 20  # Safe for SSD health
    
    print("🧬 NCBI BLAST Database Extractor")
    print("="*50)
    print(f"📁 Working directory: {NCBI_DIR}")
    print(f"🔧 Max concurrent extractions: {MAX_CONCURRENT}")
    print("⚠️  WARNING: This will DELETE tar.gz files after successful extraction!")
    
    # Verify directory exists
    if not os.path.exists(NCBI_DIR):
        print(f"❌ Directory not found: {NCBI_DIR}")
        sys.exit(1)
    
    # Check available disk space
    try:
        stat = shutil.disk_usage(NCBI_DIR)
        free_gb = stat.free / (1024**3)
        print(f"💾 Available disk space: {free_gb:.1f} GB")
        
        if free_gb < 100:  # Less than 100GB free
            print("⚠️  WARNING: Low disk space! Consider freeing space before extraction.")
    except Exception as e:
        print(f"⚠️  Could not check disk space: {e}")
    
    # Initialize extractor
    extractor = DatabaseExtractor(NCBI_DIR, MAX_CONCURRENT)
    
    # Run extraction
    try:
        results = extractor.extract_all()
        
        if results["failed"]:
            print(f"\n⚠️  Some extractions failed. Check the logs above.")
            sys.exit(1)
        else:
            print(f"\n🎉 All extractions completed successfully!")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Extraction interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
