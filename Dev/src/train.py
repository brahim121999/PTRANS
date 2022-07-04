""" Boucle d'apprentissage du réseau """

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, sampler
from torchvision import transforms
from dataset.dataset import RadioDataset
from model.model import Network
from model.unet_model import UNet
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy
import time
import os

def plotCurve(nb_sample_array,train_err_array,nb_epoch, val_err_array, start_time):
    """ Création courbe apprentissage """
    plt.figure()
    plt.plot(nb_sample_array, train_err_array, 'b', label='train_error')
    plt.plot(nb_sample_array, val_err_array, 'r', label='valid_error')
    plt.legend()
    fig = plt.gcf()
    fig.suptitle("{} époques, best validation loss : {}, time : {}".format(nb_epoch, best_val_loss, time.time() - start_time))
    plt.savefig("../output/loss.png", dpi=300)
    plt.close()

def splitBatchSize(input_w, input_h, MAX_RAM):
    """ Détermination de la taille idéale de découpe d'image """

    div = 1
    while (input_w // div) *  (input_h // div) > MAX_RAM :
        div += 1

    batch_w, batch_h =  input_w // div, input_h // div
    return batch_w, batch_h


def trainingValidationLoop(data, optimizer, criterion, net, Training=True):
    """ Boucle de validation et d'apprentissage """
    # erreur de coût de l'input en cours
    current_input_loss = 0.0

    # Récupération de l'input et de la vérité terrain
    input, masks = data
    input, masks = input.to(device), masks.to(device)

    # Mise à zéro des paramètres du gradient
    optimizer.zero_grad()

    # Calcul de la taille de l'input et d'une taille de découpe idéale
    # Format des tensor pytorch : (Batch, Channels, HEIGHT, WIDTH)
    input_w, input_h = input.size()[3], input.size()[2]
    batch_w, batch_h = splitBatchSize(input_w, input_h, MAX_RAM)

    # Découpe de l'input  à partir de la taille idéale calculée
    batch = input[:, :, 0:batch_h, 0:batch_w]

    # Prédiction du batch découpé de l'image
    output = net(batch)

    # Calcul taille d'une prédiction du réseau sur un batch
    output_w, output_h = output.size()[3], output.size()[2]

    # Préparation outil de crop de tensor
    # Permet de découper la vérité terrain en fonction de la taille de prédiction
    centerTransform = transforms.CenterCrop((output_h, output_w))

    # Découpe de la vérité terrain associée à la sortie du réseau
    gt_mask = centerTransform(masks[:, 0:batch_h, 0:batch_w])

    # Apprentissage du réseau
    loss = criterion(output, gt_mask.long())
    if Training:
        loss.backward()
        optimizer.step()
    current_input_loss += loss.item()

    # Calcul différence de taille input/ouput
    diff_width, diff_height = batch_w - output_w, batch_h - output_h
    # Calcul différence à gauche et en haut input/output pour déplacement
    diff_left, diff_top =  diff_width // 2, diff_height // 2

    """
    On découpe l'image ligne par ligne. On avance donc à chaque fois de la
    taille d'un batch moins la différence entre un batch et sa Prédiction
    associée afin de ne pas perdre de données d'apprentissages.
    On commence à zéro
    """
    # On prend en compte la première découpe
    current_x, current_y = batch_w - diff_width, 0

    # tracking nombre de batches de l'image pour calculer erreur de predction
    nb_batches = 1
    # Découpe de l'image ligne par ligne
    while current_y + batch_h  < input_h:
        while current_x + batch_w  < input_w:
            batch = input[:, :,
             current_y:(batch_h + current_y),
             current_x:(batch_w +current_x)]
            gt_mask = centerTransform(masks[:,
              current_y:(batch_h + current_y),
              current_x:(batch_w +current_x)])

            output = net(batch)
            loss = criterion(output, gt_mask.long())
            if Training:
                loss.backward()
                optimizer.step()

            current_input_loss += loss.item()
            current_x += batch_w - diff_width
            nb_batches += 1
        current_y += batch_h - diff_height
    return current_input_loss / nb_batches

# Détection de la présence d'un GPU pour les calculs
use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
print("Device used by pytorch : ", device)

'''
Si NNPACK ne peut pas être initialisé, décommenter cette ligne.
'''

# Création du dataset
fullDataset = RadioDataset()
dataLength = len(fullDataset)
trainPercentage = 0.8
trainPart = int(trainPercentage * dataLength)
validpart = dataLength - trainPart

print("Size of dataset : ", dataLength)
print("Size of Trainset : ", trainPart)
print("Size of ValidSet : ", validpart)

# Répartition du dataset (apprentissage et validation)
trainset, validationset, _ignored = torch.utils.data.random_split(
    fullDataset, [trainPart, validpart, dataLength - trainPart - validpart])

# Création du réseau (1 canal entrée et 4 en sortie (3 classes + background))
net = UNet(1, 4)
net.to(device)

# Tableaux de suivi d'apprentissage et de validation pour création de courbe
val_err_array = np.array([])
train_err_array = np.array([])
nb_sample_array = np.array([])

# Meilleures résultats du modèle
best_val_loss = 1000000
best_model =  copy.deepcopy(net)
best_train_loss = 1000000

# Meta paramètres
minibatch_size = 1
learning_rate = 0.001
print_every = 100
nb_epoch = 160
MAX_RAM = 850*850 # Nombre de pixels que peut supporter la RAM pour apprentissage

print("Metaparametres : ")
print("minibatch_size : ", 1)
print("learning_rate : ", 0.001)
print("print_every : ", print_every)
print("nb_epoch : ", nb_epoch)
print("MAX_RAM : ", np.sqrt(MAX_RAM))

# Fonction de coût utilisée et algorithme d'optimisation
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=learning_rate, momentum=0.9)

