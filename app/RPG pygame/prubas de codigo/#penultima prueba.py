#penultima prueba
import pygame
import random
import math
import time
import csv
# Definimos la ruta al directorio actual
path = "C:/Users/martinjr44/Desktop/"

# Inicializa Pygame
pygame.init()

# Define las dimensiones de la pantalla
screen_width = 1500
screen_height = 850
screen = pygame.display.set_mode((screen_width, screen_height))

# Función para cargar imágenes con manejo de errores
def load_image(path):
    try:
        return pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print(f"Error al cargar la imagen {path}: {e}")
        return None


# Clase para el Jugador
class Player:
    def __init__(self):
        # Carga las imágenes del jugador (animación)
        self.name = "master"
        self.player_speed= 0.3
        self.images = {
            "idle": [
                load_image("normal.png"),
                load_image("normal.png"),
                load_image("normal_2.png"),
                load_image("normal_2.png"),
            ],
            "walk_right": [
                load_image("correr_derecha_1.png"),
                load_image("correr_derecha_2.png"),
                load_image("correr_derecha_3.png"),
                load_image("correr_derecha_4.png"),
                load_image("correr_derecha_5.png"),
                load_image("correr_derecha_6.png"),
            ],
            "walk_left": [
                load_image("correr_izquierda_1.png"),
                load_image("correr_izquierda_2.png"),
                load_image("correr_izquierda_3.png"),
                load_image("correr_izquierda_4.png"),
                load_image("correr_izquierda_5.png"),
                load_image("correr_izquierda_6.png"),
            ],
            "walk_up": [
                load_image("correr_derecha_1.png"),
                load_image("correr_derecha_2.png"),
                load_image("correr_derecha_3.png"),
                load_image("correr_derecha_4.png"),
                load_image("correr_derecha_5.png"),
                load_image("correr_derecha_6.png"),
            ],
            "walk_down": [
                load_image("correr_izquierda_1.png"),
                load_image("correr_izquierda_2.png"),
                load_image("correr_izquierda_3.png"),
                load_image("correr_izquierda_4.png"),
                load_image("correr_izquierda_5.png"),
                load_image("correr_izquierda_6.png"),
            ],
            "attack_animacion": [
                load_image("atacar.png")  # Añade más fotogramas si tienes
            ],
        }

        # Escalar las imágenes del jugador
        self.player_size = (128, 128)
        for key, image_list in self.images.items():
            for i, image in enumerate(image_list):
                if image:  # Verifica que la imagen se haya cargado correctamente
                    self.images[key][i] = pygame.transform.scale(image, self.player_size)
                    # Agrandar el tamaño del jugador cuando este ataque
                    if key == "attack_animacion":
                        self.images[key][i] = pygame.transform.scale(image, (218 , 128))

        # Define la posición inicial del jugador
        self.pos = (150, 159)
        self.rect = self.images["idle"][0].get_rect(center=self.pos)

        # Estado actual del jugador
        self.state = "idle"
        self.current_frame = 0

        # Variables para la animación
        self.animation_speed = 0.1  # Velocidad de la animación (más pequeño, más rápido)
        self.animation_timer = 0

        # Estadísticas del jugador
        self.health = 300
        self.attack = 20
        self.defense = 5
        self.level = 1
        self.experience = 0

        # Control de la animación de ataque
        self.attack_timer = 0
        self.attack_cooldown = 1  # Enfriamiento entre ataques (en segundos)
        self.attack_animation_timer = 0  # Control del avance de la animación de ataque

    def update(self):
        # Si está atacando, actualizamos la animación de ataque
        if self.state == "attack_animacion":
            self.attack_animation_timer += self.animation_speed
            if self.attack_animation_timer >= 1:
                self.attack_animation_timer = 0
                self.current_frame += 1
                if self.current_frame >= len(self.images["attack_animacion"]):
                    self.state = "idle"  # Después de la animación de ataque, volvemos a "idle"
                    self.current_frame = 0  # Reiniciamos el frame de animación
        # Si no está atacando, actualizamos la animación normal (idle o caminar)
        elif self.state != "attack_animacion":
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.images[self.state])

    # Aquí se corrige la definición del método draw
    def draw(self, screen, camera_x, camera_y):
        # Verificar que el estado y el índice de la animación son válidos
        if self.state in self.images and 0 <= self.current_frame < len(self.images[self.state]):
            # Resta las coordenadas de la cámara para hacer que el jugador se mueva en función de la cámara
            screen.blit(self.images[self.state][self.current_frame], 
                        (self.rect.x - camera_x, self.rect.y - camera_y))

    def receive_damage(self, damage):
       # enfriamiento entre ataques
        if self.attack_timer < 0:
            self.attack_timer = 0.05
            # Si el enemigo ha sido derrotado, recibe experiencia
        player.attack_timer-=0.05
        damage_taken = max(0, damage - self.defense)
        self.health -= damage_taken
        print(f"{self.health} - {damage_taken} (Daño recibido)")
        if self.health <= 0:
            self.health = 0  # Evitar que la salud sea negativa
            print("¡Has muerto!")
            return False  # El jugador ha muerto
        return True

    def attack_enemy(self, enemy):
        # Sólo se puede atacar si el tiempo de enfriamiento ha pasado
        if self.attack_timer <= 00.5:  
            damage = random.randint(self.attack - 2, self.attack + 2)
            print(f"{self.name} ataca a {enemy.name} con {damage} de daño.")
            self.attack_timer = self.attack_cooldown  # Reinicia el temporizador de ataque
            self.state = "attack_animacion"  # Activar la animación de ataque
            return enemy.receive_damage(damage)
        return False

    def level_up(self):
        if self.experience >= 100 * self.level:
            self.level += 1
            self.attack += 5
            self.defense += 2
            self.health = 100 + self.level * 10
            self.experience = 0
            print(f"¡Nivel {self.level} alcanzado! Salud: {self.health}, Ataque: {self.attack}, Defensa: {self.defense}")

