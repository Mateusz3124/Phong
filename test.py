import pygame
import math
import numpy as np

ambient_strength = 0.01
diffuse_strength = 0.8
specular_strength = 0.499
shininess = 16

light_position = np.array([300, -400, 700])
camera_position = np.array([0, -200, 500])
ball_color = np.array([0.7216,0.451,0.2])

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Phong Model Sphere")
clock = pygame.time.Clock()

def render_sphere(radius, sphere_center, light_pos, camera_pos):
    for y in range(-radius, radius):
        for x in range(-radius, radius):
            if x**2 + y**2 <= radius**2:
                z = math.sqrt(radius**2 - x**2 - y**2) 

                normal = np.array([x, y, z]) / radius

                light_vec = (light_pos - np.array([x, y, z]))
                light_vec /= np.linalg.norm(light_vec)

                view_vec = (camera_pos - np.array([x, y, z]))
                view_vec /= np.linalg.norm(view_vec)

                diffuse = max(0, np.dot(normal, light_vec))
                diffuse_color = diffuse_strength * diffuse

                reflection_vec = 2 * np.dot(normal, light_vec) * normal - light_vec
                specular = max(0, np.dot(view_vec, reflection_vec))
                specular_color = specular_strength * (specular ** shininess)

                final_intensity = ambient_strength + diffuse_color + specular_color
                final_intensity = max(0, min(final_intensity, 1))

                color = ball_color * final_intensity * 255
                screen.set_at((x + sphere_center[0], y + sphere_center[1]), color)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        light_position[2] -= 100
    if pressed[pygame.K_s]:
        light_position[2] += 100
    if pressed[pygame.K_a]:
        light_position[0] -= 100
    if pressed[pygame.K_d]:
        light_position[0] += 100
    if pressed[pygame.K_z]:
        light_position[1] -= 100
    if pressed[pygame.K_x]:
        light_position[1] += 100
    
    if pressed[pygame.K_1]:
        ambient_strength = 0.1
        diffuse_strength = 0.8
        specular_strength = 0.499
        shininess = 16
        ball_color = np.array([0.7216,0.451,0.2])
    if pressed[pygame.K_2]:
        ambient_strength = 0.35
        diffuse_strength = 0.6
        specular_strength = 1.44
        shininess = 14 
        ball_color = np.array([0.53,0.53,0.53])
    if pressed[pygame.K_3]:
        ambient_strength = 0.2
        diffuse_strength = 0.7
        specular_strength = 0.24
        shininess = 8 
        ball_color = np.array([0,1,0])
    if pressed[pygame.K_4]:
        ambient_strength = 0.1
        diffuse_strength = 0.9
        specular_strength = 0.01
        shininess = 8 
        ball_color = np.array([1,1,1])

    screen.fill((0, 0, 0))

    render_sphere(100, [200, 150], light_position, camera_position)

    pygame.display.flip()

pygame.quit()
