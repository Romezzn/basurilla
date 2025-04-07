import os
import shutil

# IP/puerto objetivo
IP_OBJETIVO = "176.57.188.45:9000"
CARPETA_ORIGEN = "."  # Carpeta actual
CARPETA_DESTINO = "para resubir"

# Crear carpeta destino si no existe
os.makedirs(CARPETA_DESTINO, exist_ok=True)

# Recorrer archivos .strm en la carpeta y subcarpetas
for root, dirs, files in os.walk(CARPETA_ORIGEN):
    for nombre_archivo in files:
        if not nombre_archivo.lower().endswith(".strm"):
            continue  # Ignora archivos que no sean .strm

        ruta_completa = os.path.join(root, nombre_archivo)

        # Evitar mover archivos de la carpeta destino
        if os.path.abspath(CARPETA_DESTINO) in os.path.abspath(ruta_completa):
            continue

        try:
            with open(ruta_completa, 'r', encoding='utf-8', errors='ignore') as archivo:
                contenido = archivo.read()

            # Verifica si contiene la IP
            if IP_OBJETIVO not in contenido:
                # Construir nueva ruta evitando sobrescribir
                nueva_ruta = os.path.join(CARPETA_DESTINO, nombre_archivo)
                contador = 1
                while os.path.exists(nueva_ruta):
                    base, ext = os.path.splitext(nombre_archivo)
                    nueva_ruta = os.path.join(CARPETA_DESTINO, f"{base}_{contador}{ext}")
                    contador += 1

                shutil.move(ruta_completa, nueva_ruta)
                print(f"🔁 Movido: {ruta_completa} → {nueva_ruta}")
            else:
                print(f"✔ Contiene IP: {ruta_completa}")

        except Exception as e:
            print(f"⚠️ Error al procesar {ruta_completa}: {e}")
