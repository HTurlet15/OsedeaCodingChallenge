import cv2
import os

class EdgeDetector:
    def __init__(self, image_folder):
        self.image_folder = image_folder

    def count_edges(self, image_path):
        image = cv2.imread(image_path, 0)
        edges = cv2.Canny(image, 100, 200)
        return cv2.countNonZero(edges)

    def find_most_edges_image(self):
        edges_count = {img: self.count_edges(os.path.join(self.image_folder, img)) 
                       for img in os.listdir(self.image_folder)}
        most_edges_image = max(edges_count, key=edges_count.get)
        return most_edges_image
    