# Création des loader de datasets
trainloader = DataLoader(trainset, batch_size=minibatch_size, shuffle=True, num_workers=0)
validloader = DataLoader(validationset, batch_size=minibatch_size, shuffle=True, num_workers=0)

start_time = time.time()

# Garde en mémoire le nombre d'inputs fournis au réseau
nb_used_sample = 0

# Erreur de prédiction d'apprentissage entre chaque validation
running_loss = 0.0

for epoch in range(nb_epoch):  # Itération du dataset plusieurs fois

    for i, data in enumerate(trainloader, 0): # Itération dataset apprentissage

        input_loss = trainingValidationLoop(data, optimizer, criterion, net)

        nb_used_sample += minibatch_size
        running_loss += input_loss

        """
        La boucle de validation fonctionne de la même façon que celle d'apprentissage
        La différence est que l'on ne fait pas de rétropropagation pour apprentissage
        """
        if nb_used_sample % (print_every * minibatch_size) == 0:
            train_err = (running_loss / (print_every * minibatch_size))
            running_loss = 0.0
            totalValLoss = 0.0

            with torch.no_grad():
                for data in validloader:
                    input_loss = trainingValidationLoop(data, optimizer, criterion, net, Training=False)
                    totalValLoss += input_loss

            val_err = (totalValLoss / len(validationset))
            train_err_array = np.append(train_err_array, train_err)
            val_err_array = np.append(val_err_array, val_err)
            nb_sample_array = np.append(nb_sample_array, nb_used_sample)

            # Sauvegarde du meilleur modèle
            if best_val_loss > val_err :
                best_model =  copy.deepcopy(net)
                torch.save(best_model.state_dict(), "../output/Apprentissage_8/best_model.pt")
                best_val_loss = val_err
                best_train_loss = train_err
    plotCurve(nb_sample_array,train_err_array,nb_epoch, val_err_array, start_time)

print('Finished Training in {}s'.format(time.time() - start_time))
print("Train error array : ", train_err_array)
print("Validation error array : ", val_err_array)
print("Sample  array : ", nb_sample_array)
plotCurve(nb_sample_array,train_err_array,nb_epoch, val_err_array, start_time)
