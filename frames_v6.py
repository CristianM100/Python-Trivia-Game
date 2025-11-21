from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QSizePolicy, QWidget, QHBoxLayout
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6 import QtCore
from PyQt6.QtCore import QTimer
from clickableGear_v2 import ClickableWidget
import json, os
import pandas as pd


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
    "score_indicator":[]
}

#initialliza grid layout
grid = QGridLayout()
current_gear_widget=None

#Progress File
PROGRESS_FILE = "prog copy.json"
default_progress = {
    "unlocked_topics": 1,
    "score": 0,
    "completed_topics": [],
    "topic_scores":{}
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
                # Convert completed_topics to a set for faster lookup
                data["completed_topics"] = set(data.get("completed_topics", []))
                if "topic_scores" not in data:
                    data["topic_scores"]={}
                return data
        except Exception:
            pass
    # If file missing or corrupted, return default
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

#----------Stats Helpers ------------------

def get_topic_score(topic):
    """Returns sum of points earned in this topic"""
    return sum(progress["topic_scores"].get(topic, []))

def get_topic_percentage(topic):
    """Returns percentage score (0-100) for this topic"""
    scores = progress["topic_scores"].get(topic, [])
    if not scores:
        return 0
    max_score = len(scores)  # each question counts as 1
    return int(sum(scores) / max_score * 100)

def get_overall_highest():
    """Highest single topic score"""
    if not progress["topic_scores"]:
        return 0
    return max(sum(scores) for scores in progress["topic_scores"].values())

def get_overall_percentage():
    """Overall percentage across all topics"""
    total_points = 0
    total_possible = 0
    for scores in progress["topic_scores"].values():
        total_points += sum(scores)
        total_possible += len(scores)
    if total_possible == 0:
        return 0
    return int(total_points / total_possible * 100)

"""def get_highest(topic):
    if "topic_scores" not in progress:
        return 0
    if topic not in progress["topic_scores"]:
        return 0
    if len(progress["topic_scores"][topic]) == 0:
        return 0
    return max(progress["topic_scores"][topic])


def get_average(topic):
    if "topic_scores" not in progress or topic not in progress["topic_scores"]:
        return 0
    scores = progress["topic_scores"][topic]
    if len(scores) == 0:
        return 0
    # Cap each score at 100%
    capped_scores = [min(s, 100) for s in scores]
    return int(sum(capped_scores) / len(capped_scores))

    "if "topic_scores" not in progress:
        return 0
    if topic not in progress["topic_scores"]:
        return 0
    scores = progress["topic_scores"][topic]
    if len(scores) == 0:
        return 0
    # each quiz is out of 10
    return int((sum(scores) / (len(scores) * 10)) * 100)"


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
    total = 0
    count = 0
    for topic, scores in progress["topic_scores"].items():
        for s in scores:
            total += min(s, 100)
            count += 1
    if count == 0:
        return 0
    return int(total / count)

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
    return int((earned / total_attempts) * 100)"""



#------------------ Frames ------------------------------------------

def frame1():
    clear_widgets()

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

    grid.addWidget(button, 4, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

  #  grid.addWidget(button, 3, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)


def frame2():
    global current_gear_widget
    clear_widgets()
    if current_gear_widget:
        grid.removeWidget(current_gear_widget)
        current_gear_widget.setParent(None)
        current_gear_widget = None

    #Back button
    button = QPushButton("⬅️")
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.clicked.connect(frame1)  
    button.setStyleSheet(
         '''
        *{
            border-radius: 70px;
            font-size: 24px;
            color: white;
            padding: 0px 0px;
            background-color: rgba(0, 0, 0, 80);
            
        
        }
        *:hover{
            background-color: rgba(56, 53, 55, 180)
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
        margin-top: 20px;
    ''')
    title.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    widgets["title"] = [title]
    grid.addWidget(title, 1, 0, 1, 1)


    # Score label + statistics icon button
    score_label = QLabel(f"Score: {progress['score']}")
    score_label.setStyleSheet('''
        color: white;
        font-family: "Arial";
        font-size: 18px;
        font-weight: bold;
    ''')
    score_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

    # Statistics icon button
    stats_button = QPushButton("📊")
    stats_button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    stats_button.setFixedSize(30, 30)
    stats_button.setStyleSheet('''
        *{
            border: none;
            font-size: 18px;
            background: transparent;
            color: white;
        }
        *:hover{
            background-color: rgba(255, 255, 255, 30);
            border-radius: 5px;
        }
    ''')
    stats_button.clicked.connect(frame_stats)

    # Use horizontal layout to combine score label + icon
    score_widget = QWidget()
    hbox = QHBoxLayout()
    hbox.setContentsMargins(0,0,0,0)
    hbox.addWidget(score_label)
    hbox.addWidget(stats_button)
    score_widget.setLayout(hbox)

    widgets["score"] = [score_label]
    grid.addWidget(score_widget, 1, 1, 1, 1)


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

    """#Statistics Button
    stats_btn = QPushButton("Statistics")
    stats_btn.setFixedHeight(50)
    stats_btn.clicked.connect(frame_stats)
    stats_btn.setStyleSheet(
        QPushButton {
            background-color: #574e35;
            color: white;
            border-radius: 8px;
            font-size: 18px;
        }
        QPushButton:hover {
            background-color: #956b48;
        }
    )
    grid.addWidget(stats_btn, len(topics) + 4, 0, 1, 2)"""

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
            button.clicked.connect(lambda _, t=topic: open_topic_window(t,topics))
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

        grid.addWidget(button, i + 2, 0, 1, 2)

    # === RESET BUTTON ===
    reset_btn = QPushButton("Reset Progress")
    reset_btn.setFixedHeight(50)
    reset_btn.setStyleSheet("""
        QPushButton {
            background-color: #c97b37;
            color: white;
            border-radius: 8px;
            font-size: 18px;
        }
        QPushButton:hover {
            background-color: #efbc50;
        }
    """)
    reset_btn.clicked.connect(reset_progress)

    grid.setRowStretch(len(topics) + 3, 2)
    # Add to the grid, below the topics
    grid.addWidget(reset_btn, len(topics) + 3, 0, 1, 2)


def open_topic_window(topic_name,topics):
    """Open the ClickableWidget gear interface for the selected topic."""
    global current_gear_widget
    clear_widgets()
    if current_gear_widget:
        grid.removeWidget(current_gear_widget)
        current_gear_widget.setParent(None)
    
    questions_for_topic=TOPIC_QUESTIONS[topic_name]
   
    # Create the ClickableWidget
    clickable_widget = ClickableWidget()
    clickable_widget.setTopicName(topic_name)  # Set the topic name
    clickable_widget.setQuestions(questions_for_topic)  # Match window size
    clickable_widget.clicked.connect(lambda gear_id: show_question_page(gear_id, questions_for_topic[gear_id], topics))
    current_gear_widget=clickable_widget
    widgets["clickable"].append(clickable_widget)
    clickable_widget.back_clicked.connect(frame2)

    """clickable_widget.gear_states = ["unanswered"] * 10
    for g in clickable_widget.widgets:
        g["state"] = "unanswered"
        g["enabled"] = True
    clickable_widget.update()"""
    topic_scores = progress.get("topic_scores", {}).get(topic_name, [])
    clickable_widget.gear_states = []
    for i in range(len(topic_scores)):
        if topic_scores[i] == 1:
            clickable_widget.gear_states.append("correct")
            clickable_widget.widgets[i]["state"] = "correct"
            clickable_widget.widgets[i]["enabled"] = False
        else:
            clickable_widget.gear_states.append("unanswered")
            clickable_widget.widgets[i]["state"] = None
            clickable_widget.widgets[i]["enabled"] = True
    # Fill the rest with "unanswered" if less than 10 questions
    for i in range(len(topic_scores), 10):
        clickable_widget.gear_states.append("unanswered")
        clickable_widget.widgets[i]["state"] = None
        clickable_widget.widgets[i]["enabled"] = True

    current_gear_widget = clickable_widget
    # Add the clickable widget to the grid (spans entire window)
    grid.addWidget(clickable_widget, 1, 0, 1, 2)
    clickable_widget.back_clicked.connect(frame2)
    clickable_widget.update()

    """#Back button
    button = QPushButton("<-Back")
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.clicked.connect(frame2)  
    button.setStyleSheet(
         '''
        *{
            border: 1px solid '#262124';
            border-radius: 70px;
            font-size: 10px;
            color: white;
            padding: 10px 10px;
            background-color: rgba(0, 0, 0, 80);
            
        
        }
        *:hover{
            background-color: rgba(56, 53, 55, 180)
        }
        '''
    )
    widgets["button"].append(button)
    grid.addWidget(button, 1, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)"""
    

def show_question_page(gear_id, question_data,topics):
    global current_gear_widget
    
    #if current_gear_widget is not None:
    #   current_gear_widget.setParent(None)

    #clear_widgets(exclude_current_gear=True)
    if current_gear_widget:
        current_gear_widget.hide()

    # Set equal column stretches for consistent sizing
    grid.setColumnStretch(0, 1)
    grid.setColumnStretch(1, 1)

    #l_margin = 50
    #r_margin = 50

    for key in ["question", "answer0", "answer1", "answer2", "answer3", "score", "button"]:
        while widgets.get(key):
            w = widgets[key].pop()
            grid.removeWidget(w)
            w.deleteLater()

    #Back button
    button = QPushButton("⬅️")
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.clicked.connect(frame2)  
    button.setStyleSheet(
         '''
        *{
            border-radius: 70px;
            font-size: 24px;
            color: white;
            padding: 0px 0px;
            background-color: rgba(0, 0, 0, 80);
            
        
        }
        *:hover{
            background-color: rgba(56, 53, 55, 180)
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
            margin: 10px 10px 10px 10px;
        }
        *:hover{
            background: '#bc9d00';
        }
        '''
        )
        btn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn.clicked.connect(lambda _, a=answer: check_answer(a, question_data, gear_id,topics))
        widgets[f"answer{i}"] = [btn]
        grid.addWidget(btn, 2 + i//2, i % 2)

def check_answer(selected, question_data, gear_id, topics):
    """Handles selecting an answer for a question. Updates score, topic progress, and UI feedback."""
    global current_gear_widget

    gear_widget = current_gear_widget
    topic_name = gear_widget.topic_name  # Must assign first
    unlocked_index_of_topic = topics.index(topic_name)  # index in topics list

    # Determine if the selected answer is correct
    correct = question_data["correct"]
    question_score = 1 if selected == correct else -1  # subtract 1 if wrong
    
    # Count wrong answers in this topic
    topic_scores = progress["topic_scores"].get(topic_name, [])
    wrong_answers = topic_scores.count(0)

    # If user fails too many times → FAIL FRAME
    if wrong_answers >= 3:
        frame4(topic_name, topics)  
        return



    # Ensure the topic exists in progress
    if topic_name not in progress["topic_scores"]:
        progress["topic_scores"][topic_name] = []

    # Save this question's score in the correct position
    if len(progress["topic_scores"][topic_name]) > gear_id:
        progress["topic_scores"][topic_name][gear_id] = max(0, question_score)  # store 0 for wrong
    else:
        # Fill with zeros if missing
        while len(progress["topic_scores"][topic_name]) < gear_id:
            progress["topic_scores"][topic_name].append(0)
        progress["topic_scores"][topic_name].append(max(0, question_score))

    # Update overall score (subtract 1 for wrong)
    update_score(question_score)
    refresh_score()

    if all(topic["completed"] for topic in topics.values()):
        frame3(topics)
        return


    # Visual feedback
    if selected == correct:
        gear_widget.disable_gear(gear_id)
    else:
        gear_widget.mark_gear_state(gear_id, "wrong")

    # Show result temporarily
    result_label = QLabel("✅ Correct!" if selected == correct else "❌ Wrong!")
    result_label.setStyleSheet("color: yellow; font-size: 20px;")
    result_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    widgets["message"].append(result_label)
    grid.addWidget(result_label, 6, 0, 1, 2)

    def return_to_gear():
        while widgets.get("message"):
            w = widgets["message"].pop()
            grid.removeWidget(w)
            w.deleteLater()

        # Remove question and answer buttons
        for key in ["question", "answer0", "answer1", "answer2", "answer3", "score", "button"]:
            while widgets.get(key):
                w = widgets[key].pop()
                grid.removeWidget(w)
                w.deleteLater()

        # Show gear widget again
        gear_widget.update()
        gear_widget.show()

        # Update progress first
        topic_scores = progress.get("topic_scores", {}).get(topic_name, [])
        total_questions = len(TOPIC_QUESTIONS[topic_name])
        # Pad missing questions as 0
        padded_scores = topic_scores + [0] * (total_questions - len(topic_scores))

        # Count number of correct answers for unlocking next topic
        correct_count = sum(1 for s in padded_scores if s == 1)

        # Unlock next topic if 8 or more correct
        if correct_count >= 8:
            progress["unlocked_topics"] = max(progress["unlocked_topics"], unlocked_index_of_topic + 2)

        # Mark topic as completed (green) only if all correct (10/10)
        if all(s == 1 for s in padded_scores):
            progress["completed_topics"].add(topic_name)

        save_progress()
        refresh_score()


    # Wait 1 second, then return to gear view
    QTimer.singleShot(1000, return_to_gear)




"""def check_answer(selected, question_data, gear_id):
    global current_gear_widget
    gear_widget = current_gear_widget  # use the current gear page
    correct = question_data["correct"]
    
    if selected == correct:
        result_text = "✅ Correct!"
        update_score()
        refresh_score()
        # Disable the gear so it can't be clicked again
        gear_widget.disable_gear(gear_id)
    else:
        result_text = "❌ Wrong!"
        update_score(-1)
        refresh_score()
        gear_widget.mark_gear_state(gear_id, "wrong")
    
    # Show a temporary QLabel with result
    result_label = QLabel(result_text)
    result_label.setStyleSheet("color: yellow; font-size: 20px;")
    result_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    grid.addWidget(result_label, 6, 0, 1, 2)

    # After 1 second, remove the label and return to gear page
    def return_to_gear():
        grid.removeWidget(result_label)
        result_label.deleteLater()

        for key in ["question", "answer0", "answer1", "answer2", "answer3", "score"]:
            if widgets.get(key):
                w=widgets[key].pop()
                grid.removeWidget(w)
                w.deleteLater()
        if gear_widget is not None:
            grid.addWidget(gear_widget,0,0,1,2)
            gear_widget.update()  # redraw gears
        if gear_widget.all_correct():
            topic_name=gear_widget.topic_name
            
            if topic_name not in progress["topic_scores"]:
                progress["topic_scores"][topic_name]=[]
            progress["topic_scores"][topic_name].append(get_score())

            progress["completed_topics"].add(topic_name)
            progress["unlocked_topics"]+=1
            save_progress()
            frame2()

    QTimer.singleShot(1000, return_to_gear)"""


#*********************************************
#             FRAME 3 - WIN GAME
#*********************************************
def frame3(topics):
    clear_widgets()

    # WIN MESSAGE
    message = QLabel("Congratulations!\nYou completed ALL topics!\nYour total score is:")
    message.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 25px; color: 'white'; margin: 100px 0px;"
    )
    widgets["message"].append(message)

    # TOTAL SCORE (sum of all topic scores)
    total_score = sum(topic["score"] for topic in topics.values())
    score_label = QLabel(str(total_score))
    score_label.setStyleSheet("font-size: 100px; color: #8FC740; margin: 0 75px;")
    widgets["score"].append(score_label)

    # SECOND MESSAGE
    message2 = QLabel("OK. Now go back to WORK.")
    message2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    message2.setStyleSheet(
        "font-family: 'Shanti'; font-size: 30px; color: 'white'; margin-top:0px; margin-bottom:75px;"
    )
    widgets["message2"].append(message2)

    # BUTTON → RETURN TO MAIN MENU
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        "*{background:'#BC006C'; padding:25px 0px; border: 1px solid '#BC006C'; "
        "color: 'white'; font-family: 'Arial'; font-size: 25px; border-radius: 40px; "
        "margin: 10px 300px;} *:hover{background:'#ff1b9e';}"
    )
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.clicked.connect(frame1)   # returns to main menu
    widgets["button"].append(button)

    # LOGO
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    logo.setStyleSheet("padding:10px; margin-top:75px; margin-bottom:20px;")
    widgets["logo"].append(logo)

    # PLACE WIDGETS
    grid.addWidget(widgets["message"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 2, 2)

#----------------------------Progress ----------------
progress=load_progress()
if "topic_scores" not in progress:
    progress["topic_scores"] = {}


#------------------ Statistics Frame -----------------

def frame_stats():
    clear_widgets()

    top_row = QWidget()
    hbox = QHBoxLayout()
    hbox.setContentsMargins(0, 0, 0, 0)

    title = QLabel("Statistics")
    title.setStyleSheet("font-size: 40px; color: white; font-weight: bold;")
    hbox.addWidget(title, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

    #Back button
    button = QPushButton("⬅️")
    button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    button.clicked.connect(frame2)  
    button.setStyleSheet(
         '''
        *{
            border-radius: 50px;
            font-size: 24px;
            color: white;
            padding: 0px 0px;
            background-color: rgba(0, 0, 0, 80);
        
        }
        *:hover{
            background-color: rgba(56, 53, 55, 180)
        }
        '''
    )
    widgets["button"].append(button)
    hbox.addWidget(button, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

    top_row.setLayout(hbox)
    grid.addWidget(top_row, 0, 0, 1, 2)

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
    overall_label.setStyleSheet("font-size: 20px; color: orange;")
    grid.addWidget(overall_label, row, 0)

    overall_score = QLabel(f"Highest Score: {get_overall_highest()}")
    overall_percent = QLabel(f"Win Percent: {get_overall_percentage()}%")
    grid.addWidget(overall_score, row+1, 0)
    grid.addWidget(overall_percent, row+2, 0)
    row += 3

    # ✅ Per-topic
    for topic in topics:
        name = QLabel(topic)
        name.setStyleSheet("font-size: 18px; color: orange;")
        grid.addWidget(name, row, 0)

        high = get_topic_score(topic)
        avg = get_topic_percentage(topic)

        high_label = QLabel(f"Highest Score: {high}")
        avg_label = QLabel(f"Win Percent: {avg}%")

        grid.addWidget(high_label, row+1, 0)
        grid.addWidget(avg_label, row+2, 0)

        row += 3


#*********************************************
#                  FRAME 4 - FAIL
#*********************************************
def frame4(topic_name, topics):
    """Show fail screen when player gets 3+ wrong answers in this topic."""
    clear_widgets()

    # Compute score for THIS topic
    topic_scores = progress["topic_scores"].get(topic_name, [])
    correct = topic_scores.count(1)

    # FAIL MESSAGE
    message = QLabel(f"Sorry!\nYou failed this topic.\nCorrect answers: {correct}/10")
    message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 32px; color: white; margin: 40px; padding: 20px;"
    )
    widgets["message"].append(message)

    # TRY AGAIN BUTTON → returns to gear page for THIS topic
    retry_btn = QPushButton("TRY AGAIN")
    retry_btn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    retry_btn.setStyleSheet(
        '''*{
            padding: 20px 0;
            background: '#966b47';
            color: white;
            font-family: 'Arial';
            font-size: 30px;
            border-radius: 30px;
            margin: 10px 150px;
        }
        *:hover{
            background: '#855a3f';
        }'''
    )
    retry_btn.clicked.connect(lambda: open_topic_window(topic_name, topics))
    widgets["button"].append(retry_btn)

    # LOGO
    pix = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pix)
    logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    logo.setStyleSheet("padding: 10px; margin-top: 30px;")
    widgets["logo"].append(logo)

    # Add to layout
    grid.addWidget(message, 0, 0, 1, 2)
    grid.addWidget(retry_btn, 1, 0, 1, 2)
    grid.addWidget(logo, 2, 0, 1, 2)
