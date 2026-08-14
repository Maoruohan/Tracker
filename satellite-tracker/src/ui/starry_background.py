"""
星空背景 - 动态星星效果
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
import math

class Star:
    """单颗星星"""
    def __init__(self, x, y, size, brightness, twinkle_speed):
        self.x = x
        self.y = y
        self.size = size
        self.base_brightness = brightness
        self.brightness = brightness
        self.twinkle_speed = twinkle_speed
        self.phase = random.uniform(0, 2 * math.pi)
    
    def update(self, dt):
        """更新星星闪烁"""
        self.phase += dt * self.twinkle_speed
        self.brightness = self.base_brightness * (0.6 + 0.4 * math.sin(self.phase))
    
    def draw(self, painter):
        """绘制星星"""
        alpha = int(self.brightness * 255)
        color = QColor(255, 255, 255, alpha)
        painter.setPen(QPen(color, self.size, Qt.SolidLine))
        painter.drawPoint(int(self.x), int(self.y))

class StarryBackground(QWidget):
    """星空背景组件"""
    
    def __init__(self, parent=None, num_stars=200):
        super().__init__(parent)
        self.num_stars = num_stars
        self.stars = []
        self.last_time = QDateTime.currentMSecsSinceEpoch()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stars)
        self.timer.start(50)  # 20fps
        
        # 设置透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        
        # 生成星星
        self.generate_stars()
    
    def generate_stars(self):
        """生成星星"""
        self.stars = []
        for _ in range(self.num_stars):
            x = random.randint(0, self.width())
            y = random.randint(0, self.height())
            size = random.uniform(0.5, 2.5)
            brightness = random.uniform(0.3, 1.0)
            speed = random.uniform(0.5, 3.0)
            self.stars.append(Star(x, y, size, brightness, speed))
    
    def update_stars(self):
        """更新星星闪烁"""
        now = QDateTime.currentMSecsSinceEpoch()
        dt = (now - self.last_time) / 1000.0
        self.last_time = now
        
        for star in self.stars:
            star.update(dt)
        
        self.update()  # 触发重绘
    
    def resizeEvent(self, event):
        """窗口大小变化时重新生成星星"""
        self.generate_stars()
        super().resizeEvent(event)
    
    def paintEvent(self, event):
        """绘制星空"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景渐变（深空蓝到紫）
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(10, 10, 30))
        gradient.setColorAt(0.3, QColor(13, 27, 42))
        gradient.setColorAt(0.6, QColor(26, 10, 46))
        gradient.setColorAt(1, QColor(10, 10, 30))
        painter.fillRect(self.rect(), gradient)
        
        # 绘制星星
        for star in self.stars:
            star.draw(painter)
        
        # 绘制几颗亮星带光晕
        for i in range(min(5, len(self.stars))):
            star = self.stars[i * 20]
            if star.base_brightness > 0.7:
                # 光晕
                glow = QRadialGradient(star.x, star.y, 20)
                glow.setColorAt(0, QColor(255, 255, 255, 30))
                glow.setColorAt(1, QColor(255, 255, 255, 0))
                painter.setBrush(glow)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPointF(star.x, star.y), 20, 20)
        
        painter.end()
        
        # 绘制子组件
        self._draw_children(event)
    
    def _draw_children(self, event):
        """绘制子组件（保持透明）"""
        for child in self.children():
            if isinstance(child, QWidget) and child.isVisible():
                # 让子组件自己绘制
                child.render(self, QPoint(child.x(), child.y()))
