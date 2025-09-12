#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
import psutil

BASE_URL = "https://ftp.ncbi.nlm.nih.gov/blast/db/"
DOWNLOAD_DIR = "ncbi_blast_db_files"
EXCLUDE_LIST = ['FASTA/', 'cloud/', 'experimental/', 'v4/', 'v5/', 'README']

def get_remote_file_list():
    print(f"Fetching remote file list from {BASE_URL}...")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch file list: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    files = []

    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if not href or any(href.startswith(ex) for ex in EXCLUDE_LIST) or href.endswith('/'):
            continue
        files.append(href)

    print(f"Found {len(files)} remote files.")
    return files

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8*1024*1024), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def verify_file_md5(file_name, md5_dict):
    if not os.path.exists(file_name):
        return (file_name, "MISSING")
    actual_md5 = calculate_md5(file_name)
    expected_md5 = md5_dict.get(file_name)
    if expected_md5 is None:
        return (file_name, "NO_MD5")
    if actual_md5.lower() == expected_md5.lower():
        return (file_name, "OK")
    return (file_name, "FAILED")

def load_md5_files():
    md5_dict = {}
    md5_files = [f for f in os.listdir('.') if f.endswith('.md5')]
    for md5_file in md5_files:
        with open(md5_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    md5, fname = parts
                    md5_dict[fname] = md5
    return md5_dict

def verify_local_files_parallel(remote_files):
    if not os.path.exists(DOWNLOAD_DIR):
        print(f"Download directory '{DOWNLOAD_DIR}' does not exist.")
        return [], []

    os.chdir(DOWNLOAD_DIR)
    local_files = [f for f in os.listdir('.') if not f.endswith('.aria2')]
    missing_files = [f for f in remote_files if f not in local_files]

    md5_dict = load_md5_files()
    corrupted_files = []

    # CPU info
    physical_cores = psutil.cpu_count(logical=False)
    logical_threads = psutil.cpu_count(logical=True)
    max_workers = min(logical_threads, len([f for f in local_files if f.endswith('.tar.gz')]))
    print(f"\nCPU Info: {physical_cores} physical cores, {logical_threads} logical threads")
    print(f"Running {max_workers} parallel MD5 verification tasks...\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(verify_file_md5, f, md5_dict) for f in local_files if f.endswith('.tar.gz')]
        for future in as_completed(futures):
            file_name, status = future.result()
            if status != "OK":
                corrupted_files.append(file_name)
            print(f"{file_name}: {status}")

    return missing_files, corrupted_files

def print_summary(missing_files, corrupted_files):
    print("\n========== SUMMARY ==========")
    if missing_files:
        print(f"\nMissing files ({len(missing_files)}):")
        for f in missing_files:
            print(f"  {f}")
    else:
        print("\nNo files are missing.")

    if corrupted_files:
        print(f"\nCorrupted / checksum failed files ({len(corrupted_files)}):")
        for f in corrupted_files:
            print(f"  {f}")
    else:
        print("\nNo files failed checksum verification.")

    if not missing_files and not corrupted_files:
        print("\n✅ All files are present and verified successfully!")
    else:
        print("\n❌ Some files are missing or corrupted. Please re-download them.")

if __name__ == "__main__":
    remote_files = get_remote_file_list()
    missing_files, corrupted_files = verify_local_files_parallel(remote_files)
    print_summary(missing_files, corrupted_files)

