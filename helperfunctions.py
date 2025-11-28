from PyQt6.QtWidgets import QGridLayout
import json, os

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

#----------------------------Progress ----------------
progress = load_progress()

if "topic_scores" not in progress:
    progress["topic_scores"] = {}