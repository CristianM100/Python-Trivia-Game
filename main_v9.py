import sys
from PyQt6.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout
from frames_v9 import frame1, grid

app = QApplication(sys.argv)

# Get screen information
screen = app.primaryScreen()
screen_rect = screen.availableGeometry()

# set window size
w = int(screen_rect.width() * 0.8)
h = int(screen_rect.height() * 1)

# Main window
window = QWidget()
window.setWindowTitle("Python Trivia Game")
window.resize(w, h)
window.setStyleSheet("background: #397591")

frame1()  

# the grid layout in a scrollable widget 
content_widget = QWidget()     # holds your layout
content_widget.setLayout(grid)

scroll = QScrollArea()
scroll.setWidgetResizable(True)  
scroll.setWidget(content_widget)

# scroll area into the main window 
main_layout = QVBoxLayout()
main_layout.addWidget(scroll)
window.setLayout(main_layout)

window.show()
app.exec()
