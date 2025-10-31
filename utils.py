from PyQt6.QtWidgets import  QGridLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6 import QtCore

grid = QGridLayout()  

'''
widgets = { 
    "button": [],
    "logo": []
}

grid = QGridLayout()    


def clear_widgets(widgets, grid):
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(len(widgets[widget])):
            widgets[widget].pop()

'''

widgets = {
    "logo": [],
    "button": [],
    "title": [],
    "score": [],
    "clickable": [],
    "back_button": [],
    "question": [],
    "counter": [],
    "score_indicator": [],
    "submit": [],
    "answer_0": [],
    "answer_1": [],
    "answer_2": [],
    "answer_3": []
}

def clear_widgets(widget_dict, layout):
    """Remove all widgets from the layout and clear the dictionary."""
    for widget_list in widget_dict.values():
        for widget in widget_list:
            layout.removeWidget(widget)
            widget.deleteLater()
        widget_list.clear()


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
        border: 2px solid '#BC006C';
        color: white;
        font-family: 'shanti';
        font-size: 16px;
        border-radius: 15px;
        padding: 15px 0;
        margin-top: 10px;
        }
        *:hover{
            background: '#BC006C';
        }
        '''
    )
    #button.clicked.connect(lambda x: is_correct(button))
    return button

    #def is_correct(btn):
    
