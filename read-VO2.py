import imaplib
import email
from email.header import decode_header
import time

# Configuración de la cuenta
SERVER = 'imap.gmail.com'
USER = 'Tu_Correo'
PASS = 'Tu_Contraseña de aplicaciones'  # Contraseña de aplicación

try:
    # Conexión al servidor
    server = imaplib.IMAP4_SSL(SERVER)
    server.login(USER, PASS)
    server.select('Inbox')

    # Leer el último correo
    result, data = server.search(None, 'ALL')
    ids = data[0].split()
    latest_email_id = ids[-1]

    result, data = server.fetch(latest_email_id, '(RFC822)')
    raw_email = data[0][1].decode('utf-8')
    server.logout()

    # Extraer solo el cuerpo del correo
    msg = email.message_from_string(raw_email)
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload:
                    body += payload.decode('utf-8', errors='ignore')
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode('utf-8', errors='ignore')

    print("[DEBUG] Contenido limpio del correo:")
    print(body)

    # Verifica si contiene ON u OFF
    estado = "OFF"
    if "ON" in body.upper():
        estado = "ON"
    elif "OFF" in body.upper():
        estado = "OFF"

    print(f"[DEBUG] Estado detectado: {estado}")

    # Escribir en estado.txt
    with open('/home/Owen/estado.txt', 'w') as f:
        f.write(estado)

    # Guardar log
    with open('/home/Owen/log_estado.txt', 'a') as log:
        log.write(f"[{time.ctime()}] Estado del correo actualizado a: {estado}\n")

    print(f"[INFO] Estado del correo actualizado a: {estado}")

except Exception as e:
    print(f"[ERROR] {e}")
    with open('/home/Owen/log_estado.txt', 'a') as log:
        log.write(f"[{time.ctime()}] Error: {str(e)}\n")