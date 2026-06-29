import pygame
import os
import subprocess
import urllib.request
import importlib.util
import tkinter as tk
from tkinter import messagebox

# set everything up
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1920, 1080))

DESKTOP_DIR = os.path.dirname(os.path.abspath(__file__))
FETCH_SCRIPT_PATH = os.path.join(DESKTOP_DIR, "programs", "fetchCatalogue.py")
APPS_DIR = os.path.join(DESKTOP_DIR, "programs", "installedApps")
HANDOVER_FILE = os.path.join(DESKTOP_DIR, "programs", "cache", "app_handover.txt")

CATALOG_URL = "https://raw.githubusercontent.com/bigalarmstudios/brang-applications/refs/heads/main/catalougeAlone/catalogue.txt"

admin_user_screen = [pygame.Rect(200, 300, 300, 300)]
extra_background_box = [pygame.Rect(210, 80, 1500, 900)]
appstore_openagain_box = [pygame.Rect(1150, 85, 100, 100)]

desktop            = True
running            = True
storeOpened        = False
active_app         = None

font = pygame.font.SysFont('Arial', 24)
appslist_font = pygame.font.SysFont('Arial', 20)

WHITE  = (255, 255, 255)
BLUE   = (0, 0, 255)
GREEN  = (0, 255, 0)
ORANGE = (255, 165, 0)
RED    = (255, 0, 0)
LIGHT_BLUE = (45, 210, 255)
APPSTORE_BLUE = (52, 199, 255)
APPEDGE = (150, 150, 150)

width, height = 1920, 1080

player_size = 50
player = pygame.Rect(
    width // 2 - player_size // 2,
    height // 2 - player_size // 2,
    player_size,
    player_size
)

pygame.display.set_caption("Brang OS")

def fetch_catalog_from_github():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(CATALOG_URL, headers=headers)
    try:
        print("[OS] Contacting GitHub to fetch catalog names...")
        with urllib.request.urlopen(req) as response:
            raw_data = response.read().decode('utf-8')
            return [line.replace('\r', '').strip() for line in raw_data.splitlines() if line.strip()]
    except Exception as e:
        print(f"[OS NETWORK ERROR] Failed to reach GitHub catalog: {e}")
        return []

def initialize_apps_list():
    built_in_apps = [
        {"name": "Big Alarm Store", "x": 250, "y": 120, "installed": True}
    ]
    remote_apps = fetch_catalog_from_github()
    start_x, start_y = 400, 120
    spacing_x = 150
    max_x = 1600
    current_x = start_x
    current_y = start_y
    
    for app_line in remote_apps:
        if ',' in app_line:
            app_name, _ = app_line.split(',', 1)
            app_name = app_name.strip()
        else:
            app_name = app_line.strip()
            
        if app_name.lower() == "big alarm store":
            continue
            
        local_file_path = os.path.join(APPS_DIR, f"{app_name}.py")
        is_installed = os.path.exists(local_file_path)
        
        app_entry = {
            "name": app_name,
            "x": current_x,
            "y": current_y,
            "installed": is_installed
        }
        built_in_apps.append(app_entry)
        current_x += spacing_x
        if current_x > max_x:
            current_x = 250
            current_y += 180
    return built_in_apps

apps_list = initialize_apps_list()

def check_installed_apps():
    if not os.path.exists(APPS_DIR):
        return
    for filename in os.listdir(APPS_DIR):
        if filename.endswith(".py"):
            app_name = filename[:-3]
            already_tracked = False
            for app in apps_list:
                if app["name"].lower() == app_name.lower():
                    app["installed"] = True
                    already_tracked = True
                    break
            if not already_tracked:
                next_x = 250 + (len([a for a in apps_list if a["installed"]]) * 150)
                next_y = 120
                if next_x > 1600: 
                    next_x = 250 + ((len(apps_list) % 8) * 150)
                    next_y = 300
                new_app = {"name": app_name, "x": next_x, "y": next_y, "installed": True}
                apps_list.append(new_app)

