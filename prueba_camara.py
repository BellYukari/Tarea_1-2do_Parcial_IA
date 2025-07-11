import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: No se pudo acceder a la camara.")
    exit()

print("presiona 'q' para salir.")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Error al recibir el frame.")
        break

    cv2.imshow('prueba de camara', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


