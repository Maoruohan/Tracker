#!/usr/bin/env python3
"""
Satellite Tracker - Main Application Entry Point
"""

import sys
import os
import argparse
from pathlib import Path
import yaml

# 重要：必须在导入 PyQt5 之前设置
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ui.main_window import SatelliteTrackerGUI
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap, QColor, QPainter, QFont, QPen, QRadialGradient, QLinearGradient


class SplashScreen(QSplashScreen):
    """启动画面"""
    
    def __init__(self):
        # 先初始化属性
        self.progress_value = 0
        self.status_index = 0
        self.status_texts = [
            "初始化系统...",
            "加载轨道数据...",
            "连接卫星数据库...",
            "准备跟踪系统...",
            "即将就绪...",
            "启动中..."
        ]
        
        # 创建空白像素图
        pixmap = QPixmap(480, 380)
        pixmap.fill(QColor(10, 15, 30, 0))
        
        super().__init__(pixmap)
        
        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 显示启动画面
        self.show()
        
        # 绘制初始界面
        self.draw_splash()
        
        # 定时更新进度
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)
    
    def draw_splash(self):
        """绘制启动画面"""
        pixmap = QPixmap(480, 380)
        pixmap.fill(QColor(10, 15, 30, 0))
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = 480, 380
        
        # 1. 背景
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(10, 15, 30, 230))
        painter.drawRoundedRect(0, 0, w, h, 20, 20)
        
        # 2. 边框
        painter.setPen(QPen(QColor(80, 150, 200, 60), 1.5))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(1, 1, w-2, h-2, 19, 19)
        
        # 3. 顶部光晕
        grad = QRadialGradient(w//2, 0, w//2)
        grad.setColorAt(0, QColor(80, 180, 255, 30))
        grad.setColorAt(1, QColor(80, 180, 255, 0))
        painter.fillRect(0, 0, w, h//3, grad)
        
        # 4. 图标
        font = QFont("Calibri", 48, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(200, 230, 255))
        painter.drawText(0, 30, w, 70, Qt.AlignHCenter, "🛰️")
        
        # 5. 标题
        font = QFont("Calibri", 20, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(160, 210, 240))
        painter.drawText(0, 100, w, 30, Qt.AlignHCenter, "Satellite Tracker")
        
        # 6. 副标题
        font = QFont("Calibri", 11)
        painter.setFont(font)
        painter.setPen(QColor(100, 150, 190))
        painter.drawText(0, 130, w, 20, Qt.AlignHCenter, "卫星跟踪系统")
        
        # 7. 进度条
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
        
        # 8. 百分比
        font = QFont("Calibri", 12, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(140, 190, 220))
        painter.drawText(0, bar_y + 20, w, 25, Qt.AlignHCenter, f"{int(self.progress_value)}%")
        
        # 9. 状态文字
        font = QFont("Calibri", 10)
        painter.setFont(font)
        painter.setPen(QColor(90, 140, 180))
        status = self.status_texts[min(self.status_index, len(self.status_texts)-1)]
        painter.drawText(0, bar_y + 50, w, 20, Qt.AlignHCenter, status)
        
        # 10. 底部 - v2.0
        font = QFont("Calibri", 9)
        painter.setFont(font)
        painter.setPen(QColor(60, 100, 140, 120))
        painter.drawText(0, h - 50, w, 20, Qt.AlignHCenter, "v2.0 • Loading...")
        
        # 11. 底部 - by Ryan 2026.8.14
        font = QFont("Calibri", 9)
        painter.setFont(font)
        painter.setPen(QColor(80, 130, 170, 100))
        painter.drawText(0, h - 28, w, 20, Qt.AlignHCenter, "by Ryan 2026.8.14")
        
        painter.end()
        
        self.setPixmap(pixmap)
    
    def update_progress(self):
        """更新进度"""
        self.progress_value += 3
        if self.progress_value % 20 < 3:
            self.status_index = min(self.status_index + 1, len(self.status_texts)-1)
        
        if self.progress_value >= 100:
            self.timer.stop()
            self.progress_value = 100
        
        self.draw_splash()
        QApplication.processEvents()


def load_config(config_path=None):
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    
    default_config = {
        'observer': {'latitude': "44.7739", 'longitude': "-76.6872", 'altitude': 100},
        'hardware': {
            'arduino': {'enabled': False, 'port': None, 'baud_rate': 115200},
            'rotctld': {'enabled': False, 'host': "127.0.0.1", 'port': 4533}
        },
        'tracking': {
            'tle_update_minutes': 10,
            'tracking_interval': 2.5,
            'position_read_interval': 2.5,
            'gear_ratio_azimuth': 3.0
        },
        'ui': {'theme': 'dark', 'refresh_rate': 10, 'show_debug': False},
        'cache': {'directory': 'tle_cache', 'max_age_days': 7}
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                for key in default_config:
                    if key not in config:
                        config[key] = default_config[key]
                return config
        except:
            return default_config
    else:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        return default_config


def main():
    parser = argparse.ArgumentParser(description='Satellite Tracker')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    args = parser.parse_args()
    config = load_config()
    
    if args.headless:
        print("Headless mode not implemented yet")
        return
    
    app = QApplication(sys.argv)
    app.setApplicationName("Satellite Tracker")
    
    # 显示启动画面
    splash = SplashScreen()
    
    # 创建主窗口
    def show_main_window():
        window = SatelliteTrackerGUI(config)
        window.show()
        splash.close()
    
    # 延迟加载，让启动画面显示一会儿
    QTimer.singleShot(1500, show_main_window)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
