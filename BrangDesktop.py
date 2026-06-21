import pygame
import random

# set everything up
pygame.init()
pygame.font.init()

# Assigned display to the 'screen' variable
screen = pygame.display.set_mode((1920, 1080))

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


# ── SCALABLE APP SYSTEM WITH INSTALL CHECKS ──────────────────────────────
# We've added an "installed" key. 
# Only apps set to True will render on the desktop canvas.
apps_list = [
    {"name": "Big Alarm Store", "x": 250, "y": 120, "installed": True},  # Store is pre-installed
    {"name": "Chat App",        "x": 400, "y": 120, "installed": False}, # Waiting for download script
    {"name": "File Explorer",   "x": 550, "y": 120, "installed": False}, # Waiting for download script
    {"name": "Settings",        "x": 700, "y": 120, "installed": True}   # Settings is pre-installed
]

def draw_app(screen, x, y, title):
    """Draws an icon, its borders, and its text dynamically at any X, Y position"""
    # Draw main icon box
    pygame.draw.rect(screen, APPSTORE_BLUE, (x, y, 100, 100))
    
    # Draw app borders relative to the starting x and y
    pygame.draw.rect(screen, APPEDGE, (x, y, 100, 10))        # Top
    pygame.draw.rect(screen, APPEDGE, (x, y, 10, 100))        # Left
    pygame.draw.rect(screen, APPEDGE, (x + 90, y, 10, 100))   # Right
    pygame.draw.rect(screen, APPEDGE, (x, y + 90, 100, 10))   # Bottom
    
    # Draw text right below the icon
    text_surface = font.render(title, True, WHITE)
    screen.blit(text_surface, (x, y + 110))
# ─────────────────────────────────────────────────────────────────────────


# The main script
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
                for appstore in appstore:
                    if appstore.collidepoint(mx, my):
                        storeOpened = True
                        desktop = False
                        break

    # drawing
    if desktop:
        screen.fill(BLUE)
        pygame.draw.rect(screen, LIGHT_BLUE, extra_background_box[0])
        
        # Loop through our app list and ONLY render them if installed is True
        for app in apps_list:
            if app["installed"]:
                draw_app(screen, app["x"], app["y"], app["name"])

        pygame.draw.rect(screen, BLUE, player)
    
    elif storeOpened:
        appliststatus = "Fetching"
        screen.fill(APPSTORE_BLUE)
        screen.blit(font.render("Big Alarm Store", True, WHITE), (850, 60))
        screen.blit(appslist_font.render("Available Apps:", True, WHITE), (100, 150))
        screen.blit(appslist_font.render(appliststatus, True, WHITE), (100, 200))
    
    pygame.display.flip()

pygame.quit()