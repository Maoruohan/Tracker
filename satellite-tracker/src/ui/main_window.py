"""
卫星跟踪器主窗口 - 带中英双语切换
"""

import sys
import time
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ..tracker import SatelliteTracker
from ..tle_manager import TLEManager
from ..arduino_controller import ArduinoController
from ..satellite_db import find_satellite, get_all_satellites
from .starry_background import StarryBackground
from .location_search import LocationSearchWidget, CoordinatesInputWidget
from .settings_tab import SettingsTab
from .languages import tr, set_language, get_language

class WorkerSignals(QObject):
    position_updated = pyqtSignal(float, float, float)
    status_updated = pyqtSignal(str)
    error = pyqtSignal(str)

class TrackingWorker(QRunnable):
    def __init__(self, tracker, arduino, tle_manager, norad_id, sat_name, config):
        super().__init__()
        self.tracker = tracker
        self.arduino = arduino
        self.tle_manager = tle_manager
        self.norad_id = norad_id
        self.sat_name = sat_name
        self.config = config
        self.running = True
        self.signals = WorkerSignals()
        self.last_tle_update = 0
        self.start_time = time.time()
    
    def run(self):
        while self.running:
            try:
                now = time.time()
                if now - self.last_tle_update >= self.config['tracking']['tle_update_minutes'] * 60:
                    tle = self.tle_manager.fetch_tle(self.norad_id, self.sat_name, force_refresh=True)
                    if tle:
                        name, tle1, tle2 = tle
                        self.tracker.set_tle(name, tle1, tle2)
                    self.last_tle_update = now
                az, el, rng, raw_el = self.tracker.compute_position()
                self.signals.position_updated.emit(az, el, rng)
                if self.arduino and self.arduino.connected:
                    gear = self.config['tracking']['gear_ratio_azimuth']
                    motor_az = (az * gear) % 360.0
                    self.arduino.set_position(motor_az, el)
                elapsed = now - self.start_time
                status = f"Tracking ({elapsed:.0f}s)" if raw_el >= 0 else f"Below horizon ({elapsed:.0f}s)"
                self.signals.status_updated.emit(status)
                time.sleep(self.config['tracking']['tracking_interval'])
            except Exception as e:
                self.signals.error.emit(str(e))
                break
    
    def stop(self):
        self.running = False

