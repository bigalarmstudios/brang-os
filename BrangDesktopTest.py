import pygame
import random


# set everything up
pygame.init()
pygame.font.init()

# FIX 1: Assigned display to the 'screen' variable
screen = pygame.display.set_mode((1920, 1080))

# specify all the variables
admin_user_screen = [pygame.Rect(200, 300, 300, 300)]

# game states
login               = True   # Start on “login” screen

# Fonts
font = pygame.font.SysFont('Arial', 120)
font_admin = pygame.font.SysFont('Arial', 50)
font_manual_text = pygame.font.SysFont('Arial', 30)

# Colors
WHITE  = (255, 255, 255)
BLUE   = (0, 0, 255)
GREEN  = (0, 255, 0)
ORANGE = (255, 165, 0)
RED    = (255, 0, 0)

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

# The main script
while running:
    # FIX 2: Moved player mouse-tracking INSIDE the loop so it actually moves dynamically
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

            if login:
                # If clicked inside the red “Admin” box → go to admin screen
                for admin_for in admin_user_screen:
                    if admin_for.collidepoint(mx, my):
                        admin_start_confirm = True
                        login = False
                        break

    # drawing
    if login:
        screen.fill(WHITE)
        screen.blit(font.render("log in", True, GREEN), (850, 60))

        pygame.draw.rect(screen, BLUE, player)
    
    pygame.display.flip()

pygame.quit()