import pygame
import math
import numpy as np

# Define Phong reflection parameters
ambient_strength = 0.1
diffuse_strength = 0.9
specular_strength = 0.01
shininess = 8 

# Define light position and camera position
light_position = np.array([300, -400, 700])
camera_position = np.array([0, -200, 500])
ball_color = np.array([1,1,1])

# wall
# ambient_strength = 0.1
# diffuse_strength = 0.9
# specular_strength = 0.01
# shininess = 8 

# # Define light position and camera position
# light_position = np.array([500, -400, 700])
# camera_position = np.array([0, -200, 500])
# ball_color = np.array([1,1,1])

# copper 0.7216,0.451,0.2
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Phong Model Sphere")
clock = pygame.time.Clock()

# Function to calculate the sphere with Phong lighting
def render_sphere(radius, sphere_center, light_pos, camera_pos):
    for y in range(-radius, radius):
        for x in range(-radius, radius):
            if x**2 + y**2 <= radius**2:
                z = math.sqrt(radius**2 - x**2 - y**2)  # Calculate z value to simulate sphere

                # Calculate normal vector at point (x, y, z)
                normal = np.array([x, y, z]) / radius

                # Calculate the light vector and view vector
                light_vec = (light_pos - np.array([x, y, z]))
                light_vec /= np.linalg.norm(light_vec)

                view_vec = (camera_pos - np.array([x, y, z]))
                view_vec /= np.linalg.norm(view_vec)

                # Diffuse component
                diffuse = max(0, np.dot(normal, light_vec))
                diffuse_color = diffuse_strength * diffuse

                # Specular component (Phong reflection)
                reflection_vec = 2 * np.dot(normal, light_vec) * normal - light_vec
                specular = max(0, np.dot(view_vec, reflection_vec))
                specular_color = specular_strength * (specular ** shininess)
                # Final color calculation
                final_intensity = ambient_strength + diffuse_color + specular_color
                final_intensity = max(0, min(final_intensity, 1))

                # Color sphere based on light intensity
                color = ball_color * final_intensity * 255
                screen.set_at((x + sphere_center[0], y + sphere_center[1]), color)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_s]:
        specular_strength -= 0.1
    if pressed[pygame.K_w]:
        specular_strength += 0.1
    if pressed[pygame.K_a]:
        diffuse_strength -= 0.1
    if pressed[pygame.K_q]:
        diffuse_strength += 0.1
    print(str(specular_strength) + " " + str(diffuse_strength))
    # Clear the screen
    screen.fill((0, 0, 0))

    # Render the sphere with Phong lighting
    render_sphere(100, [200, 150], light_position, camera_position)

    pygame.display.flip()
    clock.tick(60)  # Limit frame rate to 60 FPS

pygame.quit()
