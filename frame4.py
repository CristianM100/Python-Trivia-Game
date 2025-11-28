from PyQt6 import QtCore
from PyQt6.QtGui import QCursor, QPixmap
from PyQt6.QtWidgets import QLabel,QPushButton
from helperfunctions import widgets,grid,clear_widgets

#*********************************************
#                  FRAME 4 - FAIL
#*********************************************
def frame4():
    #clear_widgets(widgets, grid)
    global current_topic_score
    current_topic_score = int(current_topic_score)   # force safe int

    clear_widgets()
    #sorry widget
    message = QLabel("Sorry, you have failed!\n Your score is: ")
    message.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight) 
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 35px; color: 'white'; margin: 75px 5px; padding:20px;"
        )
    widgets["message"].append(message)

    #score widget
    score = QLabel(str(current_topic_score))
    #score = QLabel(str(progress["score"]))

    score.setStyleSheet("font-size: 100px; color: white; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #button widget
    button = QPushButton('TRY AGAIN!')
    button.setStyleSheet(
        '''*{
            padding: 25px 0px;
            background: '#966b47';
            color: 'white';
            font-family: 'Arial';
            font-size: 35px;
            border-radius: 40px;
            margin: 10px 200px;
        }
        *:hover{
            background: '#966b47';
        }'''
        )
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    from frames.frame2 import frame2
    button.clicked.connect(frame2)

    widgets["button"].append(button)

    #logo widget
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message"][-1], 1, 0)
    grid.addWidget(widgets["score"][-1], 1, 1)
    grid.addWidget(widgets["button"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2)

