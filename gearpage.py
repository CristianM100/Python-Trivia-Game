from PyQt6 import QtCore
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QGridLayout, QPushButton
from clickableGear import ClickableWidget
from helperfunctions import clear_widgets, widgets, grid, TOPIC_QUESTIONS
from frames.questionpage import show_question_page

def open_topic_window(topic_name):

    """Open the ClickableWidget gear interface for the selected topic."""
    global current_gear_widget
    global current_topic_score
    current_topic_score = 0

    clear_widgets()

    #Back button
    from frames.frame2 import frame2
    button = QPushButton("⬅️")
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.clicked.connect(frame2)  
    button.setStyleSheet(
         '''
        *{
            border-radius: 70px;
            font-size: 26px;
            color: white;
            padding: 0px 0px;
        }
        '''
    )
    widgets["button"].append(button)

    grid.addWidget(button, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)

    
    questions_for_topic=TOPIC_QUESTIONS[topic_name]
   
    # Create the ClickableWidget
    clickable_widget = ClickableWidget() 
    clickable_widget.setTopicName(topic_name) 
    # Set the topic name 
    clickable_widget.setQuestions(questions_for_topic) # Match window size 
    clickable_widget.clicked.connect(lambda gear_id: show_question_page(gear_id,questions_for_topic[gear_id])) 
    current_gear_widget = clickable_widget 
    widgets["clickable"].append(clickable_widget)

    clickable_widget.gear_states = ["unanswered"] * 10
    for g in clickable_widget.widgets:
        g["state"] = "unanswered"
        g["enabled"] = True
    clickable_widget.update()
   
    # Add the clickable widget to the grid (spans entire window)
    #grid.addWidget(clickable_widget, 2, 0, 1, 2)
    #grid.addWidget(clickable_widget, 2, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
   # grid.setRowStretch(1, 1)
    grid.addWidget(clickable_widget, 1, 0, 1, 2)