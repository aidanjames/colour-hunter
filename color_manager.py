from sklearn.cluster import KMeans
import cv2
from collections import Counter
import numpy as np


class ColorManager:

    def rgb_to_hex(self, color):
        return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

    def get_colors(self, image_data, number_of_colors):
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), -1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        modified_image = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)
        modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)
        clf = KMeans(n_clusters=number_of_colors)
        labels = clf.fit_predict(modified_image)
        counts = Counter(labels)
        center_colors = clf.cluster_centers_
        ordered_colors = [center_colors[i] for i in counts.keys()]
        hex_colors = [self.rgb_to_hex(ordered_colors[i]) for i in counts.keys()]
        return hex_colors