def launch_app_by_name(app_name, argument=None):
    global active_app, desktop, storeOpened
    app_file_path = os.path.join(APPS_DIR, f"{app_name}.py")
    if os.path.exists(app_file_path):
        try:
            spec = importlib.util.spec_from_file_location(app_name, app_file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if argument and hasattr(module, "load_file"):
                module.load_file(argument)
                
            active_app = module
            desktop = False
            storeOpened = False
            print(f"[OS] Successfully booted {app_name}")
            return True
        except Exception as e:
            print(f"[OS] Error initializing app script: {e}")
    else:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        messagebox.showerror("App Error", f"The application '{app_name}' is not installed! Download it from the store first.")
        root.destroy()
    return False

def check_app_handover():
    if os.path.exists(HANDOVER_FILE):
        try:
            with open(HANDOVER_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
            os.remove(HANDOVER_FILE)
            
            if "|" in content:
                target_app, file_argument = content.split("|", 1)
                launch_app_by_name(target_app, file_argument)
        except Exception as e:
            print(f"[OS HANDOVER ERROR] {e}")

def draw_app(screen, x, y, title):
    pygame.draw.rect(screen, APPSTORE_BLUE, (x, y, 100, 100))
    pygame.draw.rect(screen, APPEDGE, (x, y, 10, 100))
    pygame.draw.rect(screen, APPEDGE, (x, y, 100, 10))
    pygame.draw.rect(screen, APPEDGE, (x + 90, y, 10, 100))
    pygame.draw.rect(screen, APPEDGE, (x, y + 90, 100, 10))
    
    display_title = title if len(title) <= 12 else title[:10] + ".."
    text_surface = font.render(display_title, True, WHITE)
    screen.blit(text_surface, (x, y + 110))

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.center = (mouse_x, mouse_y)
    player.x = max(0, min(player.x, width - player_size))
    player.y = max(0, min(player.y, height - player_size))

    if desktop:
        check_installed_apps()
        
    check_app_handover()

    events = pygame.event.get()
    
    # ── NEW INTERCEPT SYSTEM: SCAN FOR SUB-APP HANDOVER NOTIFICATIONS ──
    for event in events:
        if event.type == pygame.USEREVENT and getattr(event, "action", "") == "exit_to_explorer":
            print("[OS Handover Alert] Swapping textEditor out for fileExplorer...")
            launch_app_by_name("fileExplorer", "SAVE_AS_MODE")
            break

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if desktop:
                for app in apps_list:
                    if app["installed"]:
                        store_rect = pygame.Rect(app["x"], app["y"], 100, 100)
                        if store_rect.collidepoint(mx, my):
                            if app["name"] == "Big Alarm Store":
                                storeOpened = True
                                desktop = False
                                subprocess.Popen(["start", "cmd", "/c", "python", FETCH_SCRIPT_PATH], shell=True)
                            else:
                                launch_app_by_name(app["name"])
                            break
            
            elif storeOpened:
                if pygame.Rect(20, 20, 100, 50).collidepoint(mx, my):
                    desktop = True
                    storeOpened = False
                    
            elif active_app is not None:
                if pygame.Rect(1800, 20, 100, 50).collidepoint(mx, my):
                    active_app = None
                    desktop = True

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
        pygame.draw.rect(screen, RED, (20, 20, 100, 50))
        screen.blit(font.render("Back", True, WHITE), (45, 30))
        screen.blit(appslist_font.render("Please wait... The selection menu is starting.", True, WHITE), (100, 150))
        pygame.draw.rect(screen, WHITE, appstore_openagain_box[0])
        screen.blit(appslist_font.render("Open Store Again", True, WHITE), (1300, 120))
        pygame.draw.rect(screen, BLUE, player)
        
    elif active_app is not None:
        try:
            screen.fill(BLUE)
            pygame.draw.rect(screen, LIGHT_BLUE, extra_background_box[0])
            if hasattr(active_app, "update"):
                active_app.update(events)
            active_app.render(screen)
            pygame.draw.rect(screen, RED, (1800, 20, 100, 50))
            screen.blit(font.render("Exit", True, WHITE), (1830, 31))
            pygame.draw.rect(screen, BLUE, player)
        except Exception as e:
            print(f"[OS] App crashed during loop execution: {e}")
            active_app = None
            desktop = True
    
    pygame.display.flip()

pygame.quit()