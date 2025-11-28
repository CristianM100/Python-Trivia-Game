from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtWidgets import QLabel, QGridLayout, QWidget, QPushButton
from helperfunctions import grid, widgets, clear_stretch
from frames.frame2 import frame2


def frame1():
    clear_stretch()

    background = QLabel()
    background.setPixmap(QPixmap("logo1.png"))
    background.setScaledContents(True)  # Makes image fill the whole window
    widgets["background"] = [background]
    grid.addWidget(background, 0, 0, 5, 5) 

    button = QPushButton("PLAY NOW!")
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.clicked.connect(frame2)  
    button.setStyleSheet(
         '''
        *{
            border: 1px solid '#262124';
            border-radius: 15px;
            font-size: 15px;
            color: white;
            padding: 15px 15px;
            background-color: rgba(0, 0, 0, 80);
        }
        *:hover{
            background-color: rgba(56, 53, 55, 180)
        }
        '''
    )

    widgets["button"].append(button)

    grid.addWidget(button, 3, 0, 1, 5, QtCore.Qt.AlignmentFlag.AlignCenter)

  #  grid.addWidget(button, 3, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)