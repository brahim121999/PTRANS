import numpy as np
from .utils import *
from matplotlib import pyplot as plt
from scipy.ndimage.measurements import label
import time


def find_hrt_axes(hrt_filename="coeur2.png", plot=False):
    hrt_image = load_image(hrt_filename)

    hrt_labeled, hrt_components = label(hrt_image)

    hrt_array = list()
    hrt_direction = list()

    # Récupération des directions et le barycentre  du blob de points
    for i in range(1, hrt_components + 1):
        centers, direction1, direction2 = get_direction(np.where(hrt_labeled != i, 0, hrt_labeled))
        directions = np.asarray((direction1[0], direction1[1], direction2[0], direction2[1]))
        hrt_array.append(centers)
        hrt_direction.append(directions)

    # coordonnées du barycentre du coeur
    hrt_x, hrt_y = zip(*hrt_array)
    cdg = [int(hrt_x[0]), int(hrt_y[0])]


    # Calcul axe de directions
    for i, dir in enumerate(hrt_direction):
        x = dir[0] + hrt_x[i]
        y = dir[1] + hrt_y[i]
        x2 = dir[2] + hrt_x[i]
        y2 = dir[3] + hrt_y[i]

        dir1_points = np.array([(hrt_x[i], hrt_y[i]), (x, y)])
        dir2_points = np.array([(hrt_x[i], hrt_y[i]), (x2, y2)])

    # Récupération des coordonnées des points formant le petit et grand axe
    # (utilisation de l'algorithme de bresenham)
    gaxe = get_heart_axe(dir1_points, dir2_points, cdg, hrt_image)
    paxe = get_heart_axe(dir2_points, dir1_points, cdg, hrt_image)

    # Récupération des coordonnées des points formant le petit et grand axe
    # (via calcul de produit scalaire, traitement théoriquement optimisé)
    # paxe, gaxe = get_heart_axe_V2(dir1_points,hrt_image, cdg)

    # calcul de la taille de ces axes
    ga_size = distance_euclidienne(gaxe[0], gaxe[1])
    pa_size = distance_euclidienne(paxe[0], paxe[1])

    # Affichage
    if plot:
        # Affichage du coeur et des axes
        mask_hrt = np.ma.masked_where(hrt_image <= 0, hrt_image)

        fig, ax = plt.subplots()
        # Affiche centre de gravité
        ax.scatter(hrt_x, hrt_y, marker="+", c='black')

        plt.imshow(mask_hrt)

        # affiche points des axes
        plt.scatter(gaxe[0][0], gaxe[0][1], c='green', marker='+', linewidth=3)
        plt.scatter(gaxe[1][0], gaxe[1][1], c='orange', marker='+', linewidth=3)
        plt.scatter(paxe[0][0], paxe[0][1], c='blue', marker='+', linewidth=3)
        plt.scatter(paxe[1][0], paxe[1][1], c='black', marker='+', linewidth=3)

        a = dir1_points[0][1] - dir1_points[1][1]
        b = dir1_points[0][0] - dir1_points[1][0]

        # Affiche les vecteurs sur matplotlib
        plt.quiver(cdg[0], cdg[1], a, b, color="green", scale=5)
        plt.quiver(cdg[0], cdg[1], -b, a, color="red", scale=5)
        plt.show()

    return [ga_size, pa_size], [gaxe, paxe]


if __name__ == "__main__":
    start_time = time.time()
    h_f = "coeur4.png"
    hrt_axes, hrt_points = find_hrt_axes(hrt_filename=h_f, plot=True)
    print("Taille Grand Axe : \n", hrt_axes[0], "\nTaille Petit axe : \n", hrt_axes[1])

    print("--- %s seconds ---" % (time.time() - start_time))
