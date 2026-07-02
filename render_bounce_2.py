import numpy as np
from PIL import Image, ImageDraw
import imageio
W, H, FPS, DURATION = 1080, 1920, 30, 30
n_particles = 120
pos = np.random.uniform([0,0], [W,H], (n_particles, 2))
vel = np.random.uniform(-15, 15, (n_particles, 2))
frames = []
print("[Constitution] Renderizando 900 frames... esto tarda 2-3 min")
for frame in range(FPS * DURATION):
    img = Image.new('RGB', (W, H), (0,0,0))
    draw = ImageDraw.Draw(img)
    pos += vel
    vel[pos[:,0] < 10, 0] *= -1
    vel[pos[:,0] > W-10, 0] *= -1
    vel[pos[:,1] < 10, 1] *= -1
    vel[pos[:,1] > H-10, 1] *= -1
    pos[:,0] = np.clip(pos[:,0], 10, W-10)
    pos[:,1] = np.clip(pos[:,1], 10, H-10)
    for x, y in pos:
        draw.ellipse([x-6, y-6, x+6, y+6], fill=(255,255,0))
    frames.append(np.array(img))
    if frame % 100 == 0: print(f"[Constitution] Frame {frame}/900")
imageio.mimsave("media/Particles_bounce_2.mp4", frames, fps=FPS)
print("[Constitution] ✅ Video listo: media/Particles_bounce_2.mp4")
