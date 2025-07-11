import cv2
import os
import time

# Ruta del modelo y personas
dataPath = 'rostros'
personas = os.listdir(dataPath)
print("Personas detectables:", personas)

# Cargar modelo entrenado
modelo = cv2.face.LBPHFaceRecognizer_create()
modelo.read('modelo.xml')

# Iniciar cámara
cap = cv2.VideoCapture(0)
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def leer_estado():
    try:
        with open("/home/Owen/estado.txt", "r") as f:
            estado = f.read().strip()
            print(f"[DEBUG] Estado leído: {estado}")  # Mensaje de depuración
            return estado
    except Exception as e:
        print(f"[ERROR] No se pudo leer estado.txt: {e}")
        return "OFF"

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] No se recibió el frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    estado = leer_estado()  # Leer estado en cada iteración

    for (x, y, w, h) in faces:
        rostro = gray[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)

        if estado == "ON":
            result = modelo.predict(rostro)
            if result[1] < 70:
                nombre = personas[result[0]]
                color = (0, 255, 0)  # Verde
            else:
                nombre = "Desconocido"
                color = (0, 0, 255)  # Rojo
        else:
            nombre = "Sistema Desactivado"
            color = (0, 0, 255)  # Rojo

        cv2.putText(frame, nombre, (x, y - 10), 2, 0.8, color, 1, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    cv2.imshow('Reconocimiento Facial', frame)

    if cv2.waitKey(50) == 27:  # Espera 50ms y revisa ESC
        break

cap.release()
cv2.destroyAllWindows()