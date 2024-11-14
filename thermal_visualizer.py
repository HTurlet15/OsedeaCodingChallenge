# thermal_visualizer.py
import numpy as np
import matplotlib.pyplot as plt
import os

class ThermalVisualizer:
    def __init__(self, file_path, width, height):
        self.file_path = file_path
        self.width = width
        self.height = height
        self.endianness = '>' # '>' For big-endian and '<' for little-endian (Documentation Spot)
    
    def load_data(self):
        # Charge les données en décikelvin depuis un fichier binaire
        with open(self.file_path, 'rb') as f:
            buffer = f.read()
        deciKelvin_data = np.frombuffer(buffer, dtype=f'{self.endianness}u2').reshape((int(self.height), int(self.width)))
        #Conversion en Celsius et stockage dans celsius_data
        self.celsius_data = deciKelvin_data / 10 - 273

    def show_image(self, output_folder):
        # Affiche celsius_data sous forme d'image thermique en couleurs
        if self.celsius_data is None:
            raise ValueError("Data not loaded")
        image = list(self.celsius_data)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        plt.figure()
        plt.imshow(image, plt.cm.inferno)
        plt.title("Image thermique")
        plt.colorbar(label='Temperature (°C)')  
        plt.savefig(os.path.join(output_folder, "image_thermique.png"))
        plt.close()