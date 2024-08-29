import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

class Agent():

    def __init__(self, x, y):
        self.color = "green"
        self.radius = 15
        self.velocity = pygame.Vector2(0, -2)
        self.max_speed = 2
        self.position = pygame.Vector2(x, y)
        self.max_force = 0.02
        self.rastro = []
        self.max_rastro = 200

    def draw(self, screen):
    
        for pos in self.rastro:
            pygame.draw.circle(screen, "grey", (int(pos[0]), int(pos[1])), 1)

        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
    
    def normalize(self, subvec):
        distance = math.hypot(subvec.x, subvec.y)
        if distance > 0:
            return subvec / distance
        return subvec
    
    def limit_force(self, steering):
        if steering.length() > self.max_force:
            return self.normalize(steering) * self.max_force
        return steering

    def seek(self, target):
        desired = self.normalize(target - self.position) * self.max_speed
        steering = self.limit_force(desired - self.velocity)
        self.velocity += steering
        self.position += self.velocity
        
        self.rastro.append((self.position.x, self.position.y))
        
        if len(self.rastro) > self.max_rastro:
            self.rastro.pop(0)

running = True

agent = Agent(x=50, y=300)
target = pygame.Vector2(1150, 300)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            target = pygame.Vector2(event.pos) 

    agent.seek(target)

    screen.fill("white")
    pygame.draw.circle(screen, "grey", [target.x, target.y], 30, 2)
    pygame.draw.line(screen, "black", [50, 300], [target.x, target.y], 1) 
    
    agent.draw(screen)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
