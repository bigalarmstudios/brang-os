import pygame
import os
import subprocess
import urllib.request  # Added to download catalog directly from GitHub
import importlib.util

# set everything up
pygame.init()
pygame.font.init()

# Assigned display to the 'screen' variable
screen = pygame.display.set_mode((1920, 1080))

# Get the directory of THIS desktop script to calculate paths cleanly
DESKTOP_DIR = os.path.dirname(os.path.abspath(__file__))
# Map the path to where fetchCatalogue.py lives relative to this file
FETCH_SCRIPT_PATH = os.path.join(DESKTOP_DIR, "programs", "fetchCatalogue.py")
APPS_DIR = os.path.join(DESKTOP_DIR, "programs", "installedApps")

# GitHub URL Configuration from fetchCatalogue
CATALOG_URL = "https://raw.githubusercontent.com/bigalarmstudios/brang-applications/refs/heads/main/catalougeAlone/catalogue.txt"

# specify all the variables
admin_user_screen = [pygame.Rect(200, 300, 300, 300)]
extra_background_box = [pygame.Rect(210, 80, 1500, 900)]
appstore_openagain_box = [pygame.Rect(1150, 85, 100, 100)]

# game states
desktop            = True
running            = True
storeOpened        = False
active_app         = None  # Tracks the currently active module running inside the desktop

# Fonts
font = pygame.font.SysFont('Arial', 24)
appslist_font = pygame.font.SysFont('Arial', 20)

# Colors
WHITE  = (255, 255, 255)
BLUE   = (0, 0, 255)
GREEN  = (0, 255, 0)
ORANGE = (255, 165, 0)
RED    = (255, 0, 0)
LIGHT_BLUE = (45, 210, 255)
APPSTORE_BLUE = (52, 199, 255)
APPEDGE = (150, 150, 150)

# Window size
width, height = 1920, 1080

# player setup
player_size = 50
player = pygame.Rect(
    width // 2 - player_size // 2,
    height // 2 - player_size // 2,
    player_size,
    player_size
)

pygame.display.set_caption("Brang OS")

