from postprocess.coeur import find_hrt_axes
from postprocess.t4 import find_t4
from dicom.dicom import createDicomFile
import time

def calcul_indice(vtb_filename, prc_filename, hrt_filename, plot):
    t4 = find_t4(vtb_filename, prc_filename, left=True, plot=plot)
    hrt_axes, hrt_points = find_hrt_axes(hrt_filename, plot)

    createDicomFile(hrt_points[0],hrt_points[1],[t4[1],t4[2]])
    indice = (hrt_axes[0]+hrt_axes[1])/t4[0]

    print("Taille de t4 : ", t4)
    print("Taille Grand Axe : \n", hrt_axes[0], "\nTaille Petit axe : \n", hrt_axes[1])

    return indice

if __name__ == "__main__":
    start_time = time.time()
    p_f = "postprocess/process.png"
    v_f = "postprocess/wrong_vtb2.png"
    h_f = "postprocess/coeur4.png"

    indice_buchanan = calcul_indice(vtb_filename=v_f, prc_filename=p_f, hrt_filename=h_f, plot=True)
    print("indice de buchanan", indice_buchanan)

    print("--- %s seconds ---" % (time.time() - start_time))