class SatelliteTrackerGUI(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.tracker = None
        self.arduino = None
        self.tle_manager = TLEManager(
            cache_dir=config['cache']['directory'],
            max_age_days=config['cache']['max_age_days']
        )
        self.worker = None
        self.thread_pool = QThreadPool()
        self.start_time = None
        self.data_labels = {}
        self.init_ui()
        self.init_tracker()
        self.init_arduino()
    
    def init_ui(self):
        self.setWindowTitle(tr('app_title'))
        self.setGeometry(100, 100, 1400, 900)
        
        central_widget = StarryBackground(self, num_stars=250)
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        title_layout = QHBoxLayout()
        
        self.title_label = QLabel(tr('app_title'))
        self.title_label.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #7a9bb5;
            font-family: 'Calibri', 'Courier New', monospace;
            padding: 12px;
            background: rgba(20, 30, 45, 0.5);
            border: 1px solid rgba(100, 150, 200, 0.2);
            border-radius: 10px;
        """)
        title_layout.addWidget(self.title_label)
        
        lang_widget = QWidget()
        lang_layout = QHBoxLayout(lang_widget)
        lang_layout.setContentsMargins(0, 0, 0, 0)
        lang_layout.setSpacing(5)
        
        lang_layout.addStretch()
        lang_layout.addWidget(QLabel("🌐"))
        
        self.lang_btn_zh = QPushButton("中文")
        self.lang_btn_zh.clicked.connect(lambda: self.switch_language("zh"))
        self.lang_btn_zh.setStyleSheet("""
            QPushButton {
                background: #2a3a4a;
                color: #7a9bb5;
                border: 1px solid #4a6a8a;
                border-radius: 5px;
                padding: 6px 20px;
                font-family: 'Calibri', 'Courier New', monospace;
                font-size: 13px;
                font-weight: bold;
                min-width: 80px;
                min-height: 30px;
            }
            QPushButton:hover { background: #3a4a5a; }
        """)
        
        self.lang_btn_en = QPushButton("English")
        self.lang_btn_en.clicked.connect(lambda: self.switch_language("en"))
        self.lang_btn_en.setStyleSheet("""
            QPushButton {
                background: #2a3a4a;
                color: #7a9bb5;
                border: 1px solid #4a6a8a;
                border-radius: 5px;
                padding: 6px 20px;
                font-family: 'Calibri', 'Courier New', monospace;
                font-size: 13px;
                min-width: 80px;
                min-height: 30px;
            }
            QPushButton:hover { background: #3a4a5a; }
        """)
        
        lang_layout.addWidget(self.lang_btn_zh)
        lang_layout.addWidget(self.lang_btn_en)
        title_layout.addWidget(lang_widget)
        main_layout.addLayout(title_layout)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(80, 130, 180, 0.2);
                border-radius: 10px;
                background: rgba(15, 25, 40, 0.4);
            }
            QTabBar::tab {
                min-width: 100px;
                padding: 10px 25px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Calibri', 'Courier New', monospace;
            }
        """)
        
        # === 跟踪标签页 ===
        tracking_tab = QWidget()
        tracking_layout = QVBoxLayout(tracking_tab)
        tracking_layout.setSpacing(10)
        
        self.sat_selection_group = QGroupBox(tr('satellite_selection'))
        self.sat_selection_group.setStyleSheet(self.get_group_style())
        selection_layout = QHBoxLayout()
        selection_layout.setSpacing(15)
        
        self.target_label = QLabel(tr('target'))
        self.target_label.setStyleSheet("color: #8aacb5; font-family: 'Calibri', 'Courier New', monospace; font-weight: bold;")
        selection_layout.addWidget(self.target_label)
        
        self.sat_combo = QComboBox()
        self.sat_combo.addItems(get_all_satellites())
        self.sat_combo.setEditable(True)
        self.sat_combo.setMinimumWidth(250)
        self.sat_combo.setStyleSheet(self.get_combo_style())
        
        self.select_button = QPushButton(tr('start_tracking'))
        self.select_button.clicked.connect(self.start_tracking)
        self.select_button.setMinimumWidth(140)
        self.select_button.setStyleSheet(self.get_button_style())
        
        self.stop_button = QPushButton(tr('stop_tracking'))
        self.stop_button.clicked.connect(self.stop_tracking)
        self.stop_button.setEnabled(False)
        self.stop_button.setMinimumWidth(120)
        self.stop_button.setStyleSheet(self.get_button_style())
        
        self.sat_label = QLabel(tr('satellite'))
        self.sat_label.setStyleSheet("color: #8aacb5; font-family: 'Calibri', 'Courier New', monospace; font-weight: bold;")
        selection_layout.addWidget(self.sat_label)
        selection_layout.addWidget(self.sat_combo)
        selection_layout.addWidget(self.select_button)
        selection_layout.addWidget(self.stop_button)
        selection_layout.addStretch()
        self.sat_selection_group.setLayout(selection_layout)
        tracking_layout.addWidget(self.sat_selection_group)
        
        data_map_layout = QHBoxLayout()
        data_map_layout.setSpacing(15)
        
        self.data_group = QGroupBox(tr('telemetry'))
        self.data_group.setStyleSheet(self.get_group_style())
        data_layout = QGridLayout()
        data_layout.setSpacing(10)
        
        label_style = "font-size: 13px; font-weight: bold; color: #6a8a9a; font-family: 'Calibri', 'Courier New', monospace; font-weight: bold;"
        value_style = """
            font-size: 18px;
            font-weight: bold;
            color: #7a9bb5;
            font-family: 'Calibri', 'Courier New', monospace;
            font-weight: bold;
            background: rgba(20, 30, 50, 0.4);
            border: 1px solid rgba(80, 130, 180, 0.15);
            border-radius: 8px;
            padding: 8px 15px;
        """
        
        data_items = [
            ("satellite_name", "sat_name_label"),
            ("azimuth", "az_label"),
            ("elevation", "el_label"),
            ("range", "rng_label"),
            ("status", "status_label"),
            ("elapsed", "elapsed_label")
        ]
        
        self.data_widgets = {}
        for i, (key, widget_name) in enumerate(data_items):
            label = QLabel(tr(key))
            label.setStyleSheet(label_style)
            self.data_labels[key] = label
            widget = QLabel(tr('initializing'))
            widget.setStyleSheet(value_style)
            widget.setMinimumWidth(120)
            self.data_widgets[widget_name] = widget
            data_layout.addWidget(label, i, 0)
            data_layout.addWidget(widget, i, 1)
        
        self.data_group.setLayout(data_layout)
        data_map_layout.addWidget(self.data_group, stretch=1)
        
        self.map_group = QGroupBox(tr('sky_map'))
        self.map_group.setStyleSheet(self.get_group_style())
        map_layout = QVBoxLayout()
        self.sky_map_label = QLabel()
        self.sky_map_label.setAlignment(Qt.AlignCenter)
        self.sky_map_label.setMinimumHeight(380)
        self.sky_map_label.setStyleSheet("""
            background: rgba(10, 18, 30, 0.6);
            border: 1px solid rgba(80, 130, 180, 0.15);
            border-radius: 10px;
            padding: 15px;
            font-family: 'Calibri', 'Courier New', monospace;
            color: #6a8a9a;
        """)
        self.sky_map_label.setFont(QFont("Calibri", 11))
        self.update_sky_map(0, 0)
        map_layout.addWidget(self.sky_map_label)
        self.map_group.setLayout(map_layout)
        data_map_layout.addWidget(self.map_group, stretch=1)
        
        tracking_layout.addLayout(data_map_layout)
        tracking_tab.setLayout(tracking_layout)
        self.tab_widget.addTab(tracking_tab, tr('tab_tracking'))
        
        # === 位置标签页 ===
        location_tab = QWidget()
        location_layout = QVBoxLayout(location_tab)
        location_layout.setSpacing(15)
        
        self.location_search = LocationSearchWidget()
        self.location_search.location_selected.connect(self.on_location_selected)
        location_layout.addWidget(self.location_search)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: rgba(80, 130, 180, 0.15); max-height: 1px;")
        location_layout.addWidget(line)
        
        self.coord_group = QGroupBox(tr('manual_input'))
        self.coord_group.setStyleSheet(self.get_group_style())
        coord_layout = QVBoxLayout()
        self.coord_input = CoordinatesInputWidget()
        self.coord_input.coordinate_entered.connect(self.on_coordinate_entered)
        coord_layout.addWidget(self.coord_input)
        self.coord_group.setLayout(coord_layout)
        location_layout.addWidget(self.coord_group)
        
        location_layout.addStretch()
        location_tab.setLayout(location_layout)
        self.tab_widget.addTab(location_tab, tr('tab_location'))
        
        # === 设置标签页 ===
        self.settings_tab = SettingsTab(self.config)
        self.settings_tab.settings_changed.connect(self.on_settings_changed)
        self.tab_widget.addTab(self.settings_tab, "设置")
        
        main_layout.addWidget(self.tab_widget)
        
        # === 状态栏 ===
        self.status_group = QGroupBox(tr('system_status'))
        self.status_group.setStyleSheet(self.get_group_style())
        status_layout = QHBoxLayout()
        
        self.arduino_status_label = QLabel(tr('arduino_disabled'))
        self.arduino_status_label.setStyleSheet("color: #6a8a8a; font-weight: bold; font-family: 'Calibri', 'Courier New', monospace;")
        status_layout.addWidget(self.arduino_status_label)
        
        self.tle_status_label = QLabel(tr('tle_ready_status'))
        self.tle_status_label.setStyleSheet("color: #6a8a8a; font-weight: bold; font-family: 'Calibri', 'Courier New', monospace;")
        status_layout.addWidget(self.tle_status_label)
        
        self.location_label = QLabel(f"📍 {self.config['observer']['latitude']}, {self.config['observer']['longitude']}")
        self.location_label.setStyleSheet("color: #7a9bb5; font-family: 'Calibri', 'Courier New', monospace; font-weight: bold;")
        status_layout.addWidget(self.location_label)
        
        status_layout.addStretch()
        
        self.status_bar_label = QLabel(tr('system_ready'))
        self.status_bar_label.setStyleSheet("color: #6a8a8a; font-weight: bold; font-family: 'Calibri', 'Courier New', monospace; font-size: 14px; font-weight: bold;")
        status_layout.addWidget(self.status_bar_label)
        
        self.status_group.setLayout(status_layout)
        main_layout.addWidget(self.status_group)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_elapsed_time)
        self.timer.start(1000)
    
    def get_group_style(self):
        return """
            QGroupBox {
                color: #7a9bb5;
                border: 1px solid rgba(80, 130, 180, 0.15);
                border-radius: 10px;
                margin-top: 12px;
                font-family: 'Calibri', 'Courier New', monospace;
                font-weight: bold;
                background: rgba(15, 25, 40, 0.3);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                color: #7a9bb5;
            }
        """
    
    def get_button_style(self):
        return """
            QPushButton {
                background: #2a3a4a;
                color: #8aacb5;
                border: 1px solid #3a5a6a;
                border-radius: 8px;
                padding: 10px 25px;
                font-weight: bold;
                font-family: 'Calibri', 'Courier New', monospace;
                font-size: 13px;
            }
            QPushButton:hover { background: #3a4a5a; }
            QPushButton:disabled {
                background: #1a2a3a;
                color: #4a5a6a;
                border-color: #2a3a4a;
            }
        """
    
    def get_combo_style(self):
        return """
            QComboBox {
                background: rgba(20, 30, 50, 0.6);
                color: #8aacb5;
                border: 1px solid rgba(80, 130, 180, 0.15);
                border-radius: 8px;
                padding: 8px 15px;
                min-width: 180px;
                font-family: 'Calibri', 'Courier New', monospace;
                font-weight: bold;
                font-size: 13px;
            }
            QComboBox:hover { border-color: #4a6a8a; }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background: #1a2a3a;
                color: #8aacb5;
                border: 1px solid #3a5a6a;
                selection-background-color: #2a3a4a;
            }
        """
    
    def update_lang_buttons(self):
        current = get_language()
        for btn, lang in [(self.lang_btn_zh, 'zh'), (self.lang_btn_en, 'en')]:
            if lang == current:
                btn.setStyleSheet("""
                    QPushButton {
                        background: #3a4a5a;
                        color: #aacce5;
                        border: 1px solid #5a8aaa;
                        border-radius: 5px;
                        padding: 6px 20px;
                        font-family: 'Calibri', 'Courier New', monospace;
                        font-size: 13px;
                        font-weight: bold;
                        min-width: 80px;
                        min-height: 30px;
                    }
                    QPushButton:hover { background: #4a5a6a; }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: #2a3a4a;
                        color: #7a9bb5;
                        border: 1px solid #4a6a8a;
                        border-radius: 5px;
                        padding: 6px 20px;
                        font-family: 'Calibri', 'Courier New', monospace;
                        font-size: 13px;
                        min-width: 80px;
                        min-height: 30px;
                    }
                    QPushButton:hover { background: #3a4a5a; }
                """)
    
    def switch_language(self, lang):
        set_language(lang)
        self.update_lang_buttons()
        self.update_ui_texts()
    
    def update_ui_texts(self):
        self.title_label.setText(tr('app_title'))
        self.setWindowTitle(tr('app_title'))
        
        self.tab_widget.setTabText(0, tr('tab_tracking'))
        self.tab_widget.setTabText(1, tr('tab_location'))
        if get_language() == 'zh':
            self.tab_widget.setTabText(2, "设置")
        else:
            self.tab_widget.setTabText(2, "Settings")
        
        self.sat_selection_group.setTitle(tr('satellite_selection'))
        self.target_label.setText(tr('target'))
        self.sat_label.setText(tr('satellite'))
        self.select_button.setText(tr('start_tracking'))
        self.stop_button.setText(tr('stop_tracking'))
        self.data_group.setTitle(tr('telemetry'))
        self.map_group.setTitle(tr('sky_map'))
        self.status_group.setTitle(tr('system_status'))
        
        for key, label in self.data_labels.items():
            label.setText(tr(key))
        
        if not self.worker:
            for widget_name in self.data_widgets:
                self.data_widgets[widget_name].setText(tr('initializing'))
            self.status_bar_label.setText(tr('system_ready'))
        
        if hasattr(self, 'location_search'):
            self.location_search.update_language()
        if hasattr(self, 'coord_input'):
            self.coord_input.update_language()
        if hasattr(self, 'coord_group'):
            self.coord_group.setTitle(tr('manual_input'))
        if hasattr(self, 'settings_tab'):
            self.settings_tab.update_language()
        
        self.arduino_status_label.setText(tr('arduino_disabled'))
        self.tle_status_label.setText(tr('tle_ready_status'))
    
    def on_settings_changed(self):
        if self.worker:
            self.stop_tracking()
            self.start_tracking()
    
    def on_location_selected(self, lat, lon, name):
        self.config['observer']['latitude'] = str(lat)
        self.config['observer']['longitude'] = str(lon)
        short_name = name[:25] + '...' if len(name) > 25 else name
        self.location_label.setText(f"📍 {short_name} ({lat:.4f}, {lon:.4f})")
        self.init_tracker()
        if self.worker:
            self.stop_tracking()
            self.start_tracking()
        QMessageBox.information(self, tr('success'), tr('location_updated_msg', name=name, lat=lat, lon=lon))
    
    def on_coordinate_entered(self, lat, lon):
        self.config['observer']['latitude'] = str(lat)
        self.config['observer']['longitude'] = str(lon)
        self.location_label.setText(tr('custom_location', lat=lat, lon=lon))
        self.init_tracker()
        if self.worker:
            self.stop_tracking()
            self.start_tracking()
        QMessageBox.information(self, tr('success'), tr('location_updated_msg', name='自定义坐标', lat=lat, lon=lon))
    
    def init_tracker(self):
        obs = self.config['observer']
        self.tracker = SatelliteTracker(obs['latitude'], obs['longitude'], obs['altitude'])
    
    def init_arduino(self):
        if self.config['hardware']['arduino']['enabled']:
            self.arduino = ArduinoController(
                port=self.config['hardware']['arduino']['port'],
                baud_rate=self.config['hardware']['arduino']['baud_rate']
            )
            if self.arduino.connect():
                self.arduino_status_label.setText(tr('arduino_connected'))
                self.arduino_status_label.setStyleSheet("color: #5aaa8a; font-weight: bold; font-family: 'Calibri', 'Courier New', monospace;")
            else:
                self.arduino_status_label.setText(tr('arduino_failed'))
                self.arduino_status_label.setStyleSheet("color: #aa6a6a; font-weight: bold; font-family: 'Calibri', 'Courier New', monospace;")
        else:
            self.arduino = None
            self.arduino_status_label.setText(tr('arduino_disabled'))
            self.arduino_status_label.setStyleSheet("color: #8a8a6a; font-weight: bold; font-family: 'Calibri', 'Courier New', monospace;")
    
    def start_tracking(self):
        sat_text = self.sat_combo.currentText()
        sat_info = find_satellite(sat_text)
        if sat_info is None:
            QMessageBox.warning(self, tr('error'), tr('sat_not_found', sat=sat_text))
            return
        sat_name, norad_id = sat_info
        self.status_bar_label.setText(tr('fetching_tle'))
        self.status_bar_label.setStyleSheet("color: #8a8a6a; font-weight: bold; font-family: 'Calibri', 'Courier New', monospace;")
        tle = self.tle_manager.fetch_tle(norad_id, sat_name)
        if tle is None:
            QMessageBox.warning(self, tr('error'), tr('tle_fetch_failed', sat=sat_name))
            self.status_bar_label.setText(tr('tle_failed'))
            self.status_bar_label.setStyleSheet("color: #aa6a6a; font-weight: bold; font-family: 'Calibri', 'Courier New', monospace;")
            return
        name, tle1, tle2 = tle
        self.tracker.set_tle(name, tle1, tle2)
        self.worker = TrackingWorker(
            self.tracker, self.arduino, self.tle_manager,
            norad_id, sat_name, self.config
        )
        self.worker.signals.position_updated.connect(self.update_position)
        self.worker.signals.status_updated.connect(self.update_status)
        self.worker.signals.error.connect(self.show_error)
        self.thread_pool.start(self.worker)
        self.select_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_bar_label.setText(f"● {tr('tracking')}: {sat_name}")
        self.status_bar_label.setStyleSheet("color: #5aaa8a; font-weight: bold; font-family: 'Calibri', 'Courier New', monospace;")
        self.start_time = time.time()
        self.data_widgets['sat_name_label'].setText(sat_name)
        self.tle_status_label.setText(tr('tle_loaded_status'))
        self.tle_status_label.setStyleSheet("color: #5aaa8a; font-weight: bold; font-family: 'Calibri', 'Courier New', monospace;")
    
    def stop_tracking(self):
        if self.worker:
            self.worker.stop()
            self.worker = None
        self.select_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_bar_label.setText(tr('stopped'))
        self.status_bar_label.setStyleSheet("color: #8a8a6a; font-weight: bold; font-family: 'Calibri', 'Courier New', monospace;")
        if self.arduino and self.arduino.connected:
            self.arduino.set_position(0, 0)
    
    def update_position(self, az, el, rng):
        self.data_widgets['az_label'].setText(f"{az:.2f}{tr('degrees')}")
        self.data_widgets['el_label'].setText(f"{el:.2f}{tr('degrees')}")
        self.data_widgets['rng_label'].setText(f"{rng:.2f} {tr('kilometers')}")
        self.update_sky_map(az, el)
    
    def update_status(self, status):
        self.data_widgets['status_label'].setText(status)
        if "Tracking" in status:
            self.data_widgets['status_label'].setStyleSheet("font-size: 18px; font-weight: bold; color: #5aaa8a;")
        elif "horizon" in status:
            self.data_widgets['status_label'].setStyleSheet("font-size: 18px; font-weight: bold; color: #8a8a6a;")
    
    def update_elapsed_time(self):
        if self.start_time:
            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.data_widgets['elapsed_label'].setText(tr('hours').format(hours, minutes, seconds))
    
    def update_sky_map(self, az, el, width=45, height=23):
        grid = [[" " for _ in range(width)] for _ in range(height)]
        center_x = width // 2
        center_y = height // 2
        max_radius = min(center_x, center_y) - 1
        
        el_clamped = max(0, min(90, el))
        radius = int((1.0 - el_clamped / 90.0) * max_radius)
        rad_az = math.radians(az - 90)
        x = center_x + int(radius * math.cos(rad_az))
        y = center_y + int(radius * math.sin(rad_az))
        x = max(0, min(width - 1, x))
        y = max(0, min(height - 1, y))
        
        if height > 2 and width > 2:
            grid[0][center_x] = tr('north')
            grid[height - 1][center_x] = tr('south')
            grid[center_y][0] = tr('west')
            grid[center_y][width - 1] = tr('east')
        
        for elev in [15, 30, 45, 60, 75]:
            ring_radius = int((1.0 - elev / 90.0) * max_radius)
            if ring_radius >= 1:
                if center_y - ring_radius >= 0:
                    grid[center_y - ring_radius][center_x] = "·"
                if center_y + ring_radius < height:
                    grid[center_y + ring_radius][center_x] = "·"
                if center_x - ring_radius >= 0:
                    grid[center_y][center_x - ring_radius] = "·"
                if center_x + ring_radius < width:
                    grid[center_y][center_x + ring_radius] = "·"
        
        grid[center_y][center_x] = tr('zenith')
        if el >= 0:
            grid[y][x] = tr('satellite_symbol')
        
        map_text = "┌" + "─" * width + "┐\n"
        for row in grid:
            map_text += "│" + "".join(row) + "│\n"
        map_text += "└" + "─" * width + "┘"
        self.sky_map_label.setText(map_text)
    
    def show_error(self, error):
        QMessageBox.warning(self, tr('error'), f"❌ {error}")
