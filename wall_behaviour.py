import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 520))
clock = pygame.time.Clock()

class Agent():
    def __init__(self, x, y):
        self.color = "black"
        self.radius = 15
        self.velocity = pygame.Vector2(0, -2)
        self.max_speed = 2
        self.position = pygame.Vector2(x, y)
        self.max_force = 0.1
        self.rastro = []
        self.max_rastro = 200
        self.arrival_distance = 100

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius, 2)

    def normalize(self, subvec):
        distance = math.hypot(subvec.x, subvec.y)
        if distance > 0:
            return subvec / distance
        return subvec
    
    def limit_force(self, steering):
        if steering.length() > self.max_force:
            return self.normalize(steering) * self.max_force
        return steering
    
    def map_value(self, value, start1, stop1, start2, stop2):
        return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))

    def seek(self, target):
        desired = target - self.position
        distance = math.hypot(desired.x, desired.y)
        if distance < self.arrival_distance:
            m = self.map_value(distance, 0, self.arrival_distance, 0, self.max_speed)
            desired = self.normalize(desired) * m
        else:
            desired = self.normalize(desired) * self.max_speed

        steering = self.limit_force(desired - self.velocity)
        self.velocity += steering
        self.position += self.velocity
    
    def separation(self, agents):
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in agents:
            distance = self.position.distance_to(other.position)
            if 0 < distance < self.radius * 2:
                diff = self.position - other.position
                steering += diff / distance
                total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering = self.normalize(steering) * self.max_speed - self.velocity
                steering = self.limit_force(steering)
        return steering
    
    def alignment(self, agents):
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in agents:
            distance = self.position.distance_to(other.position)
            if 0 < distance < 50:  # Consider nearby agents
                steering += other.velocity
                total += 1
        if total > 0:
            steering /= total
            steering = self.normalize(steering) * self.max_speed
            steering = self.limit_force(steering - self.velocity)
        return steering

    def cohesion(self, agents):
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in agents:
            distance = self.position.distance_to(other.position)
            if 0 < distance < 50:
                steering += other.position
                total += 1
        if total > 0:
            steering /= total
            steering = steering - self.position
            steering = self.normalize(steering) * self.max_speed
            steering = self.limit_force(steering - self.velocity)
        return steering

    def flock(self, agents):
        sep = self.separation(agents) * 3.5  # Give higher weight to separation
        ali = self.alignment(agents) * 1.0
        coh = self.cohesion(agents) * 1.0
        self.velocity += sep + ali + coh

    def check_collision(self, other):
        distance = self.position.distance_to(other.position)
        min_distance = self.radius + other.radius
        if distance < min_distance:
            overlap = min_distance - distance
            direction = (self.position - other.position).normalize()
            self.position += direction * overlap / 2
            other.position -= direction * overlap / 2

    def line_collision(self, start, end):
        line_vec = end - start
        point_vec = self.position - start
        line_len = line_vec.length()
        if line_len == 0:
            return False
        projection = point_vec.dot(line_vec) / line_len
        if projection < 0 or projection > line_len:
            return False
        closest_point = start + (line_vec * (projection / line_len))
        distance_to_line = self.position.distance_to(closest_point)
        if distance_to_line < self.radius:
            direction = (self.position - closest_point).normalize()
            self.position = closest_point + direction * self.radius
            return True
        return False

running = True

# AGENTS

agents = []
x = -200
y = 250

for y_pos in range(10):
    for agent in range(5):
        agents.append(Agent(x=x, y=y))
        y += 30
    x += 30
    y = 250

# OBSTACLES (two vertical lines)
obstacles = [
    (pygame.Vector2(500, -100), pygame.Vector2(500, 240)),
    (pygame.Vector2(500, 280), pygame.Vector2(500, 720)),
]

# TARGET
target = pygame.Vector2(1000, 260)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #elif event.type == pygame.MOUSEMOTION:
            #target = pygame.Vector2(event.pos)

    for agent in agents:
        agent.seek(target)
        agent.flock(agents)  # Apply flocking behavior
        for other_agent in agents:
            if agent != other_agent:
                agent.check_collision(other_agent)
        for start_pos, end_pos in obstacles:
            agent.line_collision(start_pos, end_pos)

    screen.fill("white")
    pygame.draw.circle(screen, "grey", [target.x, target.y], 30, 2)

    for start_pos, end_pos in obstacles:
        pygame.draw.line(screen, "blue", start_pos, end_pos, 2)

    for agent in agents:
        agent.draw(screen)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
