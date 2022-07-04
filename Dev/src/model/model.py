""" Ancien modèle créé à la main """

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import numpy
import sys, os


class Network(nn.Module):
    def down_block(self, in_c, out_c, kernel_size=3):
        block = nn.Sequential(
            nn.Conv2d(in_channels=in_c, out_channels=out_c,
                      kernel_size=kernel_size, stride=1),
            nn.BatchNorm2d(out_c),
            nn.ReLU(),
            nn.Conv2d(in_channels=out_c, out_channels=out_c,
                      kernel_size=kernel_size, stride=1),
            nn.BatchNorm2d(out_c),
            nn.ReLU()
        )
        return block

    def up_block(self, in_c, mid_c, out_c, kernel_size=3):
        block = torch.nn.Sequential(
            torch.nn.Conv2d(kernel_size=kernel_size, in_channels=in_c, out_channels=mid_c, stride=1),
            nn.BatchNorm2d(mid_c),
            torch.nn.ReLU(),
            torch.nn.Conv2d(kernel_size=kernel_size, in_channels=mid_c, out_channels=mid_c, stride=1),
            nn.BatchNorm2d(mid_c),
            torch.nn.ReLU(),
            torch.nn.ConvTranspose2d(in_channels=mid_c, out_channels=out_c, kernel_size=2, stride=2)
        )
        return block

    def final_block(self, in_c, mid_c, out_c, kernel_size=3):
        block = torch.nn.Sequential(
            torch.nn.Conv2d(kernel_size=kernel_size, in_channels=in_c, out_channels=mid_c, padding=0, stride=1),
            nn.BatchNorm2d(mid_c),
            torch.nn.ReLU(),
            torch.nn.Conv2d(kernel_size=kernel_size, in_channels=mid_c, out_channels=mid_c, padding=0, stride=1),
            nn.BatchNorm2d(mid_c),
            torch.nn.ReLU(),
            torch.nn.Conv2d(kernel_size=1, in_channels=mid_c, out_channels=out_c, stride=1)#,
            #torch.nn.ReLU()
        )
        return block

    def copy_features(self, target_tensor, contracting_tensor):
        target_height = target_tensor.size()[2]
        target_width = target_tensor.size()[3]

        crop = transforms.CenterCrop((target_height, target_width))

        contracting_tensor = crop(contracting_tensor)


        return torch.cat((target_tensor, contracting_tensor), 1)



    def __init__(self):
        super(Network, self).__init__()

        self.conv_contract_1 = self.down_block(in_c=1, out_c=64)
        self.max_pool_1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv_contract_2 = self.down_block(in_c=64, out_c=128)
        self.max_pool_2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv_contract_3 = self.down_block(in_c=128, out_c=256)
        self.max_pool_3 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv_contract_4 = self.down_block(in_c=256, out_c=512)
        self.max_pool_4 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.mid_block = torch.nn.Sequential(
            torch.nn.Conv2d(kernel_size=3, in_channels=512, out_channels=1024, stride=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(kernel_size=3, in_channels=1024, out_channels=1024, stride=1),
            torch.nn.ReLU(),
            torch.nn.ConvTranspose2d(in_channels=1024, out_channels=512,
                                     kernel_size=2, stride=2)
        )
        self.conv_expans_1 = self.up_block(in_c=1024, mid_c=512, out_c=256)
        self.conv_expans_2 = self.up_block(in_c=512, mid_c=256, out_c=128)
        self.conv_expans_3 = self.up_block(in_c=256, mid_c=128, out_c=64)
        self.final = self.final_block(in_c=128, mid_c=64, out_c=4)

    def forward(self, x):
        contract_block_1 = self.conv_contract_1(x)
        contract_pool_1 = self.max_pool_1(contract_block_1)
        contract_block_2 = self.conv_contract_2(contract_pool_1)
        contract_pool_2 = self.max_pool_2(contract_block_2)
        contract_block_3 = self.conv_contract_3(contract_pool_2)
        contract_pool_3 = self.max_pool_3(contract_block_3)
        contract_block_4 = self.conv_contract_4(contract_pool_3)
        contract_pool_4 = self.max_pool_4(contract_block_4)
        mid_block = self.mid_block(contract_pool_4)
        x = self.copy_features(mid_block, contract_block_4)
        x = self.conv_expans_1(x)
        x = self.copy_features(x, contract_block_3)
        x = self.conv_expans_2(x)
        x = self.copy_features(x, contract_block_2)
        x = self.conv_expans_3(x)
        x = self.copy_features(x, contract_block_1)
        final = self.final(x)
        return final


# Outil de debug pour voir si la découpe d'images se passe bien
def createRectangle(w, h, x, y, c='r'):
    rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=c, facecolor='none')
    return rect

# Test de découpe d'image et affichage de la découpe
if __name__ == "__main__":

    # tensor : (Channels, HEIGHT, WIDTH)
    WIDTH = 1000
    HEIGHT = 700
    test_image = torch.rand(1, 1, HEIGHT, WIDTH)

    fig, ax = plt.subplots()
    ax.imshow(test_image[0].permute(1,2,0))

    model = Network()
    #x = model(test_image)

    im_w, im_h = test_image.size()[3], test_image.size()[2]
    max_ram = 450 * 450
    div = 1

    while (im_w // div) *  (im_h // div) > max_ram :
        div += 1

    batch_w, batch_h =  im_w // div, im_h // div
    batch = test_image[:, :, 0:batch_h, 0:batch_w]

    output = model(batch)
    output_size = output.size()
    print("output_size  found : ", output_size)
    diff_left = (batch_w - output_size[3])
    diff_top = (batch_h - output_size[2])

    current_x, current_y = batch_w - diff_left, 0

    ax.add_patch(createRectangle(batch_w, batch_h, 0, 0))
    ax.add_patch(createRectangle(output_size[3], output_size[2],
                                diff_left//2,
                                diff_top//2, c='b'))
    while current_y + batch_h  < im_h:

        current_x = 0
        while current_x + batch_w  < im_w:
            batch = test_image[:, :,
            current_y:(batch_h + current_y),
             current_x:(batch_w +current_x)
             ]
            ax.add_patch(createRectangle(batch_w, batch_h, current_x, current_y))
            ax.add_patch(createRectangle(output_size[3], output_size[2],
                                        current_x + diff_left//2,
                                        current_y + diff_top//2, c='b'))

            output = model(batch)

            print("output_size  found : ", output.size())
            current_x += batch_w - diff_left
        current_y += batch_h - diff_top
        print("Current_x : {}, Im_width : {}, End new batch : {}".format(current_x, im_w, current_x + batch_w))
    plt.show()
