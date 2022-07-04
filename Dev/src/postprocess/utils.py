from sys import platform
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from numpy.linalg import norm
from scipy.ndimage.measurements import center_of_mass
from os.path import join, dirname
import pathlib
import cv2
import math


# Calcul de la distance barycentre d'une vtb et droite de
# direction d'un processus passant par barycentre du processus
def distance_vtb_prc(vtb, process, direction):
    p1 = np.asarray(process)
    p2 = p1 + np.asarray(direction)
    M = np.asarray(direction)
    vtb_p = np.asarray(vtb)

    test = np.dot(p2 - p1, vtb_p - p1) / np.dot(M, M)
    intersect = p1 + test * M
    dist = norm(vtb_p - intersect)
    return dist


# Calcul de la matrice de distances pour l'algorithme hongrois
def distance_matrix(vtb, process, directions, dist):
    matrix = np.zeros((len(vtb), len(process)))
    for i in range(len(vtb)):
        for j in range(len(process)):
            matrix[i, j] = dist(vtb[i], process[j], directions[j])
    return matrix


# Appariement des vertèbres en fonction du résultat de l'algo hongrois
def pair_matrix(pairs, vtb_labels, process_labels):
    # on récupère le nombre de vertèbres et de processus
    n_vtb = np.max(vtb_labels)
    n_prc = np.max(process_labels)
    print("Nombre de vertèbres : ", n_vtb)
    print("Nombre de processus : ", n_prc)

    # Liste des vertèbres sans processus
    errors = list()

    # on change tous les labels pour relabeliser proprement en positif plus tard
    vtb_labels = -vtb_labels
    process_labels = -process_labels

    count = n_vtb
    if n_vtb > n_prc:
        count = n_prc

    for vtb, prc in pairs:
        print("Vertèbre ", vtb + 1, " associée au processus ", prc + 1)
        if vtb + 1 > n_vtb or prc + 1 > n_prc:
            print("Détection de la vertèbre / processus superflue")
            if prc + 1 > n_prc:
                errors.append(vtb)
        else:
            vtb_labels = np.where(vtb_labels == -(vtb + 1), count, vtb_labels)
            process_labels = np.where(process_labels == -(prc + 1), count, process_labels)
            count -= 1
    vtb_labels = np.where(vtb_labels < 0, 0, vtb_labels)
    process_labels = np.where(process_labels < 0, 0, process_labels)
    return vtb_labels, process_labels, errors


# Génération d'un plot matplolib pour visualiser appariement de vertèbres et points + directions
def generate_plot(vtb_labels, prc_labels, vtb_arr, prc_arr, directions):
    mask_vtb = np.ma.masked_where(vtb_labels <= 0, vtb_labels)
    mask_prc = np.ma.masked_where(prc_labels <= 0, prc_labels)
    cmap = "tab10"

    vtb_x, vtb_y = zip(*vtb_arr)
    prc_x, prc_y = zip(*prc_arr)

    fig, ax = plt.subplots()
    img = ax.imshow(mask_vtb, cmap=cmap)
    ax.imshow(mask_prc, cmap=cmap)
    ax.scatter(vtb_x, vtb_y, marker="+", c='black')
    ax.scatter(prc_x, prc_y, marker="+", c='black')
    for i, dir in enumerate(directions):
        x = dir[0] + prc_x[i]
        y = dir[1] + prc_y[i]
        ax.axline([prc_x[i], prc_y[i]],
                  [x, y], color='red', linewidth=0.5)
    
    ax.set_title("test")
    fig.colorbar(img)


# Obtention de la direction d'un blob de pixels
# source : https://alyssaq.github.io/2015/computing-the-axes-or-orientation-of-a-blob/
# explication : https://en.wikipedia.org/wiki/Image_moment
def get_direction(pixels):
    y, x = np.nonzero(pixels)
    coords = np.vstack([x, y])
    cov = np.cov(coords)
    evalues, evectors = np.linalg.eig(cov)
    sort_indices = np.argsort(evalues)[::-1]
    x_v1, y_v1 = evectors[:, sort_indices[0]]
    y_c, x_c = center_of_mass(pixels)
    x_v2, y_v2 = evectors[:, sort_indices[1]]
    center = np.asarray((x_c, y_c))
    direction1 = np.asarray((x_v1, y_v1))
    direction2 = np.asarray((x_v2, y_v2))
    return center, direction1, direction2


