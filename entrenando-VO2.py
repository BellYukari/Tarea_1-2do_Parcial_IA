import cv2
import os
import numpy as np

dataPath = 'rostros'
personas = os.listdir(dataPath)

print("Personas encontradas:", personas)
facesData = []
labels = []
label = 0

for persona in personas:
    personPath = os.path.join(dataPath, persona)
    for archivo in os.listdir(personPath):
        ruta_imagen = os.path.join(personPath, archivo)
        img = cv2.imread(ruta_imagen, 0)  # Escala de grises
        if img is None:
            print(f"Error leyendo imagen: {ruta_imagen}")
            continue
        facesData.append(img)
        labels.append(label)
    label += 1

if len(facesData) == 0:
    print("No se encontraron imágenes para entrenar.")
    exit()

print("Entrenando modelo...")
modelo = cv2.face.LBPHFaceRecognizer_create()  # Más robusto que EigenFaces
modelo.train(facesData, np.array(labels))
modelo.write('modelo.xml')

print("Modelo entrenado y guardado como 'modelo.xml'")