import pygame

pygame.init()
pygame.font.init()
open_app = [0.5, 1, 1.5, 2]
admin_user_screen = [pygame.Rect(200, 300, 300, 300)]
start_box = [pygame.Rect(1020, 90, 100, 100)]
app_text = pygame.font.SysFont('Arial', 50)
font = pygame.font.SysFont('Arial', 120)
font_admin = pygame.font.SysFont('Arial', 50)
to_start = pygame.font.SysFont('Arial', 60)
WHITE = (255, 255, 255) //test
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
width = 1920
height = 1080
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height // 2 - player_size // 2
player_speed = 20
admin_logo = pygame.image.load("Brang_pic/admin_logo.png")
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
clock = pygame.time.Clock()
login = True
running = True
turn_off = False
admin_start = False
admin_start_confirm = False
admin_wallpaper_flag = False
admin_wallpaper = False
player = pygame.Rect(player_x, player_y, player_size, player_size)


while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not turn_off:
        if player.x < mouse_x:
            player.x = mouse_x
        if player.x > mouse_x:
            player.x = mouse_x
        if player.y < mouse_y:
            player.y = mouse_y
        if player.y > mouse_y:
            player.y = mouse_y

    player.x = max(0, min(player.x, width - player_size))
    player.y = max(0, min(player.y, height - player_size))

    if login == True:
        screen.fill(WHITE)
        title_text = font.render("log in", True, GREEN)
        screen.blit(title_text, (850, 60))
        pygame.draw.rect(screen, BLUE, player)
        for admin_for in admin_user_screen:
            screen.blit(admin_logo, (250, 350))
        for admin_login_for in admin_user_screen:
            if admin_login_for.collidepoint(mouse_pos):
                if mouse_click[0] == True:
                    admin_start_confirm = True
                    login = False
        for admin_login_text_for in admin_user_screen:
            admin_text = font_admin.render("Admin", True, BLUE)
            screen.blit(admin_text, (300, 600))
        pygame.display.flip()

    if admin_start_confirm == True:
        screen.fill(BLUE)
        pygame.draw.rect(screen, WHITE, player)
        title_text = font.render("start", True, GREEN)
        screen.blit(title_text, (800, 60))
        title_text = font.render("manual", True, GREEN)
        screen.blit(title_text, (700, 200))
        for box_for in start_box:
            pygame.draw.rect(screen, GREEN, box_for)
        for start_box_for in start_box:
            if player.colliderect(start_box_for):
                admin_wallpaper = True
        pygame.display.flip()

    clock.tick(60)

pygame.quit()