# Chargement et conversion d'image RGBA -> noir et blanc
def load_image(filename):
    
    if platform.startswith("win32"):
        current_directory = '\\'.join(dirname(__file__).split('\\')[:-1])
        print("Current directory: {}".format(join(current_directory)))
        file_loaded = join(current_directory, filename)
    elif platform.startswith("linux") or platform.startswith("cygwin"):
        current_directory = '/'.join(dirname(__file__).split('/')[:-1])
        print("Current directory: {}".format(join(current_directory)))
        file_loaded = join(current_directory, filename)
    elif platform.startswith("darwin"):
        print("Not for MacOs sorry. You can adapt the code here")


    image = Image.open(file_loaded)
    image.load()
    background = Image.new("RGB", image.size, (255, 255, 255))
    background.paste(image, mask=image.split()[3])
    image = background
    image = image.convert('L')
    image = image.point(lambda x: 255 if x < 255 else 0, '1')
    image = np.array(image)
    return image


# Calcul de distance euclidienne entre deux points
def distance_euclidienne(p1, p2):
    return np.linalg.norm(np.subtract(p1, p2))



# source : https://github.com/encukou/bresenham/blob/master/bresenham.py
# explication : https://fr.wikipedia.org/wiki/Algorithme_de_trac%C3%A9_de_segment_de_Bresenham
def bresenham(p0, p1, img, check_value, mode="normal"):
    x0, y0 = p0[0], p0[1]
    x1, y1 = p1[0], p1[1]

    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2 * dy - dx
    y = 0
    new_x, new_y = 0, 0

    list_coor = []

    for x in range(dx + 1):
        new_x, new_y = x0 + x * xx + y * yx, y0 + x * xy + y * yy
        if mode == "recup":
            list_coor.append([new_x, new_y])
        if img[new_y, new_x] == check_value:
            break
        if D >= 0:
            y += 1
            D -= 2 * dx
        D += 2 * dy

    if mode != "recup":
        return new_x, new_y
    else:
        return list_coor


# points : les deux points donnant la direction
# k : coef de proportionalité
# Donne des points en dehors du coeur pour application de l'algorithme de Bresenham
def get_far_points(points, k, origine=[]):
    x_coords, y_coords = zip(*points)
    dir = [x_coords[1] - x_coords[0], y_coords[1] - y_coords[0]]
    # x_coords [0] corresponds au cdg du coeur
    if origine == []:
        new_point = [int(x_coords[0] + dir[0] * k), int(y_coords[0] + dir[1] * k)]
    else:
        new_point = [int(origine[0] + dir[0] * k), int(origine[1] + dir[1] * k)]
    return new_point


# Algorithme reposant sur l'algotithme de bresenham
# Retourne l'axe le plus grand dans la direction (main_dir) donnée
# Balayage sur chaque axe les points du contour pour trouver la plus grande distance
def get_heart_axe(main_dir, perpendicular_dir, origine, img):
    # Choisir un point en dehors du coeur vers le quel se diriger pour trouver le contour
    far_perp_pt1 = get_far_points(perpendicular_dir, 1000)
    far_perp_pt2 = get_far_points(perpendicular_dir, -1000)
    arr1 = bresenham(origine, far_perp_pt1, img, check_value=False, mode="recup")
    arr2 = bresenham(origine, far_perp_pt2, img, check_value=False, mode="recup")
    max_dist1 = max_dist2 = 0
    axe1 = []
    axe2 = []

    for pt in arr1:

        far_pt11 = get_far_points(main_dir, 1000, origine=pt)
        far_pt12 = get_far_points(main_dir, -1000, origine=pt)
        mesure11 = bresenham(pt, far_pt11, img, check_value=False)
        mesure12 = bresenham(pt, far_pt12, img, check_value=False)
        dist1 = distance_euclidienne(mesure11, mesure12)
        if dist1 > max_dist1:
            max_dist1 = dist1
            axe1 = [mesure11, mesure12]

    for pt2 in arr2:

        far_pt21 = get_far_points(main_dir, 1000, origine=pt2)
        far_pt22 = get_far_points(main_dir, -1000, origine=pt2)
        mesure21 = bresenham(pt2, far_pt21, img, check_value=False)
        mesure22 = bresenham(pt2, far_pt22, img, check_value=False)
        dist2 = distance_euclidienne(mesure21, mesure22)

        if dist2 > max_dist2:
            axe2 = [mesure21, mesure22]
            max_dist2 = dist2

    dist1 = distance_euclidienne(axe1[0], axe1[1])
    dist2 = distance_euclidienne(axe2[0], axe2[1])

    if dist1 > dist2:
        return axe1
    else:
        return axe2

