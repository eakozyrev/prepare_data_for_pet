import matplotlib.pyplot as plt
import numpy as np
import sys

def draw(whatopen, wheresave):
    print('plot name = ',whatopen, ' to image ',wheresave)
    arr = np.fromfile(whatopen, dtype=np.float32)
    try:
        arr = np.reshape(arr, (9, 20, 356, 150, 150))
        arr = np.sum(arr, axis=(0, 1))
    except:
        arr = np.reshape(arr, (356, 150, 150))
    ax = plt.imshow(arr[:,66])
    plt.colorbar(ax)
    plt.savefig(wheresave)
    del arr

if __name__=='__main__':
    draw(sys.argv[1],sys.argv[2])
