import sys
from PyQt6.QtWidgets import QApplication, QWidget
from frames_v5 import frame1, grid

app = QApplication(sys.argv)

# Get screen information
screen = app.primaryScreen()
screen_rect = screen.availableGeometry()

# Create window
window = QWidget()
window.setWindowTitle("Python Trivia Game")

# Set window to 80% of screen size, centered
''''
width = int(screen_rect.width() * 0.8)
height = int(screen_rect.height() * 0.8)
x = (screen_rect.width() - width) // 2
y = (screen_rect.height() - height) // 2

window.setGeometry(x, y, width, height)
'''

window.setStyleSheet("background: #397591")


frame1()

window.setLayout(grid)

window.show()
app.exec()
