import sys
import math
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QRect, QPointF, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath

class ClickableWidget(QWidget):
    clicked = pyqtSignal(int)  # signal to emit widget ID when clicked
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Questions in Topic Name")
        #self.setGeometry(100, 100, 1200, 800)
        
        #print("ClickableWidget initialized")  # DEBUG
        
        # Create gradient background color (teal/green)
        self.bg_color = QColor(57, 117, 145)  # Match your app's background
        
        # topic name (will be set externally)
        self.topic_name = "Topic Name"
        
        # Create gear positions 
        self.widgets = []
        self.gear_size = 40  # Larger gears
        
        # positions for gears (adjusted for your window size)
        positions = [
            (140, 92), 
            (142, 164), 
            (280, 246), 
            (268, 328), 
            (420, 410),
            (412, 492), 
            (560, 574), 
            (548, 656), 
            (700, 738), 
            (688, 820) 
        ]
          
        for i, (x, y) in enumerate(positions):
            self.widgets.append({
                'center': QPointF(x, y),
                'id': i,
                'hovered': False
            })
        
        self.setMouseTracking(True)  # Enable mouse tracking for hover effects
        
    
    def setTopicName(self, name):
        """Set the topic name to display"""
        self.topic_name = name
        self.update()
    
    def draw_gear(self, painter, center, size, color):
        """Draw a gear icon"""
        teeth = 8
        outer_radius = size / 2
        inner_radius = outer_radius * 0.6
        tooth_height = outer_radius * 0.2
        center_hole_radius = outer_radius * 0.35
        
        path = QPainterPath()
        
        # Create gear teeth
        for i in range(teeth):
            angle1 = (i * 360 / teeth) * math.pi / 180
            angle2 = ((i + 0.4) * 360 / teeth) * math.pi / 180
            angle3 = ((i + 0.6) * 360 / teeth) * math.pi / 180
            angle4 = ((i + 1) * 360 / teeth) * math.pi / 180
            
            # Outer points
            x1 = center.x() + (outer_radius + tooth_height) * math.cos(angle1)
            y1 = center.y() + (outer_radius + tooth_height) * math.sin(angle1)
            x2 = center.x() + (outer_radius + tooth_height) * math.cos(angle2)
            y2 = center.y() + (outer_radius + tooth_height) * math.sin(angle2)
            
            # Inner points
            x3 = center.x() + outer_radius * math.cos(angle3)
            y3 = center.y() + outer_radius * math.sin(angle3)
            x4 = center.x() + outer_radius * math.cos(angle4)
            y4 = center.y() + outer_radius * math.sin(angle4)
            
            if i == 0:
                path.moveTo(x1, y1)
            else:
                path.lineTo(x1, y1)
            
            path.lineTo(x2, y2)
            path.lineTo(x3, y3)
            path.lineTo(x4, y4)
        
        path.closeSubpath()
        
        # Draw gear body
        painter.setBrush(color)
        painter.setPen(QPen(color, 2))
        painter.drawPath(path)
        
        # Draw center hole
        painter.setBrush(self.bg_color)
        painter.setPen(QPen(color, 2))
        painter.drawEllipse(center, center_hole_radius, center_hole_radius)

    def draw_dashed_line(self, painter, start, end):
        """Draw a curved dashed line between two points"""
        pen = QPen(Qt.GlobalColor.white, 2, Qt.PenStyle.DashDotDotLine)
        painter.setPen(pen)
        
        # Create a curved path using a quadratic bezier
        path = QPainterPath()
        path.moveTo(start)
        
        # Control point for curve (offset to create smooth curve)
        mid_x = (start.x() + end.x()) / 2
        mid_y = (start.y() + end.y()) / 2 + 50  # Curve downward
        control = QPointF(mid_x, mid_y)
        
        path.quadTo(control, end)
        painter.drawPath(path)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), self.bg_color)
        
        # Draw title
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        painter.setFont(QFont('Arial', 28, QFont.Weight.Bold))
        painter.drawText(50, 60, "Questions in ")
        
        # Draw topic name in black
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawText(305, 60, self.topic_name)
        
        # Draw dashed lines connecting gears
        for i in range(len(self.widgets) - 1):
            start = self.widgets[i]['center']
            end = self.widgets[i + 1]['center']
            self.draw_dashed_line(painter, start, end)
        
        # Draw gears
        for widget in self.widgets:
            center = widget['center']
            
            # Use lighter blue if hovered
            if widget['hovered']:
                color = QColor(80, 120, 255)
            else:
                color = QColor(40, 80, 220)
            
            self.draw_gear(painter, center, self.gear_size, color)
    
    def get_gear_rect(self, center):
        """Get bounding rectangle for gear collision detection"""
        half = self.gear_size / 2
        return QRect(
            int(center.x() - half),
            int(center.y() - half),
            int(self.gear_size),
            int(self.gear_size)
        )
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            
            # Check which gear was clicked
            for widget in self.widgets:
                rect = self.get_gear_rect(widget['center'])
                if rect.contains(pos):
                    self.clicked.emit(widget['id'])
                    print(f"Gear {widget['id']} clicked!")
                    break
    
    def mouseMoveEvent(self, event):
        pos = event.pos()
        needs_update = False
        
        # Update hover state for each gear
        for widget in self.widgets:
            rect = self.get_gear_rect(widget['center'])
            was_hovered = widget['hovered']
            widget['hovered'] = rect.contains(pos)
            if was_hovered != widget['hovered']:
                needs_update = True
        
        if needs_update:
            self.update()  # Trigger repaint
