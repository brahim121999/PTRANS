import torch
from PIL import Image
from model.unet_model import UNet
from torchvision import transforms
import matplotlib.pyplot as plt
import numpy as np
from os.path import join, dirname
from sys import platform

def splitBatchSize(input_w, input_h, MAX_RAM):
    """ Détermination de la taille idéale de découpe d'image """
    div = 1
    # Check batch size < max size batch
    while (input_w // div) *  (input_h // div) > MAX_RAM :
        div += 1

    batch_w, batch_h =  input_w // div, input_h // div
    return batch_w, batch_h

def grayscale(path):
    """ Transformation RGBA en niveaux de gris """
    image = Image.open(path)
    image.load()
    background = Image.new("RGB", image.size, (255, 255, 255))
    background.paste(image, mask=image.split()[3])
    image = background
    image = image.convert('L')

    ret = np.array(image)
    ret[ret == 255] = 0
    ret[ret == 150] = 255
    return ret


def predict(input, model, device):
    MAX_RAM = 500*500
    """
    Même principe que la boucle de validation dans train.py, mais on
    garde en mémoire chaque batch d'image pour les reformer ensuite
    """

    with torch.no_grad():

        input_w, input_h = input.size()[3], input.size()[2]
        batch_w, batch_h = splitBatchSize(input_w, input_h, MAX_RAM)
        batch = input[:, :, 0:batch_h, 0:batch_w]
        input_batch = input[:, :, 0:batch_h, 0:batch_w]

        output = model(batch)
        output_w, output_h = output.size()[3], output.size()[2]

        centerTransform = transforms.CenterCrop((output_h, output_w))
        input_part = centerTransform(input_batch)

        diff_width, diff_height = batch_w - output_w, batch_h - output_h
        diff_left, diff_top =  diff_width // 2, diff_height // 2

        current_x, current_y = batch_w - diff_width, 0
        nb_batches = 1
        output_matrix = list()
        input_matrix = list()
        while current_y + batch_h  < input_h:
            print(nb_batches)
            current_x = 0
            new_row = list()
            new_row_input = list()
            if nb_batches == 1:
                new_row.append(output)
                new_row_input.append(input_part)
                current_x  = batch_w - diff_width
            while current_x + batch_w  < input_w:
                batch = input[:, :,
                 current_y:(batch_h + current_y),
                 current_x:(batch_w +current_x)]
                input_batch = input[:, :,
                  current_y:(batch_h + current_y),
                  current_x:(batch_w +current_x)]
                input_part = centerTransform(input_batch)


                output = net(batch)
                new_row.append(output)
                new_row_input.append(input_part)


                current_x += batch_w - diff_width
                nb_batches += 1
            current_y += batch_h - diff_height
            concat = torch.cat(new_row, dim=3)
            concat_input = torch.cat(new_row_input, dim=3)
            output_matrix.append(concat)
            input_matrix.append(concat_input)
        predicted_segmentation = torch.cat(output_matrix, dim=2)
        built_input = torch.cat(input_matrix, dim=2)

        for i in range(0,4):
            predicted_segmentation[0][i][predicted_segmentation[0][i] <= 0] = 0
            predicted_segmentation[0][i][predicted_segmentation[0][i] > 0] = 255

        return predicted_segmentation, built_input




if __name__ == "__main__":
    """ Test de prédiction sur une image de chien """

    

    if platform.startswith("win32"):
        path_loaded = "data\\Verite_terrain\\Chiens\\{}\\20180316122722.012345.18_processed.png"
        current_directory = '\\'.join(dirname(__file__).split('\\')[:-1])
        print("Current directory: {}".format(join(current_directory)))
        path = join(current_directory, path_loaded)

        # Loading the saved model
        save_path = join(current_directory, 'output\\Apprentissage_8\\best_model.pt')
    elif platform.startswith("linux") or platform.startswith("cygwin"):
        path_loaded = "data/Verite_terrain/Chiens/{}/20180316122722.012345.18_processed.png"
        current_directory = '/'.join(dirname(__file__).split('/')[:-1])
        print("Current directory: {}".format(join(current_directory)))
        path = join(current_directory, path_loaded)

        # Loading the saved model
        save_path = join(current_directory, 'output/Apprentissage_8/best_model.pt')
    
    elif platform.startswith("darwin"):
        print("Not for MacOs sorry. You can adapt the code here")

    image = Image.open(path.format("Radios"))

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    grayscale_transform = transforms.Compose([transforms.Grayscale(num_output_channels=1),
                                              transforms.ToTensor()])
    image = grayscale_transform(image).unsqueeze(0)

    heart_mask = grayscale(path.format("Coeur"))
    vtb_mask = grayscale(path.format("Vertebres"))
    process_mask = grayscale(path.format("Process_epineux"))

    # Loading the saved model
    # save_path = '../output/Apprentissage_8/best_model.pt'
    # net = UNet(1, 4, bilinear=False)
    net = UNet(1, 4)
    net.load_state_dict(torch.load(save_path, map_location=device))
    net.eval()

    prediction, rebuilt_input = predict(image, net, device)

    plt.figure()
    plt.subplot(1,3,1)
    plt.title("Unet 4 channels output")
    plt.imshow(prediction[0][1:4].permute(1,2,0))
    plt.subplot(1,3,2)
    plt.title("Original input")
    plt.imshow(image[0].permute(1,2,0), cmap='gray')
    plt.subplot(1,3,3)
    plt.title("UNet output view of input")
    plt.imshow(rebuilt_input[0].permute(1,2,0), cmap='gray')

    plt.figure()
    for i in range(1, 4):
        plt.subplot(2,3,i)
        mask = prediction[0][i]
        plt.imshow(mask)
    plt.subplot(2,3,4)
    plt.imshow(heart_mask)
    plt.subplot(2,3,5)
    plt.imshow(vtb_mask)
    plt.subplot(2,3,6)
    plt.imshow(process_mask)
    plt.show()
