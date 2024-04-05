from copy import deepcopy
import numpy as np

#--------------------------------------------------------------------------
#utile pour tester
import matplotlib.pyplot as plt
def plot_noise(noise, cmap_given = "gray"):
    plt.imshow(noise, cmap=cmap_given, interpolation='nearest')
    plt.colorbar()
    plt.show()
#--------------------------------------------------------------------------

def interpolate(a0,a1,x):
    if (x <= 0):
        x=0
    if (x >= 1):
        x=1
    return (a1 - a0) * ((x * (x * 6.0 - 15.0) + 10.0) * x * x * x) + a0


def perlin(size,scale,a,b):
    noise = np.zeros((size, size))
    gradients = np.random.randn(size // scale + 2, size // scale + 2, 2)
    for y in range(size):
        for x in range(size):
            #grid coordinates
            cell_x = x // scale
            cell_y = y // scale
            cell_offset_x = x / scale - cell_x
            cell_offset_y = y / scale - cell_y
            dot_hg = np.dot([cell_offset_x, cell_offset_y], gradients[cell_y, cell_x])
            dot_hd = np.dot([cell_offset_x - 1, cell_offset_y], gradients[cell_y, cell_x + 1])
            dot_bg = np.dot([cell_offset_x, cell_offset_y - 1], gradients[cell_y + 1, cell_x])
            dot_bd = np.dot([cell_offset_x - 1, cell_offset_y - 1], gradients[cell_y + 1, cell_x + 1])
            interpole_h=interpolate(dot_hg,dot_hd,cell_offset_x)
            interpole_b=interpolate(dot_bg,dot_bd,cell_offset_x)
            val=interpolate(interpole_h,interpole_b,cell_offset_y)
            noise[y, x] = val
    noise = a + (noise-np.min(noise))*(b-a)/(np.max(noise)-np.min(noise))
    return noise

def fractale(size,scale,nb,persist=0.4,lacun=0.5):
    noise = np.zeros((size, size))
    f=1
    ampli=1
    som=0
    for i in range(nb):
        noise+=ampli*perlin(size,int(f*scale),0,1)
        f*=lacun
        som+=ampli
        ampli*=persist
    return fenetre(noise,0,1),som

def slope(grid,size,width=0.5):
    slope=np.zeros_like(grid)
    for i in range(size):
        for j in range(size):
            heigth=grid[i][j]
            k=np.floor(heigth/width)
            l=(heigth-k*width)/width
            slope[i][j]=float((k+min(2*l,1))*width)
    return slope

def redistrib(grid,nb,pow):
    res=np.power((grid/nb),pow)
    return fenetre(res,0,1)

def fenetre(grid,a,b):
    return a + (grid-np.min(grid))*(b-a)/(np.max(grid)-np.min(grid))

def gaussian_kernel(size, sigma):
    y = np.linspace(-(size//2), size//2, size)
    xv, yv = np.meshgrid(y, y)
    kernel = (1/(2*np.pi*sigma**2)) * np.exp(-(xv**2 + yv**2) / (2*sigma**2))
    kernel /= np.sum(kernel)
    return kernel

def convolve2D(mat, size,o=5):
    k=gaussian_kernel(size,o)
    h,w=np.shape(mat)
    h_inp,w_inp=h+(size//2)*2,w+(size//2)*2
    #inp=np.zeros((h+(size//2)*2,w+(size//2)*2))
    inp=np.pad(mat,(size//2),'edge')
    for x in range(h):
        for y in range(w):
            inp[(size//2)+x][(size//2)+y]=mat[x][y]
    out=np.zeros_like(mat)
    for i in range(h):
        for j in range(w):
            sous_matrice = inp[i:i+size, j:j+size]
            out[i, j] = np.sum(sous_matrice * k)
    return out


if __name__ == '__main__':
    imSize=200
    f,n=fractale(imSize,150,5)
    s=slope(f,imSize,0.9)
    baseriver=-redistrib(redistrib(s,n,2)-redistrib(s,n,4),1,1)
    river=np.zeros_like(baseriver)
    for i in range(imSize):
        for j in range(imSize):
            river[i][j]=1
            if baseriver[i][j]<-0.9:
                river[i][j]=0
    plot_noise(river)       
    pente=fenetre(convolve2D(river,7,5),-0.3,1)
    plot_noise(pente)
    f,n=fractale(imSize,50,5)
    s=slope(f,imSize,0.5)
    res=redistrib(s,n,4)
    for i in range(imSize):
        for j in range(imSize):
            if pente[i][j]<0:
                res[i][j]=pente[i][j]
            else:
                res[i][j]*=pente[i][j]
    plot_noise(res)