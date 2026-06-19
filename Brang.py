import pygame
import random

pygame.init()
pygame.font.init()

# ─── Setup “boxes” and fonts/colors ─────────────────────────────────────────
# Positions and sizes are identical to your original.
admin_user_screen = [pygame.Rect(200, 300, 300, 300)]
start_box        = [pygame.Rect(1150, 90, 100, 100)]
start_back_box = [pygame.Rect(1150, 340, 100, 100)]
start_manual_box = [pygame.Rect(1150, 220, 100, 100)]

# Fonts (same as before)
font       = pygame.font.SysFont('Arial', 120)
font_admin = pygame.font.SysFont('Arial', 50)

# Colors
WHITE  = (255, 255, 255)
BLUE   = (0, 0, 255)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)

# Window size
width, height = 1920, 1080

# ─── Player setup ────────────────────────────────────────────────────────────
player_size = 50
player = pygame.Rect(
    width // 2 - player_size // 2,
    height // 2 - player_size // 2,
    player_size,
    player_size
)

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Brang (Mouse‐Follow Version)")

# ─── Game states ─────────────────────────────────────────────────────────────
login               = True   # Start on “login” screen
running             = True
admin_start_confirm = False  # Moves to admin screen once Admin‐box is clicked
admin_wallpaper     = False  # Fires admin_wallpaper_def() once

# ─── Placeholder function for “Start” click ─────────────────────────────────
def admin_wallpaper_def():
    print("Admin wallpaper activated!")  # Replace with your real wallpaper logic

# ─── Main loop ───────────────────────────────────────────────────────────────
while running:
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

            elif admin_start_confirm:
                # If clicked inside the green “Start” box → call wallpaper once
                for sb in start_box:
                    if sb.collidepoint(mx, my):
                        admin_wallpaper = True
                        break

                # If clicked inside the blue “Back” box → go back to login screen
                for bb in start_back_box:
                    if bb.collidepoint(mx, my):
                        admin_start_confirm = False
                        login = True
                        break

    # ── MAKE PLAYER FOLLOW THE MOUSE ────────────────────────────────────────
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.center = (mouse_x, mouse_y)

    # ── CLAMP player INSIDE WINDOW BOUNDS ──────────────────────────────────
    player.x = max(0, min(player.x, width - player_size))
    player.y = max(0, min(player.y, height - player_size))

    # ── DRAWING ──────────────────────────────────────────────────────────────
    if login:
        screen.fill(WHITE)
        screen.blit(font.render("log in", True, GREEN), (850, 60))

        # Draw player square (blue)
        pygame.draw.rect(screen, BLUE, player)

        # Draw red Admin box + label
        for admin_for in admin_user_screen:
            pygame.draw.rect(screen, RED, admin_for)
            admin_text = font_admin.render("Admin", True, BLUE)
            # Position “Admin” text inside the red box
            screen.blit(admin_text, (admin_for.x + 50, admin_for.y + 200))

    elif admin_start_confirm:
        screen.fill(BLUE)
        # Draw cursor
        pygame.draw.rect(screen, WHITE, player)

        # Draw text
        screen.blit(font.render("start", True, GREEN), (700, 80))
        screen.blit(font.render("manual", True, GREEN), (700, 200))
        screen.blit(font.render("back", True, GREEN), (700, 330))

        # Draw the boxes
        for sb in start_box:
            pygame.draw.rect(screen, GREEN, sb)
        # Draw blue Back box
        for bb in start_back_box:
            pygame.draw.rect(screen, RED, bb)
        for mb in start_manual_box:
            pygame.draw.rect(screen, GREEN, mb)

    # If “Start” was clicked, fire admin_wallpaper_def() once
    if admin_wallpaper:
        admin_wallpaper_def()
        admin_wallpaper = False  # Ensure it prints only one time per click

    pygame.display.flip()

pygame.quit()
