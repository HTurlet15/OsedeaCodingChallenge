# Coding Challenge - Python/Computer Vision

## Practical
You will find in this folder 4 different scripts :
1. edge_detector.py : contains a class EdgeDetector to determine which image in `images/` contains the most edges. The answer will appear in the terminal
2. blue_analyzer.py : contains a class BlueAnalyzer to plot the colour channels for each image in `images/` to determine which image contains the most blue. The result will appear in the terminal (for the most blue image) and the details will be in the folder `output/` (the color channels for each image and the histogram of quantity of blue for each image)
3. thermal_visualizer.py : contains a class ThermalVisualizer to visualise the `thermal-data.raw` file with the temperature range (in Celsius). The outputted image will be in the folder `output/`.

For these scripts, we would like to be able to see the results by running something like:*
The results can be seen by running the commands :

```
docker build -t python-vision .
docker run -v $PWD/output:/app/output python-vision
```

while being located in the folder `Coding challenge/`.

## Theory

For the following, write down how you would approach the following problems:

1. Using computer vision, read an analogue gauge (as photographed in `imagesDSC06071-1200x800-5b2df79.jpg`)

Pour lire un manomètre analogique à l’aide de la vision par ordinateur, on suit plusieurs étapes pour détecter et interpréter précisément la position de l’aiguille. La première étape consiste à améliorer le contraste et la clarté de l'image pour mieux voir les éléments importants. Pour cela, on convertit l’image en niveaux de gris avec cv2.cvtColor(), on applique un flou gaussien avec cv2.GaussianBlur() pour réduire le bruit, puis on utilise cv2.Canny() pour détecter les contours du cadran, de l’aiguille, et des repères de graduation. Une fois le cadran localisé, on utilise cv2.HoughCircles() pour détecter sa forme circulaire et obtenir son centre et son rayon, ce qui nous permet de focaliser l’analyse sur cette zone. Ensuite, pour détecter l’aiguille, on limite la recherche à la zone du cadran et applique cv2.HoughLinesP(), qui identifie les lignes droites. Parmi les lignes détectées, on sélectionne celle qui semble la plus longue ou la plus proéminente, qui correspond généralement à l’aiguille orientée du centre vers le bord du cadran.

Avec l’aiguille détectée, la prochaine étape consiste à calculer son angle par rapport à un point de référence (par exemple, un axe horizontal). En utilisant math.atan2 ou np.arctan2, on peut déterminer cet angle avec précision. Ensuite, on le convertit en degrés grâce à np.degrees() pour le faire correspondre à l’échelle du cadran : par exemple, un cadran semi-circulaire ira de 0 à 180 degrés, tandis qu’un cadran complet couvrira de 0 à 360 degrés. Ce calcul de l'angle est ensuite transformé en une lecture de mesure sur l’échelle du manomètre : par exemple, pour un cadran semi-circulaire dont le 180 degrés serait 9 PSI, on saurait que un angle de 120 degrés serait égal à 120/180 * 9 PSI, soit 2/3 de 9 PSI soit 6 PSI.

2. As a bonus: using the Spot SDK documentation, determine how you display live sensor data in the Spot app

On peut récupérer les images du robot Sport assez simplement grâce aux API du robot. Grâce à la documentation et à des lignes de codes similaires à celle ci-dessous :
```{python}
from bosdyn.client import create_standard_sdk
from bosdyn.client.robot import Robot
from bosdyn.client.image import ImageClient
# Initialisation
sdk = create_standard_sdk('SpotImageDisplay')
robot = sdk.create_robot('id.du.rob.ot')  # Remplacez par l'adresse IP de Spot
robot.authenticate('user', 'password')    # Utilisez vos identifiants
# Accès aux images
image_client = robot.ensure_client(ImageClient.default_service_name)
sources = image_client.list_image_sources()
image_response = image_client.get_image_from_sources(['frontleft_fisheye_image'])  # Exemple de caméra
```

Ensuite, on peut faire une boucle sur image_response pour obtenir en continue les informations de la caméra choisie. On peut les afficher avec cv2. Pour que le flux en direct soit accessible sur le Spot App, ce flux doit être ensuite enregistré comme un service gRPC au niveau du Spot Directory Service, ce qui permet à l’application Spot de découvrir et accéder au service. Cela marche aussi pour d'autres types de data, ici j'ai pris l'exemple de la caméra avant gauche (en fisheye), mais ce serait la même chose avec la batterie ou autre.
