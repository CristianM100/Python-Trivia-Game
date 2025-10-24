from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6 import QtCore
from urllib.request import urlopen
import json
import pandas as pd
import random

# this file contains the code for each window/frame


widgets = { 
    "button": [],
    "logo1": []
}

grid = QGridLayout()    # initialize grid layout

# hide existing widgets and remove them from the dictionary
def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()

def create_buttons(answer, l_margin, r_margin):
    #create identical buttons with custom left & right margins
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet(
        #setting variable margins
        "*{margin-left: " + str(l_margin) +"px;"+
        "margin-right: " + str(r_margin) +"px;"+
        '''
        border: 4px solid '#BC006C';
        color: white;
        font-family: 'shanti';
        font-size: 16px;
        border-radius: 25px;
        padding: 15px 0;
        margin-top: 20px;
        }
        *:hover{
            background: '#BC006C';
        }
        '''
    )
    #button.clicked.connect(lambda x: is_correct(button))
    return button

    #def is_correct(btn):
    


#   FRAME 1 or WINDOW 1

def frame1():
    clear_widgets()

    image = QPixmap("logo1.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
   # logo.setStyleSheet("margin-top: 100px;")
    widgets["logo1"].append(logo)

    button = QPushButton("PLAY NOW!")
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.setStyleSheet(
         '''
        *{
            border: 4px solid '#262124';
            border-radius: 40px;
            font-size: 30px;
            color: 'white';
            padding: 25px 0;
            margin: 100px 200px;
        }
        *:hover{
            background: '#383537';
        }
        '''
    )
    widgets["button"].append(button)

    grid.addWidget(widgets["button"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["logo1"][-1], 0, 0, 1, 2)