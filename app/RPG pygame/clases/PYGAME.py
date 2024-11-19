import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

class Player():
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.forma = self.image.get_rect(0, 0, 64, 64)
        self.forma.center = x, y
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        self.max_vel = pygame.Vector2(100, 100)
        self.max_acc = pygame.Vector2(200, 200)






        def movimiento(self, delta_x, delta_y):
            self.acc.x += delta_x
            self.acc.y += delta_y



player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # llenar la pantalla con un color
    screen.fill("green")

    player_image = pygame.image.load("C:\Users\martinjr44\Desktop\png-transparent-pixel-game-among-us-pixel-art-pixelated-design-red-character-imposter-thumbnail.png")
    screen.blit(player_image, player_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt


    pygame.display.flip()


    dt = clock.tick(60) / 1000.0  

pygame.quit()