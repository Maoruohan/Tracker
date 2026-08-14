"""
启动画面 - 虚化背景 + 进度条（稳定版）
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SplashScreen(QWidget):
    """启动画面"""
    
    def __init__(self):
        super().__init__()
        self.progress_value = 0
        self.init_ui()
        
        # 旋转动画
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)
    
    def init_ui(self):
        # 无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 窗口大小
        self.setFixedSize(480, 380)
        
        # 居中显示
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() // 2 - 240, screen.height() // 2 - 190)
        
        # 设置样式
        self.setStyleSheet("""
            QLabel {
                color: #c8dce8;
                font-family: 'Calibri', sans-serif;
                background: transparent;
            }
        """)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        
        # 1. 圆角矩形背景
        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, 20, 20)
        painter.setClipPath(path)
        
        # 2. 半透明毛玻璃背景
        painter.fillRect(0, 0, w, h, QColor(10, 15, 30, 230))
        
        # 3. 边框
        painter.setPen(QPen(QColor(80, 150, 200, 60), 1.5))
        painter.drawRoundedRect(1, 1, w-2, h-2, 19, 19)
        
        # 4. 顶部光晕
        grad = QRadialGradient(w//2, 0, w//2)
        grad.setColorAt(0, QColor(80, 180, 255, 30))
        grad.setColorAt(1, QColor(80, 180, 255, 0))
        painter.fillRect(0, 0, w, h//3, grad)
        
        painter.setClipPath(QPainterPath())
        
        # 5. 图标
        font = QFont("Segoe UI Emoji", 48)
        painter.setFont(font)
        painter.setPen(QColor(200, 230, 255))
        painter.drawText(0, 30, w, 70, Qt.AlignHCenter, "🛰️")
        
        # 6. 标题
        font = QFont("Calibri", 20, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(160, 210, 240))
        painter.drawText(0, 100, w, 30, Qt.AlignHCenter, "Satellite Tracker")
        
        # 7. 副标题
        font = QFont("Calibri", 11)
        painter.setFont(font)
        painter.setPen(QColor(100, 150, 190))
        painter.drawText(0, 130, w, 20, Qt.AlignHCenter, "卫星跟踪系统")
        
        # 8. 进度条
        bar_y = 200
        bar_w = 340
        bar_h = 6
        bar_x = (w - bar_w) // 2
        
        # 背景
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(40, 60, 90, 100))
        painter.drawRoundedRect(bar_x, bar_y, bar_w, bar_h, 3, 3)
        
        # 进度
        if self.progress_value > 0:
            grad2 = QLinearGradient(bar_x, 0, bar_x + bar_w, 0)
            grad2.setColorAt(0, QColor(80, 180, 255))
            grad2.setColorAt(0.5, QColor(120, 220, 255))
            grad2.setColorAt(1, QColor(160, 120, 255))
            painter.setBrush(grad2)
            pw = int((self.progress_value / 100) * bar_w)
            if pw > 0:
                painter.drawRoundedRect(bar_x, bar_y, pw, bar_h, 3, 3)
        
        # 9. 百分比
        font = QFont("Calibri", 12, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(140, 190, 220))
        painter.drawText(0, bar_y + 20, w, 25, Qt.AlignHCenter, f"{int(self.progress_value)}%")
        
        # 10. 状态文字
        font = QFont("Calibri", 10)
        painter.setFont(font)
        painter.setPen(QColor(90, 140, 180))
        painter.drawText(0, bar_y + 50, w, 20, Qt.AlignHCenter, self.get_status_text())
        
        # 11. 底部版本信息
        font = QFont("Calibri", 9)
        painter.setFont(font)
        painter.setPen(QColor(60, 100, 140, 120))
        painter.drawText(0, h - 30, w, 20, Qt.AlignHCenter, "v2.0 • Loading...")
        
        painter.end()
    
    def get_status_text(self):
        if self.progress_value < 20:
            return "初始化系统..."
        elif self.progress_value < 40:
            return "加载轨道数据..."
        elif self.progress_value < 60:
            return "连接卫星数据库..."
        elif self.progress_value < 80:
            return "准备跟踪系统..."
        elif self.progress_value < 95:
            return "即将就绪..."
        else:
            return "启动中..."
    
    def set_progress(self, value):
        self.progress_value = min(100, max(0, value))
        self.update()
    
    def animate(self):
        self.update()
    
    def closeEvent(self, event):
        self.timer.stop()
        event.accept()
