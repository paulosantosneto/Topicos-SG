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
        self.max_force = 0.04
        self.rastro = []
        self.max_rastro = 200
        self.arrival_distance = 100
        self.seeking = True
        self.vision_range = 500

    # Possibly to rotate a triangle points
    def rotate_point(self,radius,angle):
        return pygame.Vector2(
            radius * math.cos(angle) - 0 * math.sin(angle), 
            radius * math.sin(angle) - 0 * math.cos(angle)
        )
    
    def draw(self, screen):
    
        for pos in self.rastro:
            pygame.draw.circle(screen, "grey", (int(pos[0]), int(pos[1])), 1)
            pygame.draw.line(screen,"blue",[self.position.x,self.position.y],[target.x,target.y],2)
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
    
    #Linear interpolation
    def map_value(self, value, start1, stop1, start2, stop2):
        return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))

    def seek(self, target):
        desired = target - self.position
        distance =  math.hypot(desired.x, desired.y)

        if distance < self.arrival_distance:
            m = self.map_value(distance, 0, self.arrival_distance, 0, self.max_speed)
            desired = (self.normalize(desired) * m)
        else:
            desired = (self.normalize(desired) * self.max_speed)

        steering = self.limit_force(desired - self.velocity)

        self.rastro.append((self.position.x, self.position.y))
        if len(self.rastro) > self.max_rastro:
            self.rastro.pop(0)

        return steering
       
    def flee(self, target): 
        desired = target - self.position
        distance = math.hypot(desired.x, desired.y)
        if distance <= self.vision_range:
            return self.seek(target)*-1
        else:
            return (self.seek(target))

    def apply_force(self, force):
        self.velocity += force
        self.position += self.velocity

def canvas_draw():
    screen.fill("white")
    pygame.draw.circle(screen, "grey", [target.x, target.y], 30, 2)
    pygame.draw.line(screen, "black", [50, 300], [target.x, target.y], 1)

    agent1.draw(screen)
    agent2.draw(screen)
    pygame.display.flip()
    clock.tick(120)

running = True

agent1 = Agent(x=50, y=300)
agent1.color = "red"
agent2 = Agent(x=200,y=-300)

target = pygame.Vector2(1150, 300)

while running:

    agent1.apply_force(agent1.seek(agent2.position))
    agent2.apply_force(agent2.seek(target))
    agent2.apply_force(agent2.flee(agent1.position))
    # if agent.seeking:
    #     agent.apply_force(agent.seek(target))
    # else:
    #     agent.apply_force(agent.flee(target))

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if agent.seeking == True:
        #         agent.seeking = False
        #     else:
        #         agent.seeking = True
        if event.type == pygame.MOUSEMOTION:
            target = pygame.Vector2(event.pos)
      
    canvas_draw()


pygame.quit()
