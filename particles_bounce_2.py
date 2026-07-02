from manim import *
import numpy as np

class ParticlesBounce2(Scene):
    def construct(self):
        # Vertical 9:16 para Shorts
        self.camera.frame_width = 9
        self.camera.frame_height = 16
        
        # 120 partículas - más caos que v1
        particles = VGroup()
        velocities = []
        
        for _ in range(120):
            p = Dot(radius=0.06, color=YELLOW)
            p.move_to([np.random.uniform(-4,4), np.random.uniform(-7,7), 0])
            particles.add(p)
            velocities.append(np.array([np.random.uniform(-3,3), np.random.uniform(-4,4), 0]))
        
        self.add(particles)
        
        def update_particles(mob, dt):
            for i, p in enumerate(mob):
                p.shift(velocities[i] * dt)
                # Bounce en bordes
                if abs(p.get_x()) > 4.3:
                    velocities[i][0] *= -1
                if abs(p.get_y()) > 7.8:
                    velocities[i][1] *= -1
        
        particles.add_updater(update_particles)
        self.wait(30) # 30s exactos
