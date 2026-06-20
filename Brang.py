import pygame
import random

pygame.init()
pygame.font.init()

# ─── Setup “boxes” and fonts/colors ─────────────────────────────────────────
# Positions and sizes are identical to your original.
admin_user_screen = [pygame.Rect(200, 300, 300, 300)]
start_box        = [pygame.Rect(1150, 90, 100, 100)]
start_back_box = [pygame.Rect(1150, 340, 100, 100)]
start_manual_box = [pygame.Rect(1150, 210, 100, 100)]

# Fonts (same as before)
font       = pygame.font.SysFont('Arial', 120)
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
manual_screen       = False  # Placeholder for future manual screen state

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
                # clicking desktop
                for sb in start_box:
                    if sb.collidepoint(mx, my):
                        admin_wallpaper = True
                        break

                # clicking back
                for bb in start_back_box:
                    if bb.collidepoint(mx, my):
                        admin_start_confirm = False
                        login = True
                        break
                
                for mb in start_manual_box:
                    if mb.collidepoint(mx, my):
                        manual_screen = True  # Placeholder for future manual screen logic
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

        # Draw red Admin box + label
        for admin_for in admin_user_screen:
            pygame.draw.rect(screen, RED, admin_for)
            admin_text = font_admin.render("Admin", True, BLUE)
            # Position “Admin” text inside the red box
            screen.blit(admin_text, (admin_for.x + 50, admin_for.y + 200))

        pygame.draw.rect(screen, BLUE, player)

    elif admin_start_confirm:
        screen.fill(BLUE)

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

        pygame.draw.rect(screen, WHITE, player)

    # If “Start” was clicked, fire admin_wallpaper_def() once
    if admin_wallpaper:
        admin_wallpaper_def()
        admin_wallpaper = False  # Ensure it prints only one time per click
    
    if manual_screen:
        screen.fill(BLUE)
        screen.blit(font.render("manual", True, GREEN), (750, 20))
        # the manual text
        manual_text = [
            "Welcome to the Brang Os!",
            "1. Click 'Admin' to access admin features.",
            "2. Click 'Start' to activate the admin wallpaper.",
            "3. Click 'Back' to return to the login screen.",
            "4. Move your mouse to control the player square.",
            "5. Enjoy exploring the game!"
        ]
        screen.blit(font_manual_text.render(manual_text[0], True, GREEN), (100, 100))
        screen.blit(font_manual_text.render(manual_text[1], True, GREEN), (100, 150))
        screen.blit(font_manual_text.render(manual_text[2], True, GREEN), (100, 200))
        screen.blit(font_manual_text.render(manual_text[3], True, GREEN), (100, 250))
        screen.blit(font_manual_text.render(manual_text[4], True, GREEN), (100, 300))
        screen.blit(font_manual_text.render(manual_text[5], True, GREEN), (100, 350))

        pygame.draw.rect(screen, WHITE, player)
    pygame.display.flip()

pygame.quit()