# Algorithme reposant sur les produits scalaires
def get_heart_axe_V2(dir1, img, cdg):
    # vecteur direction (doit être entier ou normé)
    a = dir1[0][1] - dir1[1][1]
    b = dir1[0][0] - dir1[1][0]
    ps1 = a * cdg[0] - b * cdg[1]
    ps2 = b * cdg[0] + a * cdg[1]
    # recupere les points du coeurs seulement
    pt_coeur = np.argwhere(img == 1)

    # Initialisation des tableaux à l'infini
    # On estime que le coeur ne fait pas plus de 2000 pixels de large et de haut
    # k0 et k1 les deux "moitiés" du petit axe calculé
    # l0 et l1 les deux "moitiés" du grand axe calculé
    k0 = [float("inf")] * 2000
    k1 = [float("-inf")] * 2000
    l0 = [float("inf")] * 2000
    l1 = [float("-inf")] * 2000

    for y, x in pt_coeur:
        # Calcul des produits scalaires dans des directions diff
        # + 1000 pour s'assurer d'avoir des produits scalaires positifs
        # -ps1 et ps2 pour recentrer au niveau du coeur

        # indice de colonne de calcul du produit scalaire dans le repère du coeur
        k = a * x - b * y + 1000 - ps1
        # indice de ligne de calcul du produit scalaire dans le repère du coeur
        l = b * x + a * y + 1000 - ps2

        # Récupère les projections du point xy sur le  petit axe
        if 0 <= int(l) < 2000:
            k0[int(l)] = min(k0[int(l)], k) # partie gauche (dans le repère du coeur)
            k1[int(l)] = max(k1[int(l)], k) # partie droite (dans le repère du coeur)

        # Récupère les projections du point xy sur le  grand axe
        if 0 <= int(k) < 2000:
            l0[int(k)] = min(l0[int(k)], l) # partie basse (dans le repère du coeur)
            l1[int(k)] = max(l1[int(k)], l) # partie haute (dans le repère du coeur)

    # Récupération des plus grandes distances trouvées et leurs indices
    k0_min, k1_max, indl = get_points_of_heart(k0, k1)
    l0_min, l1_max, indk = get_points_of_heart(l0, l1)

    # On enlève la positivité "artificielle" rajoutée précedemment
    # ainsi que le recentrage, pour obtenir la véritable longueur
    k0_min -= 1000 - ps1
    k1_max -= 1000 - ps1
    l0_min -= 1000 - ps2
    l1_max -= 1000 - ps2
    indl -= 1000 - ps2
    indk -= 1000 - ps1

    # Calcul des coordonnées de tous les points
    x1_k = k1_max * a + b * indl
    y1_k = k1_max * -b + a * indl
    x0_k = k0_min * a + b * indl
    y0_k = k0_min * -b + a * indl
    x1_l = indk * a + b * l1_max
    y1_l = indk * -b + a * l1_max
    x0_l = indk * a + b * l0_min
    y0_l = indk * -b + a * l0_min

    gaxe = [[x1_l, y1_l], [x0_l, y0_l]]
    paxe = [[x0_k, y0_k], [x1_k, y1_k]]

    return paxe, gaxe


# ps = produit scalaire
def get_points_of_heart(ps0, ps1):
    ps = []
    for i in range(len(ps0)):
        ps.append(ps1[i] - ps0[i])
    psmax = np.argmax(ps)
    # print("psmax", psmax)
    return ps0[psmax], ps1[psmax], psmax
