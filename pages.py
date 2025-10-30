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
    """"
    image = QPixmap("logo1.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
   # logo.setStyleSheet("margin-top: 100px;")
    widgets["logo1"].append(logo)
    """"
    background = QLabel()
    background.setPixmap(QPixmap("logo2.png"))
    background.setScaledContents(True)  # Makes image fill the whole window
    widgets["background"] = [background]
    grid.addWidget(background, 0, 0, 5, 5) 

    button = QPushButton("PLAY NOW!")
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.clicked.connect(frame2)  
    button.setStyleSheet(
         '''
        *{
            border: 2px solid '#262124';
            border-radius: 40px;
            font-size: 30px;
            color: white;
            padding: 25px 60px;
            background-color: rgba(0, 0, 0, 80);
        }
        *:hover{
            background-color: rgba(56, 53, 55, 180)
        }
        '''
    )
    widgets["button"].append(button)

    #grid.addWidget(widgets["button"][-1], 3, 0, 1, 2) changed to the one below
    grid.addWidget(button, 4, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
    #grid.addWidget(widgets["logo1"][-1], 0, 0, 1, 2) not needed since the image is no longer just a widget

#----------------------------------------------------------------


def frame2(): #second page
    clear_widgets()

    window = grid.parentWidget()
    window.resize(1000, 700)

    grid.setColumnStretch(0,1)
    grid.setRowStretch(1,1)
    
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
    grid.addWidget(title, 1, 0, 1, 2)

    score_label = QLabel("Score: 0")
    score_label.setStyleSheet('''
        color: white;
        font-family: "Arial";
        font-size: 18px;
        font-weight: bold;
    ''')
    score_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    widgets["score"] = [score_label]
    grid.addWidget(score_label, 1, 1, 1, 1)


    #topics = ["Python Basics", "Flow Control", "Lists", "String Manipulation"]
    topics = ["Fundamentals", "Control Structures", "Data Structures", "Functions & Scope", "OOP", "Error & Exception Handling", "File Handling", "Advanced Topics"]
    
    
    for i, topic in enumerate(topics):
        button = QPushButton(topic)
        button.setFixedHeight(60)
        button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        button.setStyleSheet("""
            QPushButton {
                background-color: #4fa3d1;
                color: white;
                border-radius: 15px;
                font-size: 18px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #6fb7e2;
            }
        """)

        if topic != "Python Basics":
            button.setEnabled(False)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2e5a77;
                    color: #aaaaaa;
                    border-radius: 15px;
                    font-size: 18px;
                    text-align: left;
                    padding-left: 15px;
                }
            """)
            button.setText("🔒 " + topic)  

        grid.addWidget(button, i + 3, 0, 1, 2)
                       
        grid.setRowStretch(len(topics) + 5, 2)

def frame3():
    clear_widgets()

    title = QLabel("Question in ")
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

