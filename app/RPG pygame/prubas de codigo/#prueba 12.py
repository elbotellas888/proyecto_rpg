import pygame
import random
import math
import time

# Definimos la ruta al directorio actual
path = "C:/Users/martinjr44/Desktop/"

# Inicializa Pygame
pygame.init()

# Define las dimensiones de la pantalla
screen_width = 1152
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Función para cargar imágenes con manejo de errores
def load_image(path):
    try:
        return pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print(f"Error al cargar la imagen {path}: {e}")
        return None

attack_timer = 0.05
# Clase para el Jugador
class Player:
    def __init__(self):
        # Carga las imágenes del jugador (animación)
        self.name = "master"
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
                        self.images[key][i] = pygame.transform.scale(image, (256 , 128))

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

    def draw(self, screen):
        # Verificar que el estado y el índice de la animación son válidos
        if self.state in self.images and 0 <= self.current_frame < len(self.images[self.state]):
            screen.blit(self.images[self.state][self.current_frame], self.rect)

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


# Clase para los Enemigos


class Enemy:
    def __init__(self, name, health, attack, defense, sprite_path):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.sprite = load_image(sprite_path)
        Enemy.attack_timer=0.05
        # Escala el sprite si fue cargado correctamente
        if self.sprite:
            self.sprite = pygame.transform.scale(self.sprite, (128, 128))
        
        # Rectángulo para detectar colisiones
        self.rect = self.sprite.get_rect()
        self.rect.x = random.randint(100, screen_width - 100)
        self.rect.y = random.randint(100, screen_height - 100)
        
        
        # Variables para el estado de la muerte del enemigo
        self.is_dead = False
        self.death_animation = [
            load_image("death_1.png"),
            load_image("death_2.png"),
            load_image("death_3.png"),
        ]
        self.death_frame = 0
        self.death_timer = 0
        self.last_death_time = 0
        self.respawn_time = 5  # En segundos
        # Enfriamiento para ataques
        self.attack_timer = 0
        self.attack_cooldown = 2  # El enemigo debe esperar 2 segundos entre cada ataque

    def receive_damage(self, damage):
        """Manejo de daño recibido por el enemigo."""
        damage_taken = max(0, damage - self.defense)
        self.health -= damage_taken
        print(f"{self.name} recibe {damage_taken} de daño. Salud restante: {self.health}")
        
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            self.last_death_time = time.time()
            print(f"{self.name} ha sido derrotado.")
            return False  # El enemigo muere
        return True

    def attack_player(self, player):
        """El enemigo ataca al jugador si no está en enfriamiento."""
        if self.attack_timer <= 0.05:
            self.attack_cooldown==0.05
            time.attack_timer = 4

            #timer para poder volver a recibir daño
            if time.time() - self.last_death_time >= 3:
                self.health = 100
                self.attack_timer = 0.05
                self.last_death_time = time.time()
                self.attack_cooldown = 2

            damage = random.randint(self.attack - 2, self.attack + 2)  # Daño aleatorio
            print(f"{self.name} ataca a {player.name} con {damage} de daño.")
            self.attack_timer = self.attack_cooldown  # Reinicia el temporizador de ataque
            return player.receive_damage(damage)
        return False

    def move_towards_player(self, player):
        """Movimiento del enemigo hacia el jugador."""
        if self.is_dead and time.time() - self.last_death_time < self.respawn_time:
            return  # No se mueve ni ataca mientras está muerto

        # Movimiento hacia el jugador
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)

        # Normalizamos el movimiento para que sea constante
        if distance != 0:
            dx, dy = dx / distance, dy / distance
            self.rect.x += dx * 2  # Movimiento horizontal
            self.rect.y += dy * 2  # Movimiento vertical
        # el enemigo deja de seguir al jugador si el jugador se aleja
        if distance > 300:
            self.rect.x -= dx * 2  # Movimiento horizontal
            self.rect.y -= dy * 2  # Movimiento vertical

        # Si el enemigo ha muerto, y el tiempo de respawn ha pasado, respawnea
        if self.is_dead and time.time() - self.last_death_time >= self.respawn_time:
            self.respawn()

    def respawn(self):
        """El enemigo respawnea después de un tiempo."""
        self.health = 100
        self.rect.x = random.randint(100, screen_width - 100)
        self.rect.y = random.randint(100, screen_height - 100)
        self.is_dead = False
        print(f"{self.name} ha reaparecido.")

    def draw(self, screen):
        """Dibuja al enemigo en la pantalla."""
        if self.is_dead:
            self.death_timer += 1
            if self.death_timer % 5 == 0:
                self.death_frame = (self.death_frame + 1) % len(self.death_animation)
            screen.blit(self.death_animation[self.death_frame], self.rect)
        else:
            screen.blit(self.sprite, self.rect)

    def update(self):
        """Actualiza el temporizador de ataque y el estado del enemigo."""
        # Actualiza el temporizador de ataque, lo reduce hasta 0
        if self.attack_timer > 0:
            self.attack_timer -= 0.1  # Reducción más lenta, ajustable

        # Aseguramos que el temporizador de ataque no sea negativo
        if self.attack_timer < 0:
            self.attack_timer -= 0.05 




# Cargar imagen del fondo
background_image = load_image("sacate.png")
background_rect = background_image.get_rect() if background_image else None

# Crea una superficie para la sombra
shadow_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

# Crea una instancia del jugador
player = Player()

# Crea instancias de enemigos
enemies = [
    Enemy("fantasma rojo", health=100, attack=6, defense=2, sprite_path="fantasma de sangre.gif"),
]

# Bucle principal del juego
clock = pygame.time.Clock()

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
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):  # Verifica si el enemigo está cerca
                player.attack_enemy(enemy)
                break
    else:
        player.state = "idle"

    # Movimiento y ataque de enemigos
    for enemy in enemies:
        enemy.move_towards_player(player)
        enemy.update()  # Actualiza el temporizador de ataque

        

        # el enemigo deja de atacar cuando esta muerto
        if enemy.is_dead:
            enemy.death_timer += 1
            if enemy.death_timer % 5 == 0:
                enemy.death_frame = (enemy.death_frame + 1) % len(enemy.death_animation)
            screen.blit(enemy.death_animation[enemy.death_frame], enemy.rect)
            continue
        
        if enemy.rect.colliderect(player.rect):  # Si el enemigo está cerca
            if not player.receive_damage(enemy.attack):
                print(f"{player.name} ha muerto.")
                running = False  # Termina el juego si el jugador muere

    # Actualiza la animación del jugador
    player.update()

    # Dibuja el fondo
    if background_image:
        screen.blit(background_image, background_rect)

    # Dibuja la sombra
    screen.blit(shadow_surface, (0, 0))

    # Dibuja al jugador
    player.draw(screen)

    # Dibuja a los enemigos
    for enemy in enemies:
        enemy.draw(screen)

    # Actualiza la pantalla
    pygame.display.flip()

    # Control de FPS
    clock.tick(60)

# Finaliza Pygame
pygame.quit()
