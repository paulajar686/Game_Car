import pygame
from pygame.locals import *
import random
import os

print("Directorio actual:", os.getcwd())
pygame.init()

# =========================
# ASSETS GLOBALES
# =========================

ROAD_X = 100
ROAD_WIDTH = 300
SIDE_WIDTH = 100

# Scroll global
road_scroll_y = 0
side_scroll_y = 0

pygame.mixer.init()
paused = False


# Pantalla de Inicio

def show_start_menu(screen):
    font_title = pygame.font.Font(None, 60)
    font_option = pygame.font.Font(None, 36)
    
    title = font_title.render("CAR GAME", True, (255, 255, 255))
    play_text = font_option.render("Presiona ENTER para jugar", True, (0, 255, 0))
    exit_text = font_option.render("Presiona ESC para salir", True, (255, 100, 100))

    while True:
        screen.fill((20, 20, 20))
        screen.blit(title, (width // 2 - title.get_width() // 2, 140))
        screen.blit(play_text, (width // 2 - play_text.get_width() // 2, 240))
        screen.blit(exit_text, (width // 2 - exit_text.get_width() // 2, 290))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    exit()


# Nuevo usuario

def get_username(screen):
    font = pygame.font.Font(None, 32)

    # Cargar usuarios
    if os.path.exists('usuarios.txt'):
        with open('usuarios.txt', 'r') as f:
            usuarios = [line.strip() for line in f if line.strip()]
    else:
        usuarios = []

    # Opciones internas (IDs)
    usuarios.append("__ADD_USER__")
    usuarios.append("__DELETE_USER__")

    selected = 0

    while True:
        screen.fill((10, 10, 10))

        title = pygame.font.Font(None, 40).render(
            "Selecciona tu usuario", True, (255, 255, 255)
        )
        screen.blit(title, (width // 2 - title.get_width() // 2, 50))

        for i, user in enumerate(usuarios):
            y_pos = 120 + i * 35
            color = (0, 255, 0) if i == selected else (255, 255, 255)

            # NUEVO USUARIO
            if user == "__ADD_USER__":
                screen.blit(icon_add, (width // 2 - 140, y_pos))
                text = font.render("Nuevo usuario", True, color)

            # ELIMINAR USUARIO
            elif user == "__DELETE_USER__":
                screen.blit(icon_trash, (width // 2 - 140, y_pos))
                text = font.render("Eliminar usuario", True, color)

            # USUARIO NORMAL
            else:
                text = font.render(user, True, color)

            screen.blit(
                text,
                (width // 2 - text.get_width() // 2, y_pos)
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    selected = (selected + 1) % len(usuarios)
                elif event.key == K_UP:
                    selected = (selected - 1) % len(usuarios)

                elif event.key == K_RETURN:
                    option = usuarios[selected]

                    if option == "__ADD_USER__":
                        return create_new_user(screen)

                    elif option == "__DELETE_USER__":
                        delete_user_menu(screen)
                        return get_username(screen)  # recargar menú

                    else:
                        return option


# Eliminar usuario

def delete_user_menu(screen):
    font = pygame.font.Font(None, 36)

    # Cargar usuarios reales
    if not os.path.exists('usuarios.txt'):
        return

    with open('usuarios.txt', 'r') as f:
        usuarios = [line.strip() for line in f if line.strip()]

    if not usuarios:
        return

    selected = 0

    while True:
        screen.fill((15, 15, 15))

        title = pygame.font.Font(None, 40).render(
            "Eliminar usuario", True, (255, 100, 100)
        )
        screen.blit(title, (width // 2 - title.get_width() // 2, 50))

        subtitle = pygame.font.Font(None, 24).render(
            "ENTER = eliminar | ESC = cancelar",
            True, (200, 200, 200)
        )
        screen.blit(subtitle, (width // 2 - subtitle.get_width() // 2, 90))

        for i, user in enumerate(usuarios):
            color = (255, 0, 0) if i == selected else (255, 255, 255)
            text = font.render(user, True, color)
            screen.blit(text, (width // 2 - text.get_width() // 2, 140 + i * 35))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    selected = (selected + 1) % len(usuarios)
                elif event.key == K_UP:
                    selected = (selected - 1) % len(usuarios)

                elif event.key == K_RETURN:
                    confirm = confirm_delete(screen, usuarios[selected])
                    if confirm:

                        username = usuarios[selected]

                        delete_user_scores(username)
                        usuarios.pop(selected)
                        with open('usuarios.txt', 'w') as f:
                            for u in usuarios:
                                f.write(u + '\n')
                        return

                elif event.key == K_ESCAPE:
                    return


# Confirmar la eliminación del usuario

def confirm_delete(screen, username):
    font = pygame.font.Font(None, 36)

    while True:
        screen.fill((0, 0, 0))

        msg = font.render(
            f"¿Eliminar a '{username}'?",
            True, (255, 255, 255)
        )
        screen.blit(msg, (width // 2 - msg.get_width() // 2, 200))

        opt = pygame.font.Font(None, 28).render(
            "Y = Sí    N = No",
            True, (200, 200, 200)
        )
        screen.blit(opt, (width // 2 - opt.get_width() // 2, 250))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_y:
                    return True
                elif event.key == K_n or event.key == K_ESCAPE:
                    return False


# Eliminar las estadísticas

def delete_user_scores(username):
    if not os.path.exists("scores.txt"):
        return

    with open("scores.txt", "r") as f:
        lines = f.readlines()

    # Mantener solo las líneas de otros usuarios
    filtered = [
        line for line in lines
        if not line.startswith(username + ",")
    ]

    with open("scores.txt", "w") as f:
        f.writelines(filtered)


# Elegir el nivel de inicio

def select_start_level(screen):
    font = pygame.font.Font(None, 36)

    # Nivel -> (nivel, velocidad inicial)
    options = [
        ("Nivel 1", 1),
        ("Nivel 2", 2),
        ("Nivel 3", 3),
        ("Nivel 5", 5),
        ("Nivel 6", 6),
        ("Nivel 7", 7),
        ("Nivel 8", 8),
    ]

    selected = 0

    while True:
        screen.fill((20, 20, 20))

        title = pygame.font.Font(None, 40).render(
            "Selecciona nivel inicial", True, (255, 255, 255)
        )
        screen.blit(title, (width // 2 - title.get_width() // 2, 60))

        for i, (label, _) in enumerate(options):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            text = font.render(label, True, color)
            screen.blit(text, (width // 2 - text.get_width() // 2, 140 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == K_RETURN:
                    return options[selected][1]  # devuelve el nivel


# Seleccionar la duración del juego

def select_game_duration(screen):
    font = pygame.font.Font(None, 36)
    options = [("30 segundos", 30), ("60 segundos", 60), ("90 segundos", 90), ("Infinito", None)]
    selected = 0

    while True:
        screen.fill((20, 20, 20))
        title = pygame.font.Font(None, 40).render("Selecciona duración del juego", True, (255, 255, 255))
        screen.blit(title, (width // 2 - title.get_width() // 2, 50))

        for i, (label, _) in enumerate(options):
            color = (255, 255, 255) if i != selected else (0, 255, 0)
            text = font.render(label, True, color)
            screen.blit(text, (width // 2 - text.get_width() // 2, 120 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == K_RETURN:
                    return options[selected][1]  # devuelve los segundos o None


# Crear nuevo usuario

def create_new_user(screen):
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(100, 300, 300, 40)
    username = ''
    active = True

    while active:
        screen.fill((0, 0, 0))
        label = font.render("Ingresa tu nombre:", True, (255, 255, 255))
        screen.blit(label, (width // 2 - label.get_width() // 2, 240))

        txt_surface = font.render(username, True, (0, 255, 0))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN and username:
                    # Guardar nuevo usuario si no existe
                    if os.path.exists('usuarios.txt'):
                        with open('usuarios.txt', 'r') as f:
                            existing = [line.strip() for line in f]
                    else:
                        existing = []

                    if username not in existing:
                        with open('usuarios.txt', 'a') as f:
                            f.write(username + '\n')

                    return username
                elif event.key == K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 15:
                        username += event.unicode


def draw_environment(screen, level, speed):
    global road_scroll_y, side_scroll_y

    road_scroll_y += speed
    side_scroll_y += speed

    if road_scroll_y >= height:
        road_scroll_y = 0
    if side_scroll_y >= height:
        side_scroll_y = 0

    lvl = min(level, max(road_textures.keys()))

    road_tex = road_textures[lvl]
    grass_tex = grass_textures[lvl]

    # Pasto izquierdo
    screen.blit(grass_tex, (0, side_scroll_y - height))
    screen.blit(grass_tex, (0, side_scroll_y))

    # Pasto derecho
    screen.blit(grass_tex, (ROAD_X + ROAD_WIDTH, side_scroll_y - height))
    screen.blit(grass_tex, (ROAD_X + ROAD_WIDTH, side_scroll_y))

    # Carretera
    screen.blit(road_tex, (ROAD_X, road_scroll_y - height))
    screen.blit(road_tex, (ROAD_X, road_scroll_y))



# --- Función para mostrar top scores ---
def draw_high_scores(screen, scores):
    # Fondo para el ranking
    pygame.draw.rect(screen, (50, 50, 50), (120, 150, 260, 180), border_radius=10)
    pygame.draw.rect(screen, (200, 200, 200), (120, 150, 260, 180), 2, border_radius=10)

    font_title = pygame.font.Font(None, 28)
    font_scores = pygame.font.Font(None, 24)
    
    title_surface = font_title.render("🏆 Mejores Puntajes 🏆", True, (255, 255, 0))
    screen.blit(title_surface, (width // 2 - title_surface.get_width() // 2, 160))

    for i, (name, score) in enumerate(scores[:5]):
        text = f"{i+1}. {name}: {score}"
        score_surface = font_scores.render(text, True, (255, 255, 255))
        screen.blit(score_surface, (140, 190 + i * 25))


def init_game_state():
    global level, speed, score, start_time

    level = start_level
    speed = 2 + (level - 1)
    score = (level - 1) * 10
    start_time = pygame.time.get_ticks()

# create the window
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

pygame.mixer.music.load(os.path.join('music/theme.ogg'))
pygame.mixer.music.set_volume(0.5)  # volumen entre 0.0 y 1.0
pygame.mixer.music.play(-1)  # -1 para reproducir en bucle

# colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# road and marker sizes
road_width = 300
marker_width = 10
marker_height = 50

# lane coordinates
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# road and edge markers
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# for animating movement of the lane markers
lane_marker_move_y = 0

# player's starting coordinates
player_x = 250
player_y = 400

# frame settings
clock = pygame.time.Clock()
fps = 120

# game settings
gameover = False
level_timer = 0
powerup_active = None
powerup_timer = 0
timed_out = False

class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # scale the image down so it's not wider than the lane
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load(os.path.join('images/car.png'))
        super().__init__(image, x, y)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image, x, y, type):
        super().__init__()
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.type = type

# sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

# create the player's car
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# load the vehicle images
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load(os.path.join('images/' + image_filename))
    vehicle_images.append(image)

# Cargar imágenes de power-ups
powerup_images = {
    'turbo': pygame.image.load(os.path.join('images/powerup_turbo.png')),
    # Puedes añadir más tipos aquí más adelante
}

# =========================
# TEXTURAS GLOBALES
# =========================

road_textures = {
    1: pygame.image.load("images/road_level.png").convert(),
}

grass_textures = {
    1: pygame.image.load("images/grass_level.png").convert(),
}

# Escalar UNA SOLA VEZ
for lvl in road_textures:
    road_textures[lvl] = pygame.transform.scale(
        road_textures[lvl], (ROAD_WIDTH, height)
    )

    grass_textures[lvl] = pygame.transform.scale(
        grass_textures[lvl], (SIDE_WIDTH, height)
    )


# --- Iconos de menú ---
ICON_SIZE = 24

icon_add = pygame.image.load(
    os.path.join('images/icon_add.png')
).convert_alpha()
icon_add = pygame.transform.scale(icon_add, (ICON_SIZE, ICON_SIZE))

icon_trash = pygame.image.load(
    os.path.join('images/icon_trash.png')
).convert_alpha()
icon_trash = pygame.transform.scale(icon_trash, (ICON_SIZE, ICON_SIZE))

# load the crash image
crash = pygame.image.load(os.path.join('images/crash.png'))
crash_rect = crash.get_rect()
show_start_menu(screen)
username = get_username(screen)
start_level = select_start_level(screen)
selected_duration = select_game_duration(screen)
init_game_state()
start_time = pygame.time.get_ticks()  # guardar el tiempo inicial

def pause_menu(screen):
    font_title = pygame.font.Font(None, 48)
    font_option = pygame.font.Font(None, 36)

    options = ["Continuar", "Salir del nivel", "Cerrar juego"]
    selected = 0

    while True:
        screen.fill((0, 0, 0))

        # Fondo semi-transparente
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title = font_title.render("PAUSA", True, (255, 255, 255))
        screen.blit(title, (width // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(options):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            text = font_option.render(option, True, color)
            screen.blit(
                text,
                (width // 2 - text.get_width() // 2, 200 + i * 50)
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == K_RETURN:
                    return options[selected]
                elif event.key == K_ESCAPE:
                    return "Continuar"


# game loop
running = True
while running:
    
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # move the player's car using the left/right arrow keys
        if event.type == KEYDOWN:
            
            if event.key == K_ESCAPE and not gameover:
                paused = True

            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100
                
            # check if there's a side swipe collision after changing lanes
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    
                    gameover = True
                    
                    # place the player's car next to other vehicle
                    # and determine where to position the crash image
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
    if paused:
        choice = pause_menu(screen)

        if choice == "Continuar":
            paused = False

        elif choice == "Salir del nivel":
            # Resetear estado del juego
            gameover = False
            paused = False
            speed = 2 + (start_level - 1)
            score = (start_level - 1) * 10
            level = start_level
            vehicle_group.empty()
            powerup_group.empty()
            player.rect.center = [player_x, player_y]
            start_time = pygame.time.get_ticks()

            # Volver a menús
            show_start_menu(screen)
            username = get_username(screen)
            start_level = select_start_level(screen)
            selected_duration = select_game_duration(screen)
            start_time = pygame.time.get_ticks()

        elif choice == "Cerrar juego":
            pygame.quit()
            exit()

        continue  # 👈 IMPORTANTE: no ejecutar lógica del juego

            
    # draw the grass
    screen.fill(green)
    
    draw_environment(screen, level, speed)

    # draw the player's car
    player_group.draw(screen)
    
    # add a vehicle
    if len(vehicle_group) < 2:
        
        # ensure there's enough gap between vehicles
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
                
        if add_vehicle:
            
            # select a random lane
            lane = random.choice(lanes)
            
            # select a random vehicle image
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)
        
        # Añadir power-up ocasionalmente
        if random.randint(1, 300) == 1 and len(powerup_group) == 0:
            lane = random.choice(lanes)
            powerup = PowerUp(powerup_images['turbo'], lane, height / -2, 'turbo')
            powerup_group.add(powerup)
 
    
    # make the vehicles move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        # remove vehicle once it goes off screen
        if vehicle.rect.top >= height:
            vehicle.kill()
            
            # add to score
            score += 1
            
            # speed up the game after passing 5 vehicles
            if score % 10 == 0:
                level += 1
                speed += 1
                level_timer = pygame.time.get_ticks()
    
    # draw the vehicles
    vehicle_group.draw(screen)
    powerup_group.draw(screen)

    
    # Mover power-ups
    for powerup in powerup_group:
        powerup.rect.y += speed
        if powerup.rect.top > height:
            powerup.kill()

    # Colisión jugador con power-up
    collected = pygame.sprite.spritecollide(player, powerup_group, True)
    for pu in collected:
        if pu.type == 'turbo':
            powerup_active = 'turbo'
            powerup_timer = pygame.time.get_ticks()
            speed += 3  # velocidad aumentada


    # display the score
    # mostrar puntuación y nivel
    font = pygame.font.Font(None, 24)
    score_text = font.render(f'Score: {score}', True, white)
    level_text = font.render(f'Nivel: {level}', True, white)
    screen.blit(score_text, (20, 20))
    screen.blit(level_text, (20, 50))
    # Mostrar cuenta regresiva si hay duración limitada
    if selected_duration is not None:
        elapsed = (pygame.time.get_ticks() - start_time) / 1000
        remaining = max(0, int(selected_duration - elapsed))

        # Cambiar color si quedan 10 segundos o menos
        if remaining <= 10:
            timer_color = (255, 0, 0) # Rojo
        else:
            timer_color = white

        timer_text = font.render(f'Tiempo: {remaining}s', True, white)
        screen.blit(timer_text, (width - 150, 20))

    # Barra de progreso hacia el próximo nivel
    progress = score % 10  # progreso entre niveles (0–9)
    bar_width = int((progress / 10) * 200)  # ancho proporcional
    bar_x = width // 2 - 100
    bar_y = 80

    # Fondo de la barra
    pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, 200, 20), border_radius=5)
    # Barra llena
    pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, bar_width, 20), border_radius=5)
    # Borde
    pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, 200, 20), 2, border_radius=5)


    # Mostrar texto de subida de nivel por 2 segundos
    if level_timer and pygame.time.get_ticks() - level_timer < 2000:
        big_font = pygame.font.Font(None, 48)
        level_msg = big_font.render(f"¡Nivel {level}!", True, (255, 255, 0))
        screen.blit(level_msg, (width // 2 - level_msg.get_width() // 2, height // 2 - 50))
    elif level_timer:
        level_timer = 0  # ocultar mensaje después de 2s

    # check if there's a head on collision
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
            
    # display game over
    if gameover:
        screen.blit(crash, crash_rect)
        
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        if 'timed_out' in locals() and timed_out:
            text = font.render('¡Tiempo agotado! ¿Jugar de nuevo? (Y/N)', True, white)
        else:
            text = font.render('Game over. Play again? (Y/N)', True, white)

        # Guardar el puntaje en archivo
        with open('scores.txt', 'a') as f:
            f.write(f'{username},{score}\n')

        # Leer y ordenar los mejores puntajes
        scores = []
        if os.path.exists('scores.txt'):
            with open('scores.txt', 'r') as f:
                for line in f:
                    name, s = line.strip().split(',')
                    scores.append((name, int(s)))
            scores.sort(key=lambda x: x[1], reverse=True)

        draw_high_scores(screen, scores)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)
    
    # Desactivar efecto turbo después de 5 segundos
    if powerup_active == 'turbo':
        if pygame.time.get_ticks() - powerup_timer > 5000:
            speed -= 3
            powerup_active = None

    # Verificar si el tiempo se agotó
    if selected_duration is not None and not gameover:
        elapsed = (pygame.time.get_ticks() - start_time) / 1000  # en segundos
        if elapsed >= selected_duration:
            gameover = True
            crash_rect.center = player.rect.center  # posiciona algo
            timed_out = True  # nuevo estado

    pygame.display.update()

    # wait for user's input to play again or exit
    while gameover:
        
        clock.tick(fps)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                gameover = False
                running = False
                
            # get the user's input (y or n)
            if event.type == KEYDOWN:
                if event.key == K_y:
                    gameover = False
                    init_game_state()
                    vehicle_group.empty()
                    powerup_group.empty()
                    player.rect.center = [player_x, player_y]


                elif event.key == K_n:
                    # exit the loops
                    gameover = False
                    running = False
pygame.mixer.music.stop()
pygame.quit()