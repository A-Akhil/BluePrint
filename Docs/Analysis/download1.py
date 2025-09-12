#!/usr/bin/env python3
import os
import sys
import subprocess
import requests
from bs4 import BeautifulSoup
import glob

def get_download_links(url, exclude_dirs):
    """
    Fetches the directory listing and extracts file links, excluding specified directories.
    """
    print(f"Fetching file list from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not fetch the URL: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if not href:
            continue

        is_excluded = any(href.startswith(ex_dir) for ex_dir in exclude_dirs)
        is_parent_dir = 'Parent Directory' in a_tag.text
        is_directory = href.endswith('/')

        if not is_excluded and not is_parent_dir and not is_directory:
            links.append(f"{url}{href}")
            
    return links

def cleanup_incomplete_files(download_dir):
    """
    Removes incomplete .aria2 files to ensure downloads can resume safely or restart cleanly.
    """
    incomplete_files = glob.glob(f"{download_dir}/*.aria2")
    
    if incomplete_files:
        print(f"\nFound {len(incomplete_files)} incomplete downloads. Deleting them...")
        for file in incomplete_files:
            print(f"Deleting {file}...")
            os.remove(file)
        print("Incomplete files deleted. Proceeding with download.")
    else:
        print("\nNo incomplete downloads found. Proceeding with download.")

def download_files_with_aria2c(links, download_dir):
    """
    Downloads files from a list of URLs using aria2c, skipping already completed files.
    """
    if not links:
        print("No files found to download.")
        return

    os.makedirs(download_dir, exist_ok=True)

    link_file_path = os.path.join(download_dir, 'download_links.txt')
    with open(link_file_path, 'w') as f:
        for link in links:
            f.write(link + '\n')

    print(f"\nFound {len(links)} files to download.")
    print(f"Starting download with aria2c into '{download_dir}' directory.")
    print("Already downloaded files will be skipped.")

    command = [
        'aria2c', '-c', '-x', '16', '-s', '16', '-k', '1M',
        '--dir', download_dir, '-i', link_file_path
    ]

    try:
        subprocess.run(command, check=True)
        print("\n✅ Download complete.")
    except FileNotFoundError:
        print("\nError: 'aria2c' command not found. Please install it.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\nAn error occurred during download: {e}")
        sys.exit(1)
    finally:
        os.remove(link_file_path)

def verify_checksums(download_dir):
    """
    Verifies downloaded files using their .md5 checksum files.
    """
    print("\nStarting MD5 checksum verification...")
    original_cwd = os.getcwd()
    os.chdir(download_dir)

    md5_files = [f for f in os.listdir('.') if f.endswith('.md5')]
    if not md5_files:
        print("No .md5 files found for verification.")
        os.chdir(original_cwd)
        return

    all_ok = True
    for md5_file in md5_files:
        print(f"\nVerifying with '{md5_file}':")
        try:
            result = subprocess.run(['md5sum', '-c', md5_file], check=True, capture_output=True, text=True)
            print(result.stdout.strip())
            if "FAILED" in result.stdout:
                all_ok = False
        except FileNotFoundError:
            print("Error: 'md5sum' command not found. Cannot verify checksums.")
            os.chdir(original_cwd)
            return
        except subprocess.CalledProcessError as e:
            print(f"Checksum verification failed for '{md5_file}':")
            print(e.stdout.strip())
            print(e.stderr.strip())
            all_ok = False

    os.chdir(original_cwd)
    
    if all_ok:
        print("\n✅ All file checksums verified successfully!")
    else:
        print("\n❌ Some files failed checksum verification. Please review the logs.")

def main():
    base_url = "https://ftp.ncbi.nlm.nih.gov/blast/db/"
    exclude_list = ['FASTA/', 'cloud/', 'experimental/', 'v4/', 'v5/', 'README']
    download_directory = "ncbi_blast_db_files"

    links = get_download_links(base_url, exclude_list)

    cleanup_incomplete_files(download_directory)

    download_files_with_aria2c(links, download_directory)

    verify_checksums(download_directory)

    print(f"\nScript finished. All downloaded files are located in '{download_directory}'.")

if __name__ == "__main__":
    main()

