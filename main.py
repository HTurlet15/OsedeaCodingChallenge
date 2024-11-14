from edge_detector import EdgeDetector
from blue_analyzer import BlueAnalyzer
from thermal_visualizer import ThermalVisualizer
import os

# Dossier de sortie pour les fichiers générés
output_folder = "output"
if not os.path.exists(output_folder):
            os.makedirs(output_folder)

# Configurations
image_folder = 'images/'
thermal_file = 'data/thermal-data.raw'
# 1. Edge detection
edge_detector = EdgeDetector(image_folder)
print("Image avec le plus d'arêtes :", edge_detector.find_most_edges_image())

# 2. Blue analyze of images
blue_analyzer = BlueAnalyzer(image_folder)
print("Image avec le plus de bleu :", blue_analyzer.find_most_blue_image())
blue_analyzer.plot_color_channels(output_folder)
blue_analyzer.save_color_channels(output_folder)

# 3. Thermal Visualisation
# J'ai supposé que l'image thermique avait été prise avec Spot, et je me suis donc
# servi de la documentation afin d'avoir des informations sur la taille et les données du .raw
# Selon la documentation, on a alors :
# The raw thermal data from the Spot CAM+IR contains 327,680 (640x512) 16-bit unsigned values. 
# Each value describes a temperature in units of decikelvin.
thermal_visualizer = ThermalVisualizer(thermal_file, width=640, height=512)
thermal_visualizer.load_data()
thermal_visualizer.show_image(output_folder)