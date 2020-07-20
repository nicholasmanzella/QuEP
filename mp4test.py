import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Movie Test', artist='Matplotlib',
                comment='Movie support!')
writer = FFMpegWriter(fps=120, metadata=metadata)

fig = plt.figure()
l, = plt.plot([], [], 'C0o')

plt.ylim(-2, 2)

x0, y0 = 0, 0

with writer.saving(fig, "writer_test.mp4", dpi=400):
    for i in range(100):
        x0 += 0.1 * np.random.randn()
        y0 += 0.1 * np.random.randn()
        l.set_data(x0, y0)
        writer.grab_frame()
