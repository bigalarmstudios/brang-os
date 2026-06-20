import pygame
import os
import sys
import requests

# 1. Setup Pygame
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1280, 720))  # Slightly smaller for easy testing
pygame.display.set_caption("Brang OS")
clock = pygame.time.Clock()

# 2. Setup Fonts & Colors
font_small = pygame.font.SysFont('Arial', 18)
font_title = pygame.font.SysFont('Arial', 16, bold=True)

WHITE     = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY  = (60, 60, 60)
BLUE      = (30, 100, 200)
TITLE_BLUE = (45, 120, 230)
RED       = (220, 50, 50)
YELLOW    = (240, 200, 40)
BLACK     = (0, 0, 0)

# 3. Choose Folder to Scan
# '.' means the current folder where this script is saved.
TARGET_FOLDER = 'downloads' 
try:
    file_list = os.listdir(TARGET_FOLDER)
except Exception as e:
    file_list = ["Error reading directory"]

# 4. Desktop Variables
folder_icon_rect = pygame.Rect(50, 50, 70, 70)
last_click_time = 0
double_click_threshold = 300 # Milliseconds to register a double-click

# 5. Window State Variables
window_open = False
window_rect = pygame.Rect(300, 200, 450, 300)
title_bar_height = 30
is_dragging = False
drag_offset_x = 0
drag_offset_y = 0

# Close Button bounds (relative to the window positions)
close_btn_width = 35

# Main Loop
running = True
while running:
    mx, my = pygame.mouse.get_pos()
    
    # Title bar calculation changes dynamically as window moves
    title_bar_rect = pygame.Rect(window_rect.x, window_rect.y, window_rect.width, title_bar_height)
    close_btn_rect = pygame.Rect(window_rect.right - close_btn_width - 5, window_rect.y + 4, close_btn_width, title_bar_height - 8)

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            # --- FOLDER ICON INTERACTION ---
            if folder_icon_rect.collidepoint(mx, my):
                current_time = pygame.time.get_ticks()
                if current_time - last_click_time < double_click_threshold:
                    # Double click detected! Open the window
                    window_open = True
                last_click_time = current_time

            # --- WINDOW INTERACTION (If open) ---
            if window_open:
                # Check for Close Button click
                if close_btn_rect.collidepoint(mx, my):
                    window_open = False
                    is_dragging = False
                
                # Check for Header Dragging click
                elif title_bar_rect.collidepoint(mx, my):
                    is_dragging = True
                    # Calculate exactly where inside the header you clicked so it doesn't snap awkwardly
                    drag_offset_x = window_rect.x - mx
                    drag_offset_y = window_rect.y - my

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if is_dragging:
                window_rect.x = mx + drag_offset_x
                window_rect.y = my + drag_offset_y

    # --- DRAWING ---
    screen.fill(BLUE) # OS Wallpaper Background

    # 1. Draw Folder Icon on Desktop
    pygame.draw.rect(screen, YELLOW, folder_icon_rect, border_radius=4)
    icon_text = font_small.render("My Files", True, WHITE)
    screen.blit(icon_text, (folder_icon_rect.x + 10, folder_icon_rect.bottom + 5))

    # 2. Draw GUI Window (Only if active)
    if window_open:
        # Window Main Body
        pygame.draw.rect(screen, LIGHT_GRAY, window_rect)
        pygame.draw.rect(screen, DARK_GRAY, window_rect, 2) # Outer border

        # Title Bar / Window Header
        pygame.draw.rect(screen, TITLE_BLUE, title_bar_rect)
        window_title = font_title.render(f"Exploring: {TARGET_FOLDER}", True, WHITE)
        screen.blit(window_title, (title_bar_rect.x + 10, title_bar_rect.y + 5))

        # Close Button
        pygame.draw.rect(screen, RED, close_btn_rect, border_radius=3)
        x_text = font_title.render("X", True, WHITE)
        screen.blit(x_text, (close_btn_rect.x + 12, close_btn_rect.y + 1))

        # Render files inside window body
        y_offset = window_rect.y + title_bar_height + 15
        
        # Slicing down to maximum 10 items so they don't leak out the bottom of the window box
        for file in file_list[:10]:
            # Simple icon representation text
            display_text = f"📄 {file}"
            text_surface = font_small.render(display_text, True, BLACK)
            screen.blit(text_surface, (window_rect.x + 15, y_offset))
            y_offset += 24

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()