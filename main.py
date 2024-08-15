import pygame
import random
import sys
from src.player import Player
from src.enemy import Enemy

# Inicializar PyGame
pygame.init()

# Configuraciones de pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Selecciona el Nivel de Juego')

# Colores
white = (255, 255, 255)
black_blue = (0, 0, 0)

# Cargar sonidos
intro_sound = pygame.mixer.Sound('assets/sounds/intro.mp3')
asteroid_sound = pygame.mixer.Sound('assets/sounds/asteroid.mp3')

def show_menu():
    font = pygame.font.Font(None, 74)
    title_text = font.render('Asteroid Kodland', True, white)
    easy_text = font.render('1. Facil', True, white)
    medium_text = font.render('2. Medio', True, white)
    hard_text = font.render('3. Experto', True, white)
    exit_text = font.render('4. Salir', True, white)

    # Reproducir sonido del menú
    intro_sound.play(-1)  # -1 para reproducir en bucle

    menu_running = True
    while menu_running:
        screen.fill(black_blue)

        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
        screen.blit(easy_text, (screen_width // 2 - easy_text.get_width() // 2, 150))
        screen.blit(medium_text, (screen_width // 2 - medium_text.get_width() // 2, 250))
        screen.blit(hard_text, (screen_width // 2 - hard_text.get_width() // 2, 350))
        screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, 450))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    intro_sound.stop()  # Detener el sonido del menú
                    return (2, 1.25)  # Nivel fácil, 2 enemigos, velocidad actual + 25%
                elif event.key == pygame.K_2:
                    intro_sound.stop()  # Detener el sonido del menú
                    return (5, 1.5)  # Nivel medio, 5 enemigos, velocidad actual + 50%
                elif event.key == pygame.K_3:
                    intro_sound.stop()  # Detener el sonido del menú
                    return (8, 1.75)  # Nivel experto, 8 enemigos, velocidad actual + 75%
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()  # Cierra el juego

def pause_menu():
    font = pygame.font.Font(None, 74)
    resume_text = font.render('1. Volver al juego', True, white)
    restart_text = font.render('2. Reiniciar en otro nivel', True, white)
    exit_text = font.render('3. Salir', True, white)

    paused = True
    while paused:
        screen.fill(black_blue)

        screen.blit(resume_text, (screen_width // 2 - resume_text.get_width() // 2, 150))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, 250))
        screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    paused = False  # Volver al juego
                elif event.key == pygame.K_2:
                    num_enemies, speed_multiplier = show_menu()  # Reiniciar en otro nivel
                    game_loop(num_enemies, speed_multiplier)
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()  # Cierra el juego

def show_game_over():
    font = pygame.font.Font(None, 74)
    game_over_text = font.render('GAME OVER', True, white)
    restart_text = font.render('1. Volver al menú', True, white)
    exit_text = font.render('2. Salir', True, white)

    # Detener el sonido del juego
    pygame.mixer.music.stop()

    game_over_running = True
    while game_over_running:
        screen.fill(black_blue)

        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, 150))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, 250))
        screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_over_running = False
                    num_enemies, speed_multiplier = show_menu()
                    if num_enemies:
                        game_loop(num_enemies, speed_multiplier)
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

def check_collision(player, enemies):
    player_rect = pygame.Rect(player.x, player.y, player.image.get_width(), player.image.get_height())
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.image.get_width(), enemy.image.get_height())
        if player_rect.colliderect(enemy_rect):
            return True
    return False

def game_loop(num_enemies, speed_multiplier):
    player = Player(screen_width // 2, screen_height - 100)
    enemies = []

    # Generar enemigos según el nivel seleccionado y aplicar el multiplicador de velocidad
    while len(enemies) < num_enemies:
        x = random.randint(0, screen_width - 50)
        y = random.randint(-150, -50)
        speed = random.randint(1, 3) * speed_multiplier
        new_enemy = Enemy(x, y, speed)
        if not any(enemy.rect.colliderect(pygame.Rect(x, y, new_enemy.image.get_width(), new_enemy.image.get_height())) for enemy in enemies):
            enemies.append(new_enemy)

    # Reproducir sonido del juego
    pygame.mixer.music.load('assets/sounds/asteroid.mp3')
    pygame.mixer.music.play(-1)  # -1 para reproducir en bucle

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause_menu()  # Pausar el juego y mostrar el menú de pausa

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -3  # Velocidad aumentada
        if keys[pygame.K_RIGHT]:
            dx = 3
        if keys[pygame.K_UP]:
            dy = -3
        if keys[pygame.K_DOWN]:
            dy = 3

        player.move(dx, dy)

        screen.fill(black_blue)

        player.draw(screen)
        for enemy in enemies:
            enemy.move()
            enemy.draw(screen)

        if check_collision(player, enemies):
            show_game_over()  # Mostrar pantalla de GAME OVER

        pygame.display.update()

    pygame.quit()
    sys.exit()

# Mostrar el menú y obtener la cantidad de enemigos y multiplicador de velocidad según el nivel seleccionado
num_enemies, speed_multiplier = show_menu()

# Iniciar el juego con el nivel seleccionado
if num_enemies:
    game_loop(num_enemies, speed_multiplier)
