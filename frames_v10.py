from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QSizePolicy,QWidget,QHBoxLayout
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6 import QtCore
from PyQt6.QtCore import QTimer
from clickableGear import ClickableWidget
import json, os
import pandas as pd

ALL_TOPICS = [
    "Fundamentals",
    "Control Structures",
    "Data Structures",
    "Functions & Scope",
    "OOP",
    "Error & Exception Handling",
    "File Handling",
    "Advanced Topics"
]

#---------------load questions----------------
with open("qna.json", "r") as f:
    TOPIC_QUESTIONS=json.load(f)


#global dictionary of dynamically changing widgets
widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "message": [],
    "message2": [],
    "clickable":[],
    "score_indicator":[],
    "background": [] 
}

#initialliza grid layout
grid = QGridLayout()

current_topic_score = 0
current_gear_widget = None

#Progress File
PROGRESS_FILE = "prog.json"
default_progress = {
    "unlocked_topics": 1,
    "score": 0,
    "completed_topics": []
}



def clear_widgets(exclude_current_gear=False):
    #Hide and remove all existing widgets from the layout and clear the widgets dict.
    global current_gear_widget
    while grid.count():
        item = grid.takeAt(0)
        widget = item.widget()
        if widget is not None:
            if exclude_current_gear and widget ==current_gear_widget:
                continue  # fully removes widget from layout and window
            widget.setParent(None)

    # also clear your tracking dictionary
    #for widget_list in widgets.values():
     #   widget_list.clear()
    # Reset all widget lists cleanly
    for key in widgets:
        widgets[key] = []

def clear_stretch(exclude_current_gear=False):
    #Hide and remove all existing widgets from the layout and clear the widgets dict.
    global current_gear_widget
    while grid.count():
        item = grid.takeAt(0)
        widget = item.widget()
        if widget is not None:
            if exclude_current_gear and widget ==current_gear_widget:
                continue  # fully removes widget from layout and window
            widget.setParent(None)

    # also clear your tracking dictionary
    for widget_list in widgets.values():
        widget_list.clear()

    for r in range(100):
        grid.setRowStretch(r, 0)
    for c in range(100):
        grid.setColumnStretch(c, 0)

#------------ Score and Progress ---------------------
# --- Load from file ---
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                data = json.load(f)
                data["completed_topics"] = set(data.get("completed_topics", []))
                if "topic_scores" not in data:
                    data["topic_scores"] = {}
                return data
        except Exception:
            pass
    return {
        "unlocked_topics": 1,
        "score": 0,
        "completed_topics": set(),
        "topic_scores": {}
    }


# --- Save to file ---
def save_progress():
    data = {
        "unlocked_topics": progress["unlocked_topics"],
        "score": progress["score"],
        "completed_topics": list(progress["completed_topics"]),
        "topic_scores": progress.get("topic_scores", {})
    }
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def update_score(amount=1):
    global progress

    if "score" not in progress:
        progress["score"]=0
    progress["score"]+= amount
    save_progress()
    refresh_score()

def get_score(): #returns current score
    global progress
    if "score" in progress:
        return progress["score"]
    return 0

def refresh_score(): # updates the score label
    if widgets.get("score"):
        # widgets["score"][0] is used as the score label in frame2
        try:
            widgets["score"][0].setText(f"Score: {get_score()}")
        except Exception:
            pass

def reset_progress():
    # Reset the JSON file
    global progress
    progress = {
        "unlocked_topics": 1,
        "score": 0,
        "completed_topics": set(),
        "topic_scores": {}
    }

    save_progress()

    frame2()


#------------------ Frames ------------------------------------------

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


