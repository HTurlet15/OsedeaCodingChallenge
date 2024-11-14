import matplotlib.pyplot as plt
import cv2
import numpy as np
import os

class BlueAnalyzer:
    def __init__(self, image_folder):
        self.image_folder = image_folder

    def get_color_channels(self, image_path):
        image_rgb = cv2.imread(image_path)
        blue_channel, green_channel, red_channel = cv2.split(image_rgb)
        return blue_channel, green_channel, red_channel

    def count_blue(self,image_path):
        blue_channel = self.get_color_channels(image_path)[0]
        return blue_channel.sum()

    def find_most_blue_image(self):
        blue_count = {img: self.count_blue(os.path.join(self.image_folder, img)) 
                       for img in os.listdir(self.image_folder)}
        most_blue_image = max(blue_count, key=blue_count.get)
        return most_blue_image
    
    def plot_color_channels(self, output_folder):
        # Sauvegarde de la quantité de bleu de chaque image
        blue_count = {img: self.count_blue(os.path.join(self.image_folder, img)) 
                       for img in os.listdir(self.image_folder)}
        # Affiche les histogrammes pour chaque canal de bleu
        plt.bar(blue_count.keys(), blue_count.values(), log = True, color ='blue', width = 0.4)
        plt.xlabel("Images")
        plt.ylabel("Quantity of blue pixels")
        plt.title("Quantity of blue for each image")
        plt.savefig(os.path.join(output_folder, "blue_quantity.png"))

    def save_color_channels(self,output_folder):
        # Créer le dossier de sortie s'il n'existe pas
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for image in os.listdir(self.image_folder):
            image_path = os.path.join(self.image_folder, image)
            # Lire l'image et extraire les canaux
            image = cv2.imread(image_path)
            blue_channel, green_channel, red_channel = cv2.split(image)

            # Crée une image vide pour chaque canal
            zeros = np.zeros_like(blue_channel)

            # Images des canaux de couleur
            blue_image = cv2.merge([blue_channel, zeros, zeros])
            green_image = cv2.merge([zeros, green_channel, zeros])
            red_image = cv2.merge([zeros, zeros, red_channel])

            # Noms des fichiers de sortie basés sur le nom de l'image d'entrée
            base_filename = os.path.splitext(os.path.basename(image_path))[0]
            cv2.imwrite(os.path.join(output_folder, f"{base_filename}_blue.png"), blue_image)
            cv2.imwrite(os.path.join(output_folder, f"{base_filename}_green.png"), green_image)
            cv2.imwrite(os.path.join(output_folder, f"{base_filename}_red.png"), red_image)

            print(f"Canaux de couleur enregistrés pour {base_filename} dans {output_folder}")