import urllib.request
import os
import time

FILES_BASE_URL = "https://raw.githubusercontent.com/bigalarmstudios/brang-applications/refs/heads/main/appFiles"
CATALOG_URL = "https://raw.githubusercontent.com/bigalarmstudios/brang-applications/refs/heads/main/catalougeAlone/catalogue.txt"

# Get the directory where THIS script sits (.../brang_os/programs)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Universal paths that work on any machine
CACHE_DIR = os.path.join(SCRIPT_DIR, "cache", "appstoreCache")
CACHE_FILE = os.path.join(CACHE_DIR, "catalogue_cache.txt")
APPS_DIR = os.path.join(SCRIPT_DIR, "installedApps")

def fetch_from_github(url):
    """Helper to download data from GitHub."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"\n[NETWORK ERROR] Failed to reach GitHub: {e}")
        return None

def get_catalog():
    """Loads catalog from local cache if valid (< 1 day old), otherwise downloads and updates cache."""
    one_day_in_seconds = 24 * 60 * 60
    
    # Check if a cache file exists and how old it is
    if os.path.exists(CACHE_FILE):
        file_age = time.time() - os.path.getmtime(CACHE_FILE)
        if file_age < one_day_in_seconds:
            print("Loading catalog from local cache...")
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return f.read()

    # If cache is missing or expired, pull a fresh one
    return refresh_catalog()

def refresh_catalog():
    """Forces a redownload of the catalog and overwrites the local cache file."""
    print("Fetching fresh catalog from GitHub...")
    raw_catalog = fetch_from_github(CATALOG_URL)
    
    if raw_catalog:
        # Save it into the universal cache directory
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            f.write(raw_catalog)
        print("✓ Local cache updated successfully.")
        return raw_catalog
    return None

def main():
    # Load catalog data (handling the 1-day rule automatically)
    raw_catalog = get_catalog()
    
    if not raw_catalog:
        print("Could not load catalog list. Please check your internet connection.")
        return

    # Clean the input data lines
    apps = [line.replace('\r', '') for line in raw_catalog.splitlines() if line.strip()]

    # STEP 2: Show the menu to the user
    print("\n--- AVAILABLE SCRIPTS ---")
    for idx, app in enumerate(apps, 1):
        print(f"{idx}. {app}")
    
    # Dynamic manual refresh option added to the end of the list
    refresh_option_num = len(apps) + 1
    print(f"{refresh_option_num}. [Refresh Catalog Data]")

    # STEP 3: Get user choice
    try:
        choice = int(input("\nSelect an option: "))
        if choice < 1 or choice > refresh_option_num:
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    # Action: Check if they chose the manual refresh button
    if choice == refresh_option_num:
        print("\nManually resetting cache...")
        if refresh_catalog():
            print("Done! Run the script again to see any new apps.")
        return

    # Action: Process an app download
    selected_script = apps[choice - 1]
    clean_script_name = selected_script.replace('\r', '').strip()
    file_extension = ".py"  
    target_url = f"{FILES_BASE_URL}/{clean_script_name}{file_extension}"
    
    print(f"\nFetching {clean_script_name}.py from: {target_url}...")
    script_contents = fetch_from_github(target_url)

    # STEP 5: Save the downloaded Python file to 'installedApps'
    if script_contents is not None:
        os.makedirs(APPS_DIR, exist_ok=True)
        local_filename = os.path.join(APPS_DIR, f"{clean_script_name}{file_extension}")
        
        with open(local_filename, "w", encoding="utf-8") as f:
            f.write(script_contents)
            
        print(f"✓ Success! Saved seamlessly to: {local_filename}")
    else:
        print(f"✗ Failed to download. Make sure '{clean_script_name}.py' exists inside your 'appFiles' folder on GitHub!")

if __name__ == "__main__":
    main()