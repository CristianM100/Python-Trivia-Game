from PyQt6 import QtCore
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QPushButton, QLabel, QSizePolicy
from helperfunctions import grid, widgets,clear_widgets, progress, refresh_score, update_score, save_progress, ALL_TOPICS, current_gear_widget, current_topic_score

def show_question_page(gear_id, question_data, gear_widget):
    global current_gear_widget, current_topic_score

    current_gear_widget = gear_widget  # always update reference

    clear_widgets(exclude_current_gear=True)

    # Add score label that always reads from progress
    score_label = QLabel(f"Score: {progress['score']}")
    widgets["score"] = [score_label]
    grid.addWidget(score_label, 1, 1, 1, 1)
    
    # ... add question and answer buttons as before ...
    for i, answer in enumerate(question_data["answers"]):
        btn = QPushButton(answer)
        btn.clicked.connect(lambda _, a=answer: check_answer(a, question_data, gear_id, gear_widget))
        widgets[f"answer{i}"] = [btn]
        grid.addWidget(btn, 2 + i//2, i % 2)


def check_answer(selected, question_data, gear_id, gear_widget):
    global current_topic_score, progress

    correct = question_data["correct"]

    if selected == correct:
        current_topic_score += 1
        update_score(1)  # increment global score
        refresh_score()
        gear_widget.disable_gear(gear_id)
    else:
        gear_widget.mark_gear_state(gear_id, "wrong")

    # when all gears answered
    all_done = all(s in ("correct", "wrong") for s in gear_widget.gear_states)
    if all_done:
        topic_name = gear_widget.topic_name
        # save attempt
        if topic_name not in progress["topic_scores"]:
            progress["topic_scores"][topic_name] = []
        progress["topic_scores"][topic_name].append(current_topic_score)
        
        # unlock next topic if passed
        if current_topic_score > 5:
            progress["completed_topics"].add(topic_name)
            progress["unlocked_topics"] = len(progress["completed_topics"]) + 1
            save_progress()
            refresh_score()
            # show next frame
            from frames.frame3 import frame3
            frame3()  # win frame if all passed or frame2 if continue
        else:
            # fail frame
            save_progress()
            from frames.frame4 import frame4
            frame4()




"""def show_question_page(gear_id, question_data):
    global current_gear_widget
    current_gear_widget = question_data.get("gear_widget", current_gear_widget)
    current_topic_score=0

    clear_widgets(exclude_current_gear=True)

    # Set equal column stretches for consistent sizing
    grid.setColumnStretch(0, 1)
    grid.setColumnStretch(1, 1)

    #l_margin = 50
    #r_margin = 50

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
    question.setStyleSheet(""
        font-family: 'shanti';
        font-size: 25px;
        color: 'white';
        padding: 75px;
        margin-top: 40px;
    "")
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

        progress["topic_scores"].setdefault(topic_name,[])
        progress["topic_scores"][topic_name].append(current_topic_score)

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
                from frames.frame3 import frame3
                frame3()   # <-- WIN GAME SCREEN
            else:
                from frames.frame2 import frame2
                frame2()   # <-- Continue normally
                

        else:
            # ❗ FAIL CASE — SHOW FAIL FRAME
            progress["score"] -= current_topic_score
            save_progress()
            #refresh_score()
            from frames.frame4 import frame4
            frame4()
            


    QTimer.singleShot(1000, return_to_gear)"""