# Función para dibujar el HUD
def draw_hud(screen, player):
    font = pygame.font.SysFont("Arial", 20)
    health_text = font.render(f"Salud: {player.health}", True, (255, 1, 1))
    attack_text = font.render(f"Ataque: {player.attack}", True, (1, 255, 1))
    defense_text = font.render(f"Defensa: {player.defense}", True, (1, 1, 255))
    level_text = font.render(f"Nivel: {player.level}", True, (200, 200, 100))
    experience_text = font.render(f"Experiencia: {player.experience}", True, (255, 1, 255))

    screen.blit(health_text, (10, 10))
    screen.blit(attack_text, (10, 40))
    screen.blit(defense_text, (10, 70))
    screen.blit(level_text, (10, 100))
    screen.blit(experience_text, (10, 130))

# colisionar con las paredes



background_image = load_image("experimento_grande.png")
background_rect = background_image.get_rect() if background_image else None

# Crea una superficie para la sombra
shadow_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

# Crea una instancia del jugador
player = Player()



# Bucle principal del juego
clock = pygame.time.Clock()

# Definir los límites del mapa (puedes ajustar estos valores dependiendo del tamaño del mapa)
map_width = 3000  # Ejemplo de un mapa más grande que la pantalla
map_height = 3000

# Coordenadas iniciales de la cámara
camera_x = 0
camera_y = 0
camera_speed = 5  

running = True
while running:
    # Gestiona los eventos del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Obtén las teclas presionadas
    keys = pygame.key.get_pressed()

    


    # Actualización del jugador
    if keys[pygame.K_RIGHT]:
        player.rect.x += 5
        player.state = "walk_right"
    elif keys[pygame.K_LEFT]:
        player.rect.x -= 5
        player.state = "walk_left"
    elif keys[pygame.K_UP]:
        player.rect.y -= 5
        player.state = "walk_up"
    elif keys[pygame.K_DOWN]:
        player.rect.y += 5
        player.state = "walk_down"
    elif keys[pygame.K_SPACE]:  # Atacar
        player.state = "attack_animacion"  # Atacar cuando presionas la barra espaciadora
        # Solo atacar si está cerca de un enemigo
        
    else:
        player.state = "idle"


# Bucle principal del juego
    # Actualiza la animación del jugador
    player.update()

    # Variables de la cámara
    # La cámara sigue al jugador, pero se limita a no salirse de los bordes del mapa
    camera_x = player.rect.centerx - screen_width // 2
    camera_y = player.rect.centery - screen_height // 2

    # Limita el movimiento de la cámara para que no salga del mapa
    camera_x = max(0, min(camera_x, map_width - screen_width))
    camera_y = max(0, min(camera_y, map_height - screen_height))

    # Dibuja el fondo
    if background_image:
        screen.blit(background_image, (-camera_x, -camera_y))  # Desplaza el fondo

    # Dibuja la sombra
    screen.blit(shadow_surface, (0, 0))

    # Dibujar al jugador
    player.draw(screen, camera_x, camera_y)

        # Dibujar el HUD
    draw_hud(screen, player)

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

# Ejecutar el juego
pygame.quit()