def fetch_catalog_from_github():
    """Pulls the raw catalogue.txt from GitHub to build our initial app list."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(CATALOG_URL, headers=headers)
    try:
        print("[OS] Contacting GitHub to fetch catalog names...")
        with urllib.request.urlopen(req) as response:
            raw_data = response.read().decode('utf-8')
            # Clean and split lines, ignoring empty rows
            return [line.replace('\r', '').strip() for line in raw_data.splitlines() if line.strip()]
    except Exception as e:
        print(f"[OS NETWORK ERROR] Failed to reach GitHub catalog: {e}")
        return []

def initialize_apps_list():
    """Builds the initial apps_list structure dynamically from GitHub metadata."""
    # Start with the built-in system store application
    built_in_apps = [
        {"name": "Big Alarm Store", "x": 250, "y": 120, "installed": True}
    ]
    
    # Fetch remaining available apps from the repository
    remote_apps = fetch_catalog_from_github()
    
    # Grid positioning parameters
    start_x, start_y = 400, 120  # Start standard apps at X=400 since Store takes X=250
    spacing_x = 150
    max_x = 1600
    
    current_x = start_x
    current_y = start_y
    
    for app_name in remote_apps:
        # Avoid duplicating the store if it's accidentally added to the catalog file
        if app_name.lower() == "big alarm store":
            continue
            
        # Check if this app is already physically downloaded locally
        local_file_path = os.path.join(APPS_DIR, f"{app_name}.py")
        is_installed = os.path.exists(local_file_path)
        
        # Build app dictionary element
        app_entry = {
            "name": app_name,
            "x": current_x,
            "y": current_y,
            "installed": is_installed
        }
        built_in_apps.append(app_entry)
        
        # Increment icon positioning coordinates
        current_x += spacing_x
        if current_x > max_x:
            current_x = 250
            current_y += 180  # Wrap down cleanly to a new row below text labels

    return built_in_apps

# INITIALIZE DYNAMIC APPS LIST ON BOOT
apps_list = initialize_apps_list()

def check_installed_apps():
    """Scans the installedApps folder and updates installation flags dynamically."""
    if not os.path.exists(APPS_DIR):
        return

    for filename in os.listdir(APPS_DIR):
        if filename.endswith(".py"):
            app_name = filename[:-3] # Strip out the ".py" extension
            
            # Check if this app is already known in our list
            already_tracked = False
            for app in apps_list:
                if app["name"].lower() == app_name.lower():
                    app["installed"] = True
                    already_tracked = True
                    break
            
            # If it's a completely brand new app downloaded, auto-calculate an X position for it
            if not already_tracked:
                # Find the next open slot on the X axis (spaced by 150 pixels)
                next_x = 250 + (len([a for a in apps_list if a["installed"]]) * 150)
                # Simple boundary check to wrap down to a second row if it exceeds screen width
                next_y = 120
                if next_x > 1600: 
                    next_x = 250 + ((len(apps_list) % 8) * 150)
                    next_y = 300
                
                new_app = {"name": app_name, "x": next_x, "y": next_y, "installed": True}
                apps_list.append(new_app)
                print(f"[OS] Detected new installed app: {app_name}, added to desktop.")

def draw_app(screen, x, y, title):
    """Draws an icon, its borders, and its text dynamically at any X, Y position"""
    pygame.draw.rect(screen, APPSTORE_BLUE, (x, y, 100, 100))
    pygame.draw.rect(screen, APPEDGE, (x, y, 100, 10))        # Top
    pygame.draw.rect(screen, APPEDGE, (x, y, 10, 100))        # Left
    pygame.draw.rect(screen, APPEDGE, (x + 90, y, 10, 100))   # Right
    pygame.draw.rect(screen, APPEDGE, (x, y + 90, 100, 10))   # Bottom
    
    # Simple formatting: if name is too long, truncate it for the desktop UI
    display_title = title if len(title) <= 12 else title[:10] + ".."
    text_surface = font.render(display_title, True, WHITE)
    screen.blit(text_surface, (x, y + 110))

# Main game loop
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.center = (mouse_x, mouse_y)
    player.x = max(0, min(player.x, width - player_size))
    player.y = max(0, min(player.y, height - player_size))

    # Real-time check: Constantly check directory updates while running
    if desktop:
        check_installed_apps()

    # Capture Pygame events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # ── LEFT MOUSE BUTTON DOWN ──────────────────────────────────────────
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if desktop:
                # Find if ANY installed app is clicked
                for app in apps_list:
                    if app["installed"]:
                        store_rect = pygame.Rect(app["x"], app["y"], 100, 100)
                        if store_rect.collidepoint(mx, my):
                            if app["name"] == "Big Alarm Store":
                                storeOpened = True
                                desktop = False
                                print(f"[OS] Launching external catalog downloader at: {FETCH_SCRIPT_PATH}")
                                subprocess.Popen(["start", "cmd", "/c", "python", FETCH_SCRIPT_PATH], shell=True)
                            else:
                                print(f"[OS] Loading downloaded app internally: {app['name']}")
                                app_file_path = os.path.join(APPS_DIR, f"{app['name']}.py")
                                if os.path.exists(app_file_path):
                                    try:
                                        # Import module on-the-fly
                                        spec = importlib.util.spec_from_file_location(app["name"], app_file_path)
                                        module = importlib.util.module_from_spec(spec)
                                        spec.loader.exec_module(module)
                                        
                                        # Handoff window control to this module
                                        active_app = module
                                        desktop = False
                                    except Exception as e:
                                        print(f"[OS] Error initializing app script: {e}")
                                else:
                                    print(f"[OS] Error: File missing at {app_file_path}")
                            break
            
            elif storeOpened:
                # Simple back button click mapping (Click top left to go back to desktop)
                if pygame.Rect(20, 20, 100, 50).collidepoint(mx, my):
                    desktop = True
                    storeOpened = False
                    
            elif active_app is not None:
                # Check if the universal "Exit App" button was clicked
                if pygame.Rect(1800, 20, 100, 50).collidepoint(mx, my):
                    active_app = None
                    desktop = True

    # Drawing & Core App Engine Processing
    if desktop:
        screen.fill(BLUE)
        pygame.draw.rect(screen, LIGHT_BLUE, extra_background_box[0])
        
        for app in apps_list:
            if app["installed"]:
                draw_app(screen, app["x"], app["y"], app["name"])

        pygame.draw.rect(screen, BLUE, player)
    
    elif storeOpened:
        screen.fill(APPSTORE_BLUE)
        screen.blit(font.render("Big Alarm Store", True, WHITE), (850, 60))
        
        # Draw a quick back button interface
        pygame.draw.rect(screen, RED, (20, 20, 100, 50))
        screen.blit(font.render("Back", True, WHITE), (45, 30))
        
        screen.blit(appslist_font.render("Please wait... The selection menu is starting.", True, WHITE), (100, 150))
        pygame.draw.rect(screen, WHITE, appstore_openagain_box[0])
        screen.blit(appslist_font.render("Open Store Again", True, WHITE), (1300, 120))

        pygame.draw.rect(screen, BLUE, player)
        
    elif active_app is not None:
        try:
            # ── RE-DRAW BACKGROUND AND APPS SO CURSOR TRAILS GET ERASED ──
            screen.fill(BLUE)
            pygame.draw.rect(screen, LIGHT_BLUE, extra_background_box[0])
            
            # Let the custom downloaded app process events and draw onto the core surface
            if hasattr(active_app, "update"):
                active_app.update(events)
            
            active_app.render(screen)
            
            # Render a unified floating 'Close App' UI on top
            pygame.draw.rect(screen, RED, (1800, 20, 100, 50))
            screen.blit(font.render("Exit", True, WHITE), (1830, 31))
            
            # Render cursor cleanly over the active app window
            pygame.draw.rect(screen, BLUE, player)
        except Exception as e:
            print(f"[OS] App crashed during loop execution: {e}")
            active_app = None
            desktop = True
    
    pygame.display.flip()

pygame.quit()