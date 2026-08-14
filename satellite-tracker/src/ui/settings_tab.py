"""
设置页面 - 调整跟踪参数
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .languages import get_language

class SettingsTab(QWidget):
    """设置页面"""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # 标题 - 直接显示
        self.title_label = QLabel()
        self.title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #7a9bb5;
            font-family: 'Calibri', 'Courier New', monospace;
            padding: 10px;
        """)
        layout.addWidget(self.title_label)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar { background: rgba(20,30,50,0.4); border: 1px solid rgba(80,130,180,0.15); border-radius: 5px; }
            QScrollBar::handle { background: #2a3a4a; border-radius: 5px; }
        """)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(12)
        
        # 跟踪参数
        self.tracking_group = QGroupBox()
        self.tracking_group.setStyleSheet(self.get_group_style())
        tracking_layout = QGridLayout()
        tracking_layout.setSpacing(10)
        
        self.tracking_interval_label = QLabel()
        self.tracking_interval_label.setStyleSheet("color: #6a8a9a; font-family: 'Calibri', 'Courier New', monospace; font-weight: bold;")
        tracking_layout.addWidget(self.tracking_interval_label, 0, 0)
        self.tracking_interval_spin = QDoubleSpinBox()
        self.tracking_interval_spin.setRange(0.5, 10.0)
        self.tracking_interval_spin.setSingleStep(0.5)
        self.tracking_interval_spin.setValue(self.config['tracking']['tracking_interval'])
        self.tracking_interval_spin.setStyleSheet(self.get_spin_style())
        tracking_layout.addWidget(self.tracking_interval_spin, 0, 1)
        self.tracking_interval_unit = QLabel()
        self.tracking_interval_unit.setStyleSheet("color: #6a8a9a; font-family: 'Calibri', 'Courier New', monospace;")
        tracking_layout.addWidget(self.tracking_interval_unit, 0, 2)
        
        self.tle_update_label = QLabel()
        self.tle_update_label.setStyleSheet("color: #6a8a9a; font-family: 'Calibri', 'Courier New', monospace; font-weight: bold;")
        tracking_layout.addWidget(self.tle_update_label, 1, 0)
        self.tle_update_spin = QSpinBox()
        self.tle_update_spin.setRange(1, 60)
        self.tle_update_spin.setValue(self.config['tracking']['tle_update_minutes'])
        self.tle_update_spin.setStyleSheet(self.get_spin_style())
        tracking_layout.addWidget(self.tle_update_spin, 1, 1)
        self.tle_update_unit = QLabel()
        self.tle_update_unit.setStyleSheet("color: #6a8a9a; font-family: 'Calibri', 'Courier New', monospace;")
        tracking_layout.addWidget(self.tle_update_unit, 1, 2)
        
        self.position_read_label = QLabel()
        self.position_read_label.setStyleSheet("color: #6a8a9a; font-family: 'Calibri', 'Courier New', monospace; font-weight: bold;")
        tracking_layout.addWidget(self.position_read_label, 2, 0)
        self.position_read_spin = QDoubleSpinBox()
        self.position_read_spin.setRange(0.5, 10.0)
        self.position_read_spin.setSingleStep(0.5)
        self.position_read_spin.setValue(self.config['tracking']['position_read_interval'])
        self.position_read_spin.setStyleSheet(self.get_spin_style())
        tracking_layout.addWidget(self.position_read_spin, 2, 1)
        self.position_read_unit = QLabel()
        self.position_read_unit.setStyleSheet("color: #6a8a9a; font-family: 'Calibri', 'Courier New', monospace;")
        tracking_layout.addWidget(self.position_read_unit, 2, 2)
        
        self.gear_ratio_label = QLabel()
        self.gear_ratio_label.setStyleSheet("color: #6a8a9a; font-family: 'Calibri', 'Courier New', monospace; font-weight: bold;")
        tracking_layout.addWidget(self.gear_ratio_label, 3, 0)
        self.gear_ratio_spin = QDoubleSpinBox()
        self.gear_ratio_spin.setRange(0.5, 10.0)
        self.gear_ratio_spin.setSingleStep(0.5)
        self.gear_ratio_spin.setValue(self.config['tracking']['gear_ratio_azimuth'])
        self.gear_ratio_spin.setStyleSheet(self.get_spin_style())
        tracking_layout.addWidget(self.gear_ratio_spin, 3, 1)
        self.gear_ratio_unit = QLabel()
        self.gear_ratio_unit.setStyleSheet("color: #6a8a9a; font-family: 'Calibri', 'Courier New', monospace;")
        tracking_layout.addWidget(self.gear_ratio_unit, 3, 2)
        
        self.tracking_group.setLayout(tracking_layout)
        content_layout.addWidget(self.tracking_group)
        
        # Arduino 参数
        self.arduino_group = QGroupBox()
        self.arduino_group.setStyleSheet(self.get_group_style())
        arduino_layout = QGridLayout()
        arduino_layout.setSpacing(10)
        
        self.baud_label = QLabel()
        self.baud_label.setStyleSheet("color: #6a8a9a; font-family: 'Calibri', 'Courier New', monospace; font-weight: bold;")
        arduino_layout.addWidget(self.baud_label, 0, 0)
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(['9600', '19200', '38400', '57600', '115200', '230400'])
        self.baud_combo.setCurrentText(str(self.config['hardware']['arduino']['baud_rate']))
        self.baud_combo.setStyleSheet(self.get_combo_style())
        arduino_layout.addWidget(self.baud_combo, 0, 1)
        
        self.enable_label = QLabel()
        self.enable_label.setStyleSheet("color: #6a8a9a; font-family: 'Calibri', 'Courier New', monospace; font-weight: bold;")
        arduino_layout.addWidget(self.enable_label, 1, 0)
        self.arduino_enable_check = QCheckBox()
        self.arduino_enable_check.setChecked(self.config['hardware']['arduino']['enabled'])
        self.arduino_enable_check.setStyleSheet("""
            QCheckBox { color: #7a9bb5; font-family: 'Calibri', 'Courier New', monospace; }
            QCheckBox::indicator { width: 18px; height: 18px; border: 1px solid rgba(80,130,180,0.3); border-radius: 4px; background: rgba(20,30,50,0.4); }
            QCheckBox::indicator:checked { background: #3a5a6a; border-color: #5a8aaa; }
        """)
        arduino_layout.addWidget(self.arduino_enable_check, 1, 1)
        
        self.arduino_group.setLayout(arduino_layout)
        content_layout.addWidget(self.arduino_group)
        
        # 缓存参数
        self.cache_group = QGroupBox()
        self.cache_group.setStyleSheet(self.get_group_style())
        cache_layout = QGridLayout()
        cache_layout.setSpacing(10)
        
        self.cache_age_label = QLabel()
        self.cache_age_label.setStyleSheet("color: #6a8a9a; font-family: 'Calibri', 'Courier New', monospace; font-weight: bold;")
        cache_layout.addWidget(self.cache_age_label, 0, 0)
        self.cache_age_spin = QSpinBox()
        self.cache_age_spin.setRange(1, 30)
        self.cache_age_spin.setValue(self.config['cache']['max_age_days'])
        self.cache_age_spin.setStyleSheet(self.get_spin_style())
        cache_layout.addWidget(self.cache_age_spin, 0, 1)
        self.cache_age_unit = QLabel()
        self.cache_age_unit.setStyleSheet("color: #6a8a9a; font-family: 'Calibri', 'Courier New', monospace;")
        cache_layout.addWidget(self.cache_age_unit, 0, 2)
        
        self.clear_cache_btn = QPushButton()
        self.clear_cache_btn.clicked.connect(self.clear_cache)
        self.clear_cache_btn.setStyleSheet("background: #3a2a2a; color: #aa7a7a; border: 1px solid #5a3a3a; border-radius: 8px; padding: 8px 20px; font-weight: bold; font-family: 'Calibri','Courier New',monospace; font-size: 13px;")
        cache_layout.addWidget(self.clear_cache_btn, 1, 0, 1, 2)
        
        self.cache_group.setLayout(cache_layout)
        content_layout.addWidget(self.cache_group)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        self.save_btn = QPushButton()
        self.save_btn.clicked.connect(self.save_settings)
        self.save_btn.setStyleSheet("background: #2a4a3a; color: #7aaa8a; border: 1px solid #3a5a4a; border-radius: 8px; padding: 12px 30px; font-weight: bold; font-family: 'Calibri','Courier New',monospace; font-size: 14px;")
        
        self.reset_btn = QPushButton()
        self.reset_btn.clicked.connect(self.reset_defaults)
        self.reset_btn.setStyleSheet("background: #3a3a2a; color: #aaaa7a; border: 1px solid #5a5a3a; border-radius: 8px; padding: 12px 30px; font-weight: bold; font-family: 'Calibri','Courier New',monospace; font-size: 14px;")
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addStretch()
        
        content_layout.addLayout(btn_layout)
        content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
        self.setLayout(layout)
        
        # 初始化文本
        self.update_language()
    
    def update_language(self):
        """更新语言 - 直接硬编码"""
        lang = get_language()
        
        if lang == 'zh':
            self.title_label.setText("⚙️ 设置")
            self.tracking_group.setTitle("📡 跟踪参数")
            self.tracking_interval_label.setText("跟踪间隔")
            self.tracking_interval_unit.setText("秒")
            self.tle_update_label.setText("TLE更新间隔")
            self.tle_update_unit.setText("分钟")
            self.position_read_label.setText("位置读取间隔")
            self.position_read_unit.setText("秒")
            self.gear_ratio_label.setText("方位角齿轮比")
            self.gear_ratio_unit.setText("倍")
            self.arduino_group.setTitle("🔌 Arduino参数")
            self.baud_label.setText("波特率")
            self.enable_label.setText("启用Arduino")
            self.cache_group.setTitle("💾 缓存参数")
            self.cache_age_label.setText("缓存有效期")
            self.cache_age_unit.setText("天")
            self.clear_cache_btn.setText("🗑️ 清空缓存")
            self.save_btn.setText("💾 保存设置")
            self.reset_btn.setText("↩️ 恢复默认")
        else:
            self.title_label.setText("⚙️ Settings")
            self.tracking_group.setTitle("📡 Tracking Settings")
            self.tracking_interval_label.setText("Tracking Interval")
            self.tracking_interval_unit.setText("s")
            self.tle_update_label.setText("TLE Update Interval")
            self.tle_update_unit.setText("min")
            self.position_read_label.setText("Position Read Interval")
            self.position_read_unit.setText("s")
            self.gear_ratio_label.setText("Azimuth Gear Ratio")
            self.gear_ratio_unit.setText("x")
            self.arduino_group.setTitle("🔌 Arduino Settings")
            self.baud_label.setText("Baud Rate")
            self.enable_label.setText("Enable Arduino")
            self.cache_group.setTitle("💾 Cache Settings")
            self.cache_age_label.setText("Cache Max Age")
            self.cache_age_unit.setText("days")
            self.clear_cache_btn.setText("🗑️ Clear Cache")
            self.save_btn.setText("💾 Save Settings")
            self.reset_btn.setText("↩️ Reset Defaults")
    
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
    
    def get_spin_style(self):
        return """
            QSpinBox, QDoubleSpinBox {
                background: rgba(20, 30, 50, 0.6);
                color: #8aacb5;
                border: 1px solid rgba(80, 130, 180, 0.15);
                border-radius: 5px;
                padding: 5px 8px;
                font-family: 'Calibri', 'Courier New', monospace;
                font-weight: bold;
                font-size: 13px;
                min-width: 80px;
            }
            QSpinBox::up-button, QDoubleSpinBox::up-button,
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                background: #2a3a4a;
                border: none;
                border-radius: 3px;
                padding: 2px;
            }
        """
    
    def get_combo_style(self):
        return """
            QComboBox {
                background: rgba(20, 30, 50, 0.6);
                color: #8aacb5;
                border: 1px solid rgba(80, 130, 180, 0.15);
                border-radius: 5px;
                padding: 5px 8px;
                font-family: 'Calibri', 'Courier New', monospace;
                font-weight: bold;
                font-size: 13px;
                min-width: 100px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background: #1a2a3a;
                color: #8aacb5;
                border: 1px solid #3a5a6a;
                selection-background-color: #2a3a4a;
            }
        """
    
    def save_settings(self):
        try:
            self.config['tracking']['tracking_interval'] = self.tracking_interval_spin.value()
            self.config['tracking']['tle_update_minutes'] = self.tle_update_spin.value()
            self.config['tracking']['position_read_interval'] = self.position_read_spin.value()
            self.config['tracking']['gear_ratio_azimuth'] = self.gear_ratio_spin.value()
            self.config['hardware']['arduino']['baud_rate'] = int(self.baud_combo.currentText())
            self.config['hardware']['arduino']['enabled'] = self.arduino_enable_check.isChecked()
            self.config['cache']['max_age_days'] = self.cache_age_spin.value()
            
            import yaml
            with open('config/config.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            
            from .languages import tr
            QMessageBox.information(self, tr('success'), "✅ " + tr('settings_saved'))
            self.settings_changed.emit()
        except Exception as e:
            from .languages import tr
            QMessageBox.warning(self, tr('error'), f"❌ {tr('save_failed')}: {str(e)}")
    
    def reset_defaults(self):
        from .languages import tr
        reply = QMessageBox.question(self, tr('warning'), "⚠️ " + tr('reset_confirm'), QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            default_config = {'tracking': {'tracking_interval': 2.5, 'tle_update_minutes': 10, 'position_read_interval': 2.5, 'gear_ratio_azimuth': 3.0}, 'hardware': {'arduino': {'enabled': False, 'baud_rate': 115200}}, 'cache': {'max_age_days': 7}}
            self.tracking_interval_spin.setValue(2.5)
            self.tle_update_spin.setValue(10)
            self.position_read_spin.setValue(2.5)
            self.gear_ratio_spin.setValue(3.0)
            self.baud_combo.setCurrentText("115200")
            self.arduino_enable_check.setChecked(False)
            self.cache_age_spin.setValue(7)
            QMessageBox.information(self, tr('success'), "✅ " + tr('reset_done'))
    
    def clear_cache(self):
        from .languages import tr
        reply = QMessageBox.question(self, tr('warning'), "⚠️ " + tr('clear_cache_confirm'), QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            import os, shutil
            cache_dir = self.config['cache']['directory']
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                os.makedirs(cache_dir)
                QMessageBox.information(self, tr('success'), "✅ " + tr('cache_cleared'))
            else:
                QMessageBox.information(self, tr('info'), "ℹ️ " + tr('cache_empty'))
