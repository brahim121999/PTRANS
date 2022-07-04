from torch.utils.data import Dataset, DataLoader, sampler
import numpy as np
import torch
import matplotlib.pyplot as plt
from torchvision import transforms
from PIL import Image, ImageOps
from torchvision.utils import save_image
import matplotlib.image as mpimg
from pathlib import Path
import os
import sys
import glob


class RadioDataset(Dataset):
    def __init__(self):
        super().__init__()

        # Chemins des dossiers de la vérité terrain
        ROOT = self.get_project_root(os.path.dirname(os.path.abspath(__file__)))
        INPUTS_DIR = 'data/'
        GROUND_TRUTH = 'Verite_terrain/'
        DOG_PATH = 'Chiens/'
        CAT_PATH = 'Chats/'
        RADIOS = 'Radios/'
        HEART_MASKS = 'Coeur/'
        VTB_MASKS = 'Vertebres/'
        PROCESS_MASKS = 'Process_epineux/'

        # Récupération et stockage des chemins des fichiers
        dog_radios = glob.glob(ROOT + INPUTS_DIR + GROUND_TRUTH + DOG_PATH + RADIOS + '*')
        cat_radios = glob.glob(ROOT + INPUTS_DIR + GROUND_TRUTH + CAT_PATH + RADIOS + '*')

        dog_hearts = glob.glob(ROOT + INPUTS_DIR + GROUND_TRUTH + DOG_PATH + HEART_MASKS + '*')
        cat_hearts = glob.glob(ROOT + INPUTS_DIR + GROUND_TRUTH + CAT_PATH + HEART_MASKS + '*')

        dog_vtb = glob.glob(ROOT + INPUTS_DIR + GROUND_TRUTH + DOG_PATH + VTB_MASKS + '*')
        cat_vtb = glob.glob(ROOT + INPUTS_DIR + GROUND_TRUTH + CAT_PATH + VTB_MASKS + '*')

        dog_prc = glob.glob(ROOT + INPUTS_DIR + GROUND_TRUTH + DOG_PATH + PROCESS_MASKS + '*')
        cat_prc = glob.glob(ROOT + INPUTS_DIR + GROUND_TRUTH + CAT_PATH + PROCESS_MASKS + '*')

        self.radios_arr = dog_radios + cat_radios
        self.heart_arr = dog_hearts + cat_hearts
        self.vtb_arr = dog_vtb + cat_vtb
        self.process_arr = dog_prc + cat_prc
        self.data_len = len(self.radios_arr)
        print("GROUND_TRUTH FOUND : ", self.data_len)

    def __getitem__(self, idx):
        """
        Fonction obligatoire utilisée par le loader lors de l'itération du dataset
        Récupération du chemin et chargement de la vérité terrain puis labellisation
        """
        grayscale_transform = transforms.Compose([transforms.Grayscale(num_output_channels=1),
                                                  transforms.ToTensor()])
        tensor_transform = transforms.ToTensor()

        radio_img = Image.open(self.radios_arr[idx])
        radio = grayscale_transform(radio_img)


        heart_mask = self.grayscale(self.heart_arr[idx])
        vtb_mask = self.grayscale(self.vtb_arr[idx])
        process_mask = self.grayscale(self.process_arr[idx])

        heart_mask[heart_mask == 150] = 1
        vtb_mask[vtb_mask == 150] = 2
        process_mask[process_mask == 150] = 3
        masks = np.zeros_like(heart_mask)
        masks[heart_mask == 1] = 1
        masks[vtb_mask == 2] = 2
        masks[process_mask == 3] = 3

        """
        Utiliser from_numpy plutôt que toTensor permet de ne pas normaliser les
        données afin de respecter la labellisation des classes par 0, 1, 2 et 3
        """
        return radio, torch.from_numpy(masks)


    def __len__(self):
        """
        Méthode nécessaire au loader qui retourne le
        nombre de données dans le dataset
        """
        return self.data_len


    def get_project_root(self, path):
        """
        Récupération de la racine de dev du projet
        """
        while os.path.basename(path) != 'Dev':
            path = os.path.dirname(path)
        return path + "/"


    def grayscale(self, path):
        image = Image.open(path)
        image.load()
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
        image = background
        image = image.convert('L')
        return np.array(image)




if __name__ == "__main__":
    test = RadioDataset()
    plt.figure()
    plt.imshow(test[0]['radio'].permute(1, 2, 0))
    print(test[0]['vtb'].shape)
    plt.figure()
    plt.imshow(test[0]['vtb'].permute(1, 2, 0))
    plt.figure()
    plt.imshow(test[0]['heart'].permute(1, 2, 0))
    plt.figure()
    plt.imshow(test[0]['processus'].permute(1, 2, 0))
    plt.show()

    t = test[0]
    # print(t)
    #plt.imshow(t[1][..., 0])
    plt.show()
