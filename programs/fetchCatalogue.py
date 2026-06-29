import urllib.request
import os
import time
import ast

FILES_BASE_URL = "https://raw.githubusercontent.com/bigalarmstudios/brang-applications/refs/heads/main/appFiles"
CATALOG_URL = "https://raw.githubusercontent.com/bigalarmstudios/brang-applications/refs/heads/main/catalougeAlone/catalogue.txt"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(SCRIPT_DIR, "cache", "appstoreCache")
CACHE_FILE = os.path.join(CACHE_DIR, "catalogue_cache.txt")
APPS_DIR = os.path.join(SCRIPT_DIR, "installedApps")

def fetch_from_github(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    bypass_url = f"{url}?t={int(time.time())}"
    req = urllib.request.Request(bypass_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"\n[NETWORK ERROR] Failed to reach GitHub: {e}")
        return None

def parse_catalog(content):
    apps_dict = {}
    if not content:
        return apps_dict
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if ',' in line:
            name, version = line.split(',', 1)
            apps_dict[name.strip()] = version.strip()
        else:
            apps_dict[line.strip()] = "1.0"
    return apps_dict

def get_local_app_version(app_name):
    """Safely extracts __version__ from the .py file without running it."""
    file_path = os.path.join(APPS_DIR, f"{app_name}.py")
    if not os.path.exists(file_path):
        return "0.0"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            node = ast.parse(f.read(), filename=file_path)
            for body_item in node.body:
                if isinstance(body_item, ast.Assign):
                    for target in body_item.targets:
                        if isinstance(target, ast.Name) and target.id == "__version__":
                            if isinstance(body_item.value, ast.Constant):
                                return str(body_item.value.value)
                            elif isinstance(body_item.value, ast.Num):
                                return str(body_item.value.n)
                            elif isinstance(body_item.value, ast.Str):
                                return str(body_item.value.s)
    except Exception:
        pass
    return "1.0"

def save_local_cache(apps_dict):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        for name, version in apps_dict.items():
            f.write(f"{name},{version}\n")

def is_newer(remote_ver, local_ver):
    try:
        remote_parts = [int(x) for x in remote_ver.split('.')]
        local_parts = [int(x) for x in local_ver.split('.')]
        max_len = max(len(remote_parts), len(local_parts))
        remote_parts += [0] * (max_len - len(remote_parts))
        local_parts += [0] * (max_len - len(local_parts))
        return remote_parts > local_parts
    except ValueError:
        return remote_ver > local_ver

def get_catalog():
    one_day_in_seconds = 24 * 60 * 60
    if os.path.exists(CACHE_FILE):
        file_age = time.time() - os.path.getmtime(CACHE_FILE)
        if file_age < one_day_in_seconds:
            print("Loading catalog...")
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return f.read()
    return refresh_catalog()

def refresh_catalog():
    print("Fetching catalogue...")
    raw_catalog = fetch_from_github(CATALOG_URL)
    if raw_catalog:
        remote_apps = parse_catalog(raw_catalog)
        save_local_cache(remote_apps)
        print("✓ Catalog updated successfully!")
        return raw_catalog
    return None

def download_app(app_name):
    """Helper to perform individual app download operations."""
    file_extension = ".py"  
    target_url = f"{FILES_BASE_URL}/{app_name}{file_extension}"
    print(f"Fetching {app_name}.py from: {target_url}...")
    script_contents = fetch_from_github(target_url)

    if script_contents is not None:
        os.makedirs(APPS_DIR, exist_ok=True)
        local_filename = os.path.join(APPS_DIR, f"{app_name}{file_extension}")
        with open(local_filename, "w", encoding="utf-8") as f:
            f.write(script_contents)
        print(f"✓ [{app_name}] successfully updated/installed!")
        return True
    else:
        print(f"✗ Failed to download [{app_name}].")
        return False

def main():
    while True: # Infinite loop allows refresh cycles to re-render the app list automatically
        raw_catalog = get_catalog()
        if not raw_catalog:
            print("Could not load catalog list. Please check internet connection.")
            return

        apps = [line.replace('\r', '').strip() for line in raw_catalog.splitlines() if line.strip()]

        print("\n--- AVAILABLE SCRIPTS ---")
        for idx, app_line in enumerate(apps, 1):
            if ',' in app_line:
                name, _ = app_line.split(',', 1)
                name = name.strip()
            else:
                name = app_line.strip()
            print(f"{idx}. {name}")
        
        refresh_option_num = len(apps) + 1
        print(f"{refresh_option_num}. [Refresh Catalog Data]")

        # Scan for outdated files
        outdated_apps = []
        for app_line in apps:
            if ',' in app_line:
                name, remote_version = app_line.split(',', 1)
                name = name.strip()
                remote_version = remote_version.strip()
            else:
                name = app_line.strip()
                remote_version = "1.0"
                
            local_file_path = os.path.join(APPS_DIR, f"{name}.py")
            if os.path.exists(local_file_path):
                current_version = get_local_app_version(name)
                if is_newer(remote_version, current_version):
                    print(f"🌟 [{name}] has a newer update available! {current_version} -> {remote_version}")
                    outdated_apps.append(name)

        # ── NEW FEATURE: "TO UPDATE ALL, PRESS ENTER!" ALERT ──
        if outdated_apps:
            print("\n👉 To update all, press enter!")

        user_input = input("\nSelect a number: ").strip()

        # Handle the "Update All" shortcut trigger
        if user_input == "" and outdated_apps:
            print(f"\n🔄 Updating all {len(outdated_apps)} apps...")
            for app_to_update in outdated_apps:
                download_app(app_to_update)
            print("\n All updates completed successfully!")
            
            # ── NEW FEATURE: FORCE SYSTEM RE-FETCH LOOP ──
            print("Refreshing catalogue UI...")
            refresh_catalog()
            continue # Loops back up to display the fresh values

        # Process standard numeric selections
        try:
            choice = int(user_input)
            if choice < 1 or choice > refresh_option_num:
                print("Invalid selection.")
                input("\nPress enter to continue...")
                continue
        except ValueError:
            print("Please enter a valid number.")
            input("\nPress enter to continue...")
            continue

        if choice == refresh_option_num:
            print("\nManually resetting cache...")
            refresh_catalog()
            continue

        selected_line = apps[choice - 1]
        if ',' in selected_line:
            clean_script_name, _ = selected_line.split(',', 1)
            clean_script_name = clean_script_name.strip()
        else:
            clean_script_name = selected_line.strip()
            
        print("")
        if download_app(clean_script_name):
            input("\nPress enter to finish.")
            break
        else:
            input("\nPress enter to return.")
            break

if __name__ == "__main__":
    main()