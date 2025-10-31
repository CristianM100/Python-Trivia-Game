from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6 import QtCore
from urllib.request import urlopen
import json
import os
import pandas as pd
import random
from utils import grid, widgets, clear_widgets
import clickableWidget

# this file contains the code for each window/frame

# Make sure widgets dictionary has all necessary keys
if "clickable" not in widgets:
    widgets["clickable"] = []
if "back_button" not in widgets:
    widgets["back_button"] = []


def frame1():
    clear_widgets(widgets, grid)

    image = QPixmap("logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    logo.setStyleSheet("width: 100%")

    widgets["logo"].append(logo)

    button = QPushButton("PLAY NOW!")
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.clicked.connect(frame2)

    button.setStyleSheet(
        '''
        *{
            border: 2px solid '#262124';
            border-radius: 40px;
            font-size: 30px;
            color: 'white';
            padding: 25px 0;
            margin: 50px 200px;
        }
        *:hover{
            background: '#383537';
        }
        '''
    )
    widgets["button"].append(button)

    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)


PROGRESS_FILE = "progress.json"

# Default structure
default_progress = {
    "unlocked_topics": 1,
    "score": 0,
    "completed_topics": []
}

# --- Load from file ---
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                data = json.load(f)
                # Convert completed_topics to a set for faster lookup
                data["completed_topics"] = set(data.get("completed_topics", []))
                return data
        except Exception:
            pass
    # If file missing or corrupted, return default
    return {
        "unlocked_topics": 1,
        "score": 0,
        "completed_topics": set()
    }

# --- Save to file ---
def save_progress():
    data = {
        "unlocked_topics": progress["unlocked_topics"],
        "score": progress["score"],
        "completed_topics": list(progress["completed_topics"])
    }
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=4)


progress = load_progress()

# --- MAIN TOPIC SELECTION PAGE ---
def frame2():
    clear_widgets(widgets, grid)

    # Title
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

    # Score label (auto-updates)
    score_label = QLabel(f"Score: {progress['score']}")
    score_label.setStyleSheet('''
        color: white;
        font-family: "Arial";
        font-size: 18px;
        font-weight: bold;
    ''')
    score_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    widgets["score"] = [score_label]
    grid.addWidget(score_label, 0, 1, 1, 1)

    # Topics list
    topics = [
        "Fundamentals",
        "Control Structures",
        "Data Structures",
        "Functions & Scope",
        "OOP",
        "Error & Exception Handling",
        "File Handling",
        "Advanced Topics"
    ]

    unlocked = progress["unlocked_topics"]

    # Topic buttons
    for i, topic in enumerate(topics):
        button = QPushButton(topic)
        button.setFixedHeight(60)
        button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        if topic in progress["completed_topics"]:
            # ✅ Completed topic
            button.setEnabled(False)
            button.setText("✅ " + topic)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 15px;
                    font-size: 18px;
                    text-align: left;
                    padding-left: 15px;
                }
            """)
        elif i < unlocked:
            # 🟢 Unlocked topic
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
            button.clicked.connect(lambda _, t=topic: open_topic_window(t))
        else:
            # 🔒 Locked topic
            button.setEnabled(False)
            button.setText("🔒 " + topic)
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

        grid.addWidget(button, i + 2, 0, 1, 2)

    grid.setRowStretch(len(topics) + 3, 2)


def open_topic_window(topic_name):
    """Open the ClickableWidget gear interface for the selected topic."""
    print(f"Opening topic: {topic_name}")  # DEBUG
    clear_widgets(widgets, grid)

    # Create the ClickableWidget
    clickable_widget = clickableWidget.ClickableWidget()
    clickable_widget.setTopicName(topic_name)  # Set the topic name
    clickable_widget.setFixedSize(900, 900)  # Match window size
    
    # Connect the gear click signal to show_question_page
    #clickable_widget.clicked.connect(lambda gear_id: show_question_page(topic_name, gear_id + 1))
    
    # Store widget reference
    if "clickable" not in widgets:
        widgets["clickable"] = []
    widgets["clickable"].append(clickable_widget)
    
    # Add the clickable widget to the grid (spans entire window)
    grid.addWidget(clickable_widget, 0, 0, 1, 2)
    
    print("ClickableWidget added to grid")  # DEBUG


#def show_question_page(topic_name, question_number):

