from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

def plot_noise(noise, cmap_given = "gray"):
    plt.imshow(noise, cmap=cmap_given, interpolation='nearest')
    plt.show()

def interpolate(a0,a1,x):
    if (x <= 0):
        x=0
    if (x >= 1):
        x=1
    return (a1 - a0) * ((x * (x * 6.0 - 15.0) + 10.0) * x * x * x) + a0

def perlin(size,res):
    noise=np.zeros((size,size))
    
def testshow(size,scale):
    noise = np.zeros((size, size))
    gradients = np.random.randn(size // scale + 2, size // scale + 2, 2)
    for y in range(size):
        for x in range(size):
            cell_x = x // scale
            cell_y = y // scale
            # Calculate the position within the cell as fractional offsets
            cell_offset_x = x / scale - cell_x
            cell_offset_y = y / scale - cell_y
            # Calculate the dot products between gradients and offsets
            dot_product_tl = np.dot([cell_offset_x, cell_offset_y], gradients[cell_y, cell_x])
            dot_product_tr = np.dot([cell_offset_x - 1, cell_offset_y], gradients[cell_y, cell_x + 1])
            dot_product_bl = np.dot([cell_offset_x, cell_offset_y - 1], gradients[cell_y + 1, cell_x])
            dot_product_br = np.dot([cell_offset_x - 1, cell_offset_y - 1], gradients[cell_y + 1, cell_x + 1])
            # Interpolate the dot products using smoothstep function
            weight_x = smoothstep(cell_offset_x)
            weight_y =  smoothstep(cell_offset_y)
            interpolated_top = lerp(dot_product_tl, dot_product_tr, weight_x)
            interpolated_bottom = lerp(dot_product_bl, dot_product_br, weight_x)
            interpolated_value = lerp(interpolated_top, interpolated_bottom, weight_y)
            # Store the interpolated value in the noise array
            noise[y, x] = interpolated_value
    # Normalize the noise values within the range of 0 to 1
    noise = (noise - np.min(noise)) / (np.max(noise) - np.min(noise))
    return noise
def smoothstep(t):
    return t * t * (3 - 2 * t)
def lerp(a, b, t):
    return a + t * (b - a)

if __name__ == '__main__':
    pic=testshow(200,50)
    for i in range(200):
        for j in range(200):
            if pic[i][j]<=0.7:
                pic[i][j]=0
    plot_noise(pic)
    conv=np.array([[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4],[1,4,7,4,1]])
    conv=conv/np.sum(conv)
    low=testshow(200,100)+testshow(200,20)
    res=5*low+20*pic
    plot_noise(res)