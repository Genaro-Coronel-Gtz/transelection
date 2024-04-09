# transelection
Script para traducir texto seleccionado en python

En el sistema:
Instalar lo de Qt
Instalar espeak


sudo apt-get install espeak

En el ambiente de python:

pyttsx3
import pyttsx3
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
from os import environ
from dotenv import load_dotenv