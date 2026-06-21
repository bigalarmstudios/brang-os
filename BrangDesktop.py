import pygame
import os
import subprocess

# set everything up
pygame.init()
pygame.font.init()

# Assigned display to the 'screen' variable
screen = pygame.display.set_mode((1920, 1080))

# Get the directory of THIS desktop script to calculate paths cleanly
DESKTOP_DIR = os.path.dirname(os.path.abspath(__file__))
# Map the path to where fetchCatalogue.py lives relative to this file
FETCH_SCRIPT_PATH = os.path.join(DESKTOP_DIR, "programs", "fetchCatalogue.py")

# specify all the variables
admin_user_screen = [pygame.Rect(200, 300, 300, 300)]
extra_background_box = [pygame.Rect(210, 80, 1500, 900)]

# game states
desktop            = True
running            = True
storeOpened        = False

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

# SCALABLE APP SYSTEM WITH INSTALL CHECKS
apps_list = [
    {"name": "Big Alarm Store", "x": 250, "y": 120, "installed": True},
    {"name": "Chat App",        "x": 400, "y": 120, "installed": False},
    {"name": "File Explorer",   "x": 550, "y": 120, "installed": False},
    {"name": "Settings",        "x": 700, "y": 120, "installed": True}
]

def draw_app(screen, x, y, title):
    """Draws an icon, its borders, and its text dynamically at any X, Y position"""
    pygame.draw.rect(screen, APPSTORE_BLUE, (x, y, 100, 100))
    pygame.draw.rect(screen, APPEDGE, (x, y, 100, 10))        # Top
    pygame.draw.rect(screen, APPEDGE, (x, y, 10, 100))        # Left
    pygame.draw.rect(screen, APPEDGE, (x + 90, y, 10, 100))   # Right
    pygame.draw.rect(screen, APPEDGE, (x, y + 90, 100, 10))   # Bottom
    text_surface = font.render(title, True, WHITE)
    screen.blit(text_surface, (x, y + 110))

# Main game loop
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.center = (mouse_x, mouse_y)
    player.x = max(0, min(player.x, width - player_size))
    player.y = max(0, min(player.y, height - player_size))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ── LEFT MOUSE BUTTON DOWN ──────────────────────────────────────────
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if desktop:
                # Find the "Big Alarm Store" icon in your list
                for app in apps_list:
                    if app["name"] == "Big Alarm Store":
                        # Create a clickable boundary matching where draw_app draws it
                        store_rect = pygame.Rect(app["x"], app["y"], 100, 100)
                        if store_rect.collidepoint(mx, my):
                            storeOpened = True
                            desktop = False
                            
                            # ── LAUNCH THE EXTERNAL FETCH SCRIPT ──
                            print(f"[OS] Launching external catalog downloader at: {FETCH_SCRIPT_PATH}")
                            # This safely pops open a native terminal window to execute the script!
                            subprocess.Popen(["start", "cmd", "/c", "python", FETCH_SCRIPT_PATH], shell=True)
                            break
            
            elif storeOpened:
                # Simple back button click mapping (Click top left to go back to desktop)
                if pygame.Rect(20, 20, 100, 50).collidepoint(mx, my):
                    desktop = True
                    storeOpened = False

    # Drawing Canvas
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
        
        screen.blit(appslist_font.render("Terminal store window opened!", True, WHITE), (100, 150))
        screen.blit(appslist_font.render("Look at your command line to select downloads.", True, WHITE), (100, 200))
    
    pygame.display.flip()

pygame.quit()