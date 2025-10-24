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

def start_game():
    clear_widgets()
    
    frame2()

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

#----------------------------------------------------------------


def frame2(): #second page
    clear_widgets()

    title = QLabel("Choose Topic")
    title.setStyleSheet('''
        color: white;
        font-family: "Arial";
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    ''')
    title.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    widgets["title"] = [title]
    grid.addWidget(title, 0, 0, 1, 2)

    score_label = QLabel("Score: 0")
    score_label.setStyleSheet('''
        color: white;
        font-family: "Arial";
        font-size: 18px;
        font-weight: bold;
    ''')
    score_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    widgets["score"] = [score_label]
    grid.addWidget(score_label, 0, 1, 1, 1)


    topics = ["Python Basics", "Flow Control", "Lists", "String Manipulation"]
    for i, topic in enumerate(topics):
        button = QPushButton(topic)
        button.setFixedHeight(60)
        button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        button.setStyleSheet("""
            QPushButton {
                background-color: #00A86B;
                color: white;
                border-radius: 15px;
                font-size: 18px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #00C080;
            }
        """)

        if topic != "Python Basics":
            button.setEnabled(False)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #007A5A;
                    color: #aaaaaa;
                    border-radius: 15px;
                    font-size: 18px;
                    text-align: left;
                    padding-left: 15px;
                }
            """)
            button.setText("🔒 " + topic)  

        grid.addWidget(button, i + 2, 0, 1, 2)
                       
        grid.setRowStretch(len(topics) + 3, 2)
