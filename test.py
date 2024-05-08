import math
import numpy as np
from multiprocessing import Pool

def setPixel(data):
    x = data[0]
    y = data[1]
    radius = data[2]
    camera_pos = data[3]
    light_pos = data[4]
    sphere_center = data[5]
    specular_color_real = data[6]
    ball_color = data[7]
    ambient_strength = data[8]
    diffuse_strength = data[9]
    specular_strength = data[10]
    shininess = data[11]
    z = math.sqrt(radius**2 - x**2 - y**2) 
    normal = np.array([x, y, z]) / radius

    light_vec = (light_pos - np.array([x, y, z]))
    light_vec /= np.linalg.norm(light_vec)

    view_vec = (camera_pos - np.array([x, y, z]))
    view_vec /= np.linalg.norm(view_vec)

    diffuse = max(0, np.dot(normal, light_vec))
    diffuse_color = diffuse_strength * diffuse
    diffuse_color = diffuse_color * ball_color

    reflection_vec = 2 * np.dot(normal, light_vec) * normal - light_vec
    
    specular = max(0, np.dot(view_vec, reflection_vec))
    specular_color = specular_strength * (specular ** shininess)
    specular_color = specular_color * specular_color_real
    final_intensity = diffuse_color + specular_color + ambient_strength * ball_color

    color = final_intensity * 255
    for i in range(len(color)):
        color[i] = min(color[i],255)
    return [(x + sphere_center[0], y + sphere_center[1]), color]    

if __name__ == '__main__':
    import pygame
    import time
    pygame.init()
    specular_color_real = np.array([0.256777,0.13,0.08])
    ball_color = np.array([0.7216,0.451,0.2])
    ambient_strength = 0.1
    diffuse_strength = 1
    specular_strength = 1
    shininess = 2
    light_position = np.array([300, -400, 700])
    camera_position = np.array([0, -200, 500])

    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Phong Model Sphere")
    pool = Pool(2) # recommended five

    def render_sphere(radius, sphere_center, light_pos, camera_pos):
        tasks = []
        for y in range(-radius, radius):
            for x in range(-radius, radius):
                if x**2 + y**2 <= radius**2:
                    tasks.append(
                        (
                            x, 
                            y, 
                            radius, 
                            camera_pos, 
                            light_pos, 
                            sphere_center,
                            specular_color_real,
                            ball_color,
                            ambient_strength,
                            diffuse_strength,
                            specular_strength,
                            shininess
                        )
                    )
        
        result = pool.map(setPixel, tasks)
        for i in result:
            screen.set_at(i[0],i[1])

    running = True
    while running:
        start = time.time()
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
            specular_color_real = np.array([0.256777,0.13,0.08])
            ambient_strength = 0.1
            diffuse_strength = 1
            specular_strength = 1
            shininess = 2
            ball_color = np.array([0.7216,0.351,0.2])
        if pressed[pygame.K_2]:
            specular_color_real = np.array([0.3,0.3,0.3])
            ambient_strength = 0.3 #35
            diffuse_strength = 1.1  #6
            specular_strength = 1.1  # 1.44
            shininess = 12
            ball_color = np.array([0.53,0.53,0.53])
        if pressed[pygame.K_3]:
            specular_color_real = np.array([0,0.3,0])
            ambient_strength = 0.4
            diffuse_strength = 0.5
            specular_strength = 1.1 # 44
            shininess = 12 
            ball_color = np.array([0,1,0])
        if pressed[pygame.K_4]:
            ambient_strength = 0.1
            diffuse_strength = 0.9
            specular_strength = 0.01
            shininess = 8 
            specular_color_real = np.array([1,1,1])
            ball_color = np.array([1,1,1])
        if pressed[pygame.K_5]:
            light_position[0] = -abs(light_position[0])
        if pressed[pygame.K_6]:
            light_position[0] = abs(light_position[0])

        screen.fill((0, 0, 0))

        render_sphere(100, [200, 150], light_position, camera_position)

        pygame.display.flip()

        end = time.time()
        print(end - start)
    pool.close()
    pool.join()
    pygame.quit()
