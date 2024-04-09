import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import *
import subprocess
from os import environ
from dotenv import load_dotenv

from MainWindow import Ui_mainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):

    def speech_translated_text(self):
        print('speech text clicked', self.textEdit_2.toPlainText())

    def traducir_texto(self, text):
        print(' traducir texto ', text)
        idioma_destino = ':' + environ.get("DST_LANGUAGE")
        try: 
            texto_traducido = subprocess.check_output(['trans', idioma_destino, '-b', text, '-no-auto'], text=True)
            return texto_traducido
        except Exception as e:
            print("Error al traducir el texot:", e)
            return None

    def obtener_texto_seleccionado(self):
        try:
            # Utiliza xsel para obtener el texto seleccionado del portapapeles primario
            texto_seleccionado = subprocess.check_output(['xsel', '-o'], text=True)
            return texto_seleccionado.strip()  # Elimina espacios en blanco adicionales alrededor del texto
        except subprocess.CalledProcessError as e:
            print("Error al obtener el texto seleccionado:", e)
            return None
    
    def guardar_texto(self):
        texto_seleccionado = self.obtener_texto_seleccionado()
        self.textEdit.setText(texto_seleccionado)

        if texto_seleccionado:
            
            load_dotenv()
            texto_traducido = self.traducir_texto(texto_seleccionado)
            self.textEdit_2.setText(texto_traducido)

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

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.label.setText('Texto original')
        self.label_2.setText('Traduccion')
        # self.pushButton.hide()
        self.pushButton.pressed.connect(self.speech_translated_text)
        self.guardar_texto()


# app = QtWidgets.QApplication(sys.argv)

# window = MainWindow()
# window.show()
# app.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setApplicationName("Download audio")
    app.setStyle("Fusion")
    # Fusion dark palette from https://gist.github.com/QuantumCD/6245215.
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    window = MainWindow()
    window.show()
    app.exec_()
