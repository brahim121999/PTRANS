import numpy as np
from PIL import Image
from .utils import *
from matplotlib import pyplot as plt
from scipy.ndimage.measurements import label, center_of_mass
from numpy.linalg import norm
from munkres import Munkres, print_matrix
import time


def find_t4(vtb_filename, prc_filename, left=True, plot=False):
    sens = 1
    if not left:
        sens = -1

    # Initialisation des path des radios de test
    process_filename = prc_filename
    vtb_filename = vtb_filename

    # Chargement des images
    vtb_image = load_image(vtb_filename)
    process_image = load_image(process_filename)

    # Labellisation de chaque vertèbre et chaque processus
    vtb_labeled, vtb_ncomponents = label(vtb_image)
    process_labeled, process_ncomponents = label(process_image)

    prc_array = list()  # Liste des barycentres
    vtb_array = list()  # Liste des barycentres des vertèbres
    directions_array = list()  # Liste des directions des processus (vecteurs)

    # Détermination des barycentres et directions des processus épineux
    for i in range(1, process_ncomponents + 1):
        centers, direction1, direction2= get_direction(np.where(process_labeled != i, 0, process_labeled))
        prc_array.append(centers)
        directions_array.append(direction1)

    # Détermination des barycentres des vertèbres
    for j in range(1, vtb_ncomponents + 1):
        y_c, x_c = center_of_mass(np.where(vtb_labeled != j, 0, vtb_labeled))
        vtb_array.append(np.asarray((x_c, y_c)))

    # Calcul de la matrice de distances
    dist_matrix = distance_matrix(vtb_array, prc_array, directions_array, distance_vtb_prc)

    # Zero padding de la matrice en cas de différence de nb de vtb et de prc
    diff = np.abs(dist_matrix.shape[0] - dist_matrix.shape[1])
    if diff != 0:
        pad = ((0, diff), (0, 0))
        if dist_matrix.shape[0] > dist_matrix.shape[1]:
            pad = ((0, 0), (0, diff))
        dist_matrix = np.pad(dist_matrix, pad)

    # Algorithme hongrois à partir de la matrice de distances
    m = Munkres()
    indexes = m.compute(dist_matrix)
    # Appariement des vertèbres à partir des indices résultatns de l'algo hongrois
    final_vtb, final_prc, errors = pair_matrix(indexes, vtb_labeled, process_labeled)

    # Repérage de T4 et récupération des barycentres de T4 et T5 (pour calcul de longueur t4)
    count = 0
    for i, val in enumerate(errors):
        print("Val : {} Remove indice {}".format(val, i))
        vtb_array.pop(val - count)
        if i <= count:
            count += 1
    vtb_array = vtb_array[::-1]

    # Récupération des centres de masse de T4 et de T5
    t4_x_c, t4_y_c = int(np.floor(vtb_array[sens * 3][0])), int(np.floor(vtb_array[sens * 3][1]))
    t5_x_c, t5_y_c = int(np.floor(vtb_array[sens * 4][0])), int(np.floor(vtb_array[sens * 4][1]))

    # On trouve les points de mesure de t4 et de t5 puis on calcule la distance entre les deux 
    mesure_t4 = bresenham([t4_x_c, t4_y_c], [2 * t4_x_c - t5_x_c, 2 * t4_y_c - t5_y_c], final_vtb, check_value=0)
    mesure_t5 = bresenham([t4_x_c, t4_y_c], [t5_x_c, t5_y_c], final_vtb, check_value=5)
    t4_width = distance_euclidienne(mesure_t4, mesure_t5)


    if plot:
        m_vtb = np.ma.masked_where(vtb_image <= 0, vtb_image)
        m_prc = np.ma.masked_where(process_image <= 0, process_image)
        plt.imshow(m_prc, cmap="Paired")
        plt.imshow(m_vtb, cmap="Accent")

        generate_plot(final_vtb, final_prc, vtb_array, prc_array, directions_array)
        plt.annotate('T4', xy=(t4_x_c, t4_y_c), xytext=(t4_x_c, t4_y_c + 300), arrowprops=dict(facecolor='black'))
        plt.plot([mesure_t4[0], mesure_t5[0]], [mesure_t4[1], mesure_t5[1]])
        plt.scatter(mesure_t4[0], mesure_t4[1], marker="x", c="black", s=50)
        plt.scatter(mesure_t5[0], mesure_t5[1], marker="x", c="black", s=50)

        plt.show()

    return t4_width, mesure_t4, mesure_t5


if __name__ == "__main__":
    start_time = time.time()
    p_f = "process.png"
    v_f = "wrong_vtb2.png"
    t4 = find_t4(vtb_filename=v_f, prc_filename=p_f, plot=True)
    print("Taille de t4 : ", t4)

    print("--- %s seconds ---" % (time.time() - start_time))
