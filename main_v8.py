# Only needed for access to command line arguments
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
#from pages import frame1, grid
from frames_v8 import frame1, grid

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = QWidget()

window.setWindowTitle("Python Trivia Game")
window.setFixedWidth(800)
window.setFixedHeight(770)
window.setStyleSheet("background: #397591")

frame1()

window.setLayout(grid)


window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()