def frame2():
    clear_widgets()

    #Back button
    button = QPushButton("⬅️")
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.clicked.connect(frame1)  
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

    # Title
    title = QLabel("Choose Topic")
    title.setStyleSheet('''
        color: white;
        font-family: "Arial";
        font-size: 28px;
        font-weight: bold;
        margin-top: 40px;
    ''')
    title.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    widgets["title"] = [title]
    grid.addWidget(title, 1, 0, 1, 1)


    # Score label (auto-updates)
    score_label = QLabel(f"Score: {progress['score']}")
    score_label.setStyleSheet('''
        color: white;
        font-family: "Arial";
        font-size: 18px;
        font-weight: bold;
        margin-right:20px;
    ''')
    score_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    widgets["score"] = [score_label]
    #grid.addWidget(score_label, 1, 1, 1, 1)
    grid.addWidget(score_label, 2, 1, QtCore.Qt.AlignmentFlag.AlignRight)

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
        button.setFixedHeight(90)
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
                    background-color: #4fa3d1;
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
                    background-color: #2e5a77;
                    color: #aaaaaa;
                    border-radius: 15px;
                    font-size: 18px;
                    text-align: left;
                    padding-left: 15px;
                }
            """)

        grid.addWidget(button, i + 3, 0, 1, 2)

    # === RESET BUTTON ===
    reset_btn = QPushButton("Reset Progress")
    reset_btn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    reset_btn.setFixedHeight(50)
    reset_btn.setStyleSheet("""
        QPushButton {
            color: white;
            border-radius: 8px;
            font-size: 18px;
            background-color: #c97b37;
        }                  
        QPushButton:hover {
            background-color: #956b48;
        }
    """)
    reset_btn.clicked.connect(reset_progress)

     #Statistics Button
    stats_btn = QPushButton("📊")
    stats_btn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    stats_btn.setFixedSize(40,40)
    stats_btn.clicked.connect(frame_stats)
    stats_btn.setStyleSheet("""
        QPushButton {
            color: white;
            border-radius: 15px;
            font-size: 40px;
        }

    """)
    #grid.addWidget(stats_btn, len(topics) + 4, 0, 1, 2)


    #grid.setRowStretch(len(topics) + 3, 2)
    # Add to the grid, below the topics
    #grid.addWidget(reset_btn, len(topics) + 3, 0, 1, 2)

    grid.setRowStretch(len(topics) + 2, 2)

    bottom_row = QWidget()
    hbox = QHBoxLayout()
    hbox.setContentsMargins(10, 10, 10, 10)
    #hbox.setSpacing(20)
    
    hbox.addWidget(stats_btn)
    hbox.addWidget(reset_btn)

    bottom_row.setLayout(hbox)
    # Place stats button at the top-right
    grid.addWidget(stats_btn, 0, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)

    grid.addWidget(bottom_row, len(topics) + 4, 0, 1, 2)

def open_topic_window(topic_name):

    """Open the ClickableWidget gear interface for the selected topic."""
    global current_gear_widget
    global current_topic_score
    current_topic_score = 0

    clear_widgets()

    #Back button
    button = QPushButton("⬅️")
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.clicked.connect(frame1)  
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
    clickable_widget.setTopicName(topic_name)  # Set the topic name
    clickable_widget.setQuestions(questions_for_topic)  # Match window size
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

def show_question_page(gear_id, question_data):
    global current_gear_widget
    
    if current_gear_widget is not None:
       current_gear_widget.setParent(None)

    clear_widgets(exclude_current_gear=True)

    # Set equal column stretches for consistent sizing
    grid.setColumnStretch(0, 1)
    grid.setColumnStretch(1, 1)

    #l_margin = 50
    #r_margin = 50

    #Back button
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

    # Score label (auto-updates)
    score_label = QLabel(f"Score: {progress['score']}")
    score_label.setStyleSheet('''
        color: white;
        font-family: "Arial";
        font-size: 18px;
        font-weight: bold;
        margin-right:20px;
    ''')
    score_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    widgets["score"] = [score_label]
    grid.addWidget(score_label, 1, 1, 1, 1)


    question = QLabel(question_data ["question"])
    #question.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
    question.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet("""
        font-family: 'shanti';
        font-size: 25px;
        color: 'white';
        padding: 75px;
        margin-top: 40px;
    """)
    #question.setFixedWidth(600)
    widgets["question"].append(question)
    grid.addWidget(question, 1, 0, 1, 2)



    # Answer buttons
    for i, answer in enumerate(question_data["answers"]):
        btn = QPushButton(answer)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn.setStyleSheet(
            '''
        *{
            min-width: 350px;  /* Add this line */
            max-width: 550px;  /* Add this line */
            border: 3px solid '#bc9d00';
            color: white;
            font-family: 'shanti';
            font-size: 16px;
            border-radius: 25px;
            padding: 15px 0;
            margin-top: 40px;
        }
        *:hover{
            background: '#bc9d00';
        }
        '''
        )
        btn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn.clicked.connect(lambda _, a=answer: check_answer(a, question_data, gear_id))
        widgets[f"answer{i}"] = [btn]
        grid.addWidget(btn, 2 + i//2, i % 2)


def check_answer(selected, question_data, gear_id):
    global current_gear_widget, current_topic_score
    gear_widget = current_gear_widget
    correct = question_data["correct"]

    # Check answer
    if selected == correct:
        result_text = "✅ Correct!"
        update_score()
        refresh_score()
        current_topic_score += 1    # ---> count correct answers
        gear_widget.disable_gear(gear_id)
    else:
        result_text = "❌ Wrong!"
        gear_widget.mark_gear_state(gear_id, "wrong")

    # Show temporary result
    result_label = QLabel(result_text)
    result_label.setStyleSheet("color: yellow; font-size: 20px;")
    result_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    grid.addWidget(result_label, 6, 0, 1, 2)

    def return_to_gear():
        grid.removeWidget(result_label)
        result_label.deleteLater()

        # Remove question widgets
        for key in ["question", "answer0", "answer1", "answer2", "answer3", "score"]:
            if widgets.get(key):
                w = widgets[key].pop()
                grid.removeWidget(w)
                w.deleteLater()

        # --- Detect if ALL gears are answered ---
        all_done = all(s in ("correct", "wrong") for s in gear_widget.gear_states)

        if not all_done:
            # Return to gear view (normal)
            grid.addWidget(gear_widget, 0, 0, 1, 2)
            gear_widget.update()
            return

        # --- ALL questions answered — decide WIN OR FAIL ---
        topic_name = gear_widget.topic_name

        # Ensure topic_scores exists
        if topic_name not in progress["topic_scores"]:
            progress["topic_scores"][topic_name] = []

        # Save this attempt
        progress["topic_scores"][topic_name].append(current_topic_score)

        if current_topic_score > 5:
            progress["completed_topics"].add(topic_name)
            progress["unlocked_topics"] = len(progress["completed_topics"]) + 1
            save_progress()

            # 🎉 Check if ALL topics completed
            if progress["completed_topics"] == set(ALL_TOPICS):
                frame3()   # <-- WIN GAME SCREEN
            else:
                frame2()   # <-- Continue normally
                

        else:
            # ❗ FAIL CASE — SHOW FAIL FRAME
            progress["score"] -= current_topic_score
            save_progress()
            #refresh_score()
            frame4()
            


    QTimer.singleShot(1000, return_to_gear)

#----------Stats Helpers ------------------

def get_highest(topic):
    if "topic_scores" not in progress:
        return 0
    if topic not in progress["topic_scores"]:
        return 0
    if len(progress["topic_scores"][topic]) == 0:
        return 0
    return max(progress["topic_scores"][topic])


def get_average(topic):
    if "topic_scores" not in progress:
        return 0
    if topic not in progress["topic_scores"]:
        return 0
    scores = progress["topic_scores"][topic]
    if len(scores) == 0:
        return 0
    # each quiz is out of 10
    return int((sum(scores) / (len(scores) * 10)) * 100)


def get_overall_highest():
    if "topic_scores" not in progress:
        return 0
    h = 0
    for topic, scores in progress["topic_scores"].items():
        if len(scores) > 0:
            h = max(h, max(scores))
    return h


def get_overall_percentage():
    if "topic_scores" not in progress:
        return 0
    total_attempts = 0
    earned = 0
    for scores in progress["topic_scores"].values():
        for s in scores:
            total_attempts += 10
            earned += s
    if total_attempts == 0:
        return 0
    return int((earned / total_attempts) * 100)


#------------------ Statistics Frame -----------------

def frame_stats():
    clear_widgets()
    
     # Title
    title = QLabel("Statistics")
    title.setStyleSheet('''
        color: white;
        font-family: "Arial";
        font-size: 28px;
        font-weight: bold;
        margin-top: 20px;
    ''')
    title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    widgets["title"] = [title]
    grid.addWidget(title, 1, 0, 1, 2)

    #Back button
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

    row = 2

    # ✅ Overall
    overall_label = QLabel("Overall")
    overall_label.setStyleSheet(""" 
        font-size: 20px;  
        color: orange;  
        margin-left: 50px; 
        margin-top: 50px;
    """)
    grid.addWidget(overall_label, row, 0)

    overall_score = QLabel(f"Highest Score: {get_overall_highest()}")
    overall_score.setStyleSheet("""
        color: white;
        font-size: 15px;
        margin-left: 60px;
    """)

    overall_percent = QLabel(f"Win Percent: {get_overall_percentage()}%")
    overall_percent.setStyleSheet("""
        color: white;
        font-size: 15px;
        margin-left: 60px;
        margin-bottom: 30px;                          
    """)


    grid.addWidget(overall_score, row+1, 0, 1, 1)
    grid.addWidget(overall_percent, row+2, 0, 1, 1)

    row += 3

    left_topics = topics[:4]     # first 4
    right_topics = topics[-4:]   # last 4
        # Start rows for both columns
    left_row = row
    right_row = row

# LEFT COLUMN (first 4 topics)
    for topic in left_topics:
        label = QLabel(topic)
        label.setStyleSheet("font-size: 15px; color: orange; margin-left: 80px")
        grid.addWidget(label, left_row, 0)

        high = get_highest(topic)
        avg = get_average(topic)

        high_label = QLabel(f"Highest Score: {high}")
        high_label.setStyleSheet("""
            color: white;
            font-size: 13px;
            margin-left: 100px;
        """)
        avg_label = QLabel(f"Win Percent: {avg}%")
        avg_label.setStyleSheet("""
            color: white;
            font-size: 13px;
            margin-left: 100px;
            margin-bottom: 15px;
        """)
        grid.addWidget(high_label, left_row+1, 0)
        grid.addWidget(avg_label, left_row+2, 0)
        left_row += 3  # move down 3 rows for next topic


# RIGHT COLUMN (last 4 topics)
    for topic in right_topics:
        label = QLabel(topic)
        label.setStyleSheet("font-size: 15px; color: orange; margin-left: 80px")
        grid.addWidget(label, right_row, 1)
    
        high = get_highest(topic)
        avg = get_average(topic)

        high_label = QLabel(f"Highest Score: {high}")
        high_label.setStyleSheet("""
            color: white;
            font-size: 13px;
            margin-left: 100px;
        """)
        avg_label = QLabel(f"Win Percent: {avg}%")
        avg_label.setStyleSheet("""
            color: white;
            font-size: 13px;
            margin-left: 100px;
            margin-bottom: 15px;
        """)
        grid.addWidget(high_label, right_row+1, 1)
        grid.addWidget(avg_label, right_row+2, 1)

        right_row += 3  # move down 3 rows for next topic

    
        for i in range(20):
           grid.setRowStretch(i, 1)

#*********************************************
#             FRAME 3 - WIN GAME
#*********************************************
def frame3():
    clear_widgets()
    #clear_widgets(widgets, grid)
    #congradulations widget
    message = QLabel("Your score is:")
    message.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 25px; color: 'white'; margin: 100px 0px;"
        )
    widgets["message"].append(message)

    #score widget
    score = QLabel(str(progress["score"]))
    score.setStyleSheet("font-size: 100px; color: #8FC740; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #go back to work widget
    message2 = QLabel("Congratulations! You passed all the challenges!")
    message2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    message2.setStyleSheet(
        "font-family: 'Shanti'; font-size: 30px; color: 'white'; margin-top:0px; margin-bottom:75px;"
        )
    widgets["message2"].append(message2)

    #button widget
    button = QPushButton('TRY AGAIN!')
    button.setStyleSheet(
        "*{background:'#BC006C'; padding:25px 0px; border: 1px solid '#BC006C'; color: 'white'; font-family: 'Arial'; font-size: 25px; border-radius: 40px; margin: 10px 300px;} *:hover{background:'#ff1b9e';}"
        )
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.clicked.connect(frame2)

    widgets["button"].append(button)

    #logo widget
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px; margin-bottom: 20px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 2, 2)


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

#----------------------------Progress ----------------
progress = load_progress()

if "topic_scores" not in progress:
    progress["topic_scores"] = {}
