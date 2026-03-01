import sys
import math
import time
import threading
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QRadialGradient, QPen, QBrush

_orb_window = None
_state = "idle"

class OrbWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS")
        self.setFixedSize(300, 300)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        self.state = "idle"
        self.pulse = 0
        self.rings = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

        # Position bottom right
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 320, screen.height() - 350)

    def set_state(self, state):
        self.state = state
        if state == "listening":
            self.rings = [0, 0.3, 0.6]

    def animate(self):
        global _state
        if self.state != _state:
            self.set_state(_state)

        self.pulse = (self.pulse + 0.05) % (2 * math.pi)
        self.rings = [r + 0.02 for r in self.rings if r < 1.5]
        if self.state == "listening" and (not self.rings or self.rings[-1] > 0.3):
            if len(self.rings) < 3:
                self.rings.append(0)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        cx, cy = 150, 150

        if self.state == "idle":
            core_colour = QColor(0, 180, 255, 180)
            glow_colour = QColor(0, 100, 200, 60)
        elif self.state == "listening":
            core_colour = QColor(0, 255, 180, 220)
            glow_colour = QColor(0, 200, 150, 80)
        elif self.state == "processing":
            core_colour = QColor(255, 165, 0, 220)
            glow_colour = QColor(200, 100, 0, 80)
        elif self.state == "speaking":
            core_colour = QColor(0, 255, 100, 220)
            glow_colour = QColor(0, 200, 80, 80)
        else:
            core_colour = QColor(0, 180, 255, 180)
            glow_colour = QColor(0, 100, 200, 60)

        # Expanding rings
        for ring in self.rings:
            radius = int(60 + ring * 100)
            alpha = max(0, int(150 * (1 - ring / 1.5)))
            ring_colour = QColor(core_colour)
            ring_colour.setAlpha(alpha)
            pen = QPen(ring_colour, 2)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)

        # Outer glow
        pulse_size = int(5 * math.sin(self.pulse))
        for i in range(5):
            glow_alpha = int(40 - i * 8)
            if glow_alpha <= 0:
                continue
            glow = QColor(glow_colour)
            glow.setAlpha(glow_alpha)
            size = 120 + i * 12 + pulse_size
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(glow))
            painter.drawEllipse(cx - size // 2, cy - size // 2, size, size)

        # Core gradient
        gradient = QRadialGradient(cx, cy, 60)
        gradient.setColorAt(0, QColor(255, 255, 255, 200))
        gradient.setColorAt(0.3, core_colour)
        gradient.setColorAt(1, QColor(core_colour.red(), core_colour.green(), core_colour.blue(), 0))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        core_size = int(100 + pulse_size * 2)
        painter.drawEllipse(cx - core_size // 2, cy - core_size // 2, core_size, core_size)

        # Inner bright core
        inner_gradient = QRadialGradient(cx, cy, 25)
        inner_gradient.setColorAt(0, QColor(255, 255, 255, 240))
        inner_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(inner_gradient))
        painter.drawEllipse(cx - 25, cy - 25, 50, 50)

        # Rotating arc when processing
        if self.state == "processing":
            pen = QPen(QColor(255, 165, 0, 200), 3)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            angle = int(self.pulse * 180 / math.pi * 16)
            painter.drawArc(cx - 70, cy - 70, 140, 140, angle, 120 * 16)

        # Speaking bars
        if self.state == "speaking":
            bar_count = 5
            bar_width = 6
            bar_gap = 10
            total_width = bar_count * (bar_width + bar_gap)
            start_x = cx - total_width // 2
            for i in range(bar_count):
                height = int(20 + 15 * math.sin(self.pulse * 3 + i * 0.8))
                painter.setBrush(QBrush(QColor(0, 255, 100, 200)))
                painter.setPen(Qt.PenStyle.NoPen)
                x = start_x + i * (bar_width + bar_gap)
                painter.drawRoundedRect(x, cy - height // 2, bar_width, height, 3, 3)

def set_orb_state(state):
    """Set orb state from anywhere — thread safe via global"""
    global _state
    _state = state

def launch_orb():
    """Must be called from main thread"""
    global _orb_window
    app = QApplication.instance() or QApplication(sys.argv)
    _orb_window = OrbWidget()
    _orb_window.show()