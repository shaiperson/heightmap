import threading as thr
from math import ceil
import numpy as np
import geometry

def create(mesh, width, height, nthreads):
    result = np.zeros((height, width))

    def thread_target(positions, height, width, meshref):
        for (i,j) in positions:
            samplingpoint = ((j / width) * meshref.xspan, meshref.yspan - (i / height) * meshref.yspan)
            containing_faces = meshref.faces_for_2D_point(samplingpoint)
            if containing_faces:
                sampleheight = max([geometry.calcMeshHeightFor2DPoint(samplingpoint, face) for face in containing_faces])
                result.itemset((i,j), sampleheight)

    total_samples = height * width
    samples_per_thread = int(ceil(total_samples / nthreads))
    positions = [(i,j) for i in range(height) for j in range(width)]

    pos_idx = 0
    threads = []
    for k in range(nthreads-1):
        curr_thread = thr.Thread(target=thread_target, args=(positions[pos_idx:pos_idx+samples_per_thread], height, width, mesh))
        threads.append(curr_thread)
        curr_thread.start()
        pos_idx += samples_per_thread

    last_thread = thr.Thread(target=thread_target, args=(positions[pos_idx:], height, width, mesh))
    threads.append(last_thread)
    last_thread.start()

    for t in threads:
        t.join()

    return result