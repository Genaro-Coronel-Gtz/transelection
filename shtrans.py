import subprocess
# import requests
from os import environ
from dotenv import load_dotenv

#TODO:
# Agregar text to speech, boton para hablar
# Posibilidad de guardar configuraciones de idiomas
# Cambiar la GUI por una creada en QT Designer, para 
# Poder tener 2 text areas, una  que muestre el texto original,
# Otra la traduccion, y ademas tenga el boton de text to speech. 

# def traducir_texto_backup(text):
#     #Este es para utilizar el traductor libretranslate
#     #para eso se puede montar un servidor como indican en la pagina de github
#     url = "https://libretranslate.com/translate"
#     payload = {
#         "q": text,
#         "source": "en",  # Ingles
#         "target": "es"   # Español
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }

#     try:
#         # Realizar la solicitud POST a la API de LibreTranslate
#         response = requests.post(url, json=payload, headers=headers)
#         # Convertir la respuesta a formato JSON
#         data = response.json()
#         # Obtener el texto traducido del JSON
#         print(data)
#         texto_traducido = data["translatedText"]
#         return texto_traducido
#     except Exception as e:
#         print("Error al traducir el texto:", e)
#         return None


def traducir_texto(text):
    idioma_destino = ':' + environ.get("DST_LANGUAGE")
    try: 
        texto_traducido = subprocess.check_output(['trans', idioma_destino, '-b', text, '-no-auto'], text=True)
        return texto_traducido
    except Exception as e:
        print("Error al traducir el texot:", e)
        return None

def obtener_texto_seleccionado():
    try:
        # Utiliza xsel para obtener el texto seleccionado del portapapeles primario
        texto_seleccionado = subprocess.check_output(['xsel', '-o'], text=True)
        return texto_seleccionado.strip()  # Elimina espacios en blanco adicionales alrededor del texto
    except subprocess.CalledProcessError as e:
        print("Error al obtener el texto seleccionado:", e)
        return None

def guardar_texto():
    
    texto_seleccionado = obtener_texto_seleccionado()

    if texto_seleccionado:
        load_dotenv()
        texto_traducido = traducir_texto(texto_seleccionado)
        try:
            with open('/tmp/translatetext', 'w') as archivo:
                archivo.write('Original: ' +  texto_seleccionado)
                archivo.write('\n')
                archivo.write('Traduccion: ' + texto_traducido)
                return True
        except Exception as e:
            print("Error al guardar el texto en el archivo", e)
            return False
    else:
        print("Error al obtener el texto seleccionado")
        return False


def mostrar_ventana_texto():
    comando = ['zenity', '--text-info', '--title=Translation', '--filename=/tmp/translatetext', '--ok-label=Ok']
    # Ejecutar el comando y capturar la salida
    try:
        subprocess.run(comando, check=True)
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar Zenity:", e)

# Obtener el texto seleccionado
texto_guardado = guardar_texto()

if texto_guardado:
    # Llamar a la función para mostrar la ventana con el texto seleccionado
    mostrar_ventana_texto()
else:
    print("Error al obtener o guardar el texto seleccionado")

