import cv2 # type: ignore
import os

nombre = 'Owen'  # Cambiar por el nombre correspondiente
ruta_absoluta = os.path.abspath(f'rostros/{nombre}')

if not os.path.exists(ruta_absoluta):
    os.makedirs(ruta_absoluta)
    print(f'Carpeta creada: {ruta_absoluta}')
else:
    print(f'Carpeta ya existe: {ruta_absoluta}')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
count = 0

print("Iniciando captura... Presiona ESC o captura 30 rostros.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al recibir el frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceClassif.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        rostro = gray[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(f'{ruta_absoluta}/rostro_{count}.jpg', rostro)
        count += 1
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Capturando Rostros', frame)

    key = cv2.waitKey(1)
    if key == 27 or count >= 30:  # ESC o 30 imágenes
        break

cap.release()
cv2.destroyAllWindows()
print(f"Captura terminada. Se guardaron {count} rostros en {ruta_absoluta}")