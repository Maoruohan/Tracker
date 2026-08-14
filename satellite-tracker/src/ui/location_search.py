from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import urllib.request, json, time
from .languages import tr, get_language

class LocationSearchWidget(QWidget):
    location_selected = pyqtSignal(float, float, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.last_search_time = 0
        self.current_results = []
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.title_label = QLabel(tr('search_location'))
        self.title_label.setStyleSheet("font-size:16px;font-weight:bold;color:#7a9bb5;font-family:'Calibri','Courier New',monospace;padding:5px;")
        layout.addWidget(self.title_label)
        
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(tr('search_placeholder'))
        self.search_input.setStyleSheet("background:rgba(20,30,50,0.6);color:#8aacb5;border:1px solid rgba(80,130,180,0.15);border-radius:8px;padding:10px 15px;font-size:14px;font-family:'Calibri','Courier New',monospace;font-weight:bold;")
        self.search_input.returnPressed.connect(self.search_location)
        
        self.search_btn = QPushButton(tr('search_btn'))
        self.search_btn.clicked.connect(self.search_location)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background: #2a3a4a;
                color: #8aacb5;
                border: 1px solid #3a5a6a;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-family: 'Calibri', 'Courier New', monospace;
                font-size: 13px;
            }
            QPushButton:hover { background: #3a4a5a; }
        """)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        layout.addLayout(search_layout)
        
        quick_layout = QHBoxLayout()
        self.hot_cities_label = QLabel(tr('hot_cities'))
        self.hot_cities_label.setStyleSheet("color:#6a8a9a;font-family:'Calibri','Courier New',monospace;font-weight:bold;")
        quick_layout.addWidget(self.hot_cities_label)
        cities = [('preset_beijing','北京'),('preset_shanghai','上海'),('preset_guangzhou','广州'),('preset_shenzhen','深圳'),('preset_nanning','南宁'),('preset_chengdu','成都'),('preset_hangzhou','杭州'),('preset_wuhan','武汉')]
        self.city_buttons = []
        for key, cn in cities:
            btn = QPushButton(cn)
            btn.setStyleSheet("background:rgba(30,40,55,0.6);color:#7a9bb5;border:1px solid rgba(80,130,180,0.15);border-radius:5px;padding:5px 12px;font-family:'Calibri','Courier New',monospace;font-weight:bold;font-size:12px;")
            btn.setProperty('tr_key', key)
            btn.clicked.connect(lambda checked, c=cn: self.search_input.setText(c))
            quick_layout.addWidget(btn)
            self.city_buttons.append(btn)
        quick_layout.addStretch()
        layout.addLayout(quick_layout)
        
        self.result_list = QListWidget()
        self.result_list.setStyleSheet("background:rgba(15,25,40,0.6);color:#7a9bb5;border:1px solid rgba(80,130,180,0.15);border-radius:8px;font-family:'Calibri','Courier New',monospace;font-weight:bold;font-size:13px;")
        self.result_list.itemClicked.connect(self.select_result)
        self.result_list.setMaximumHeight(180)
        self.result_list.hide()
        layout.addWidget(self.result_list)
        
        self.info_group = QGroupBox(tr('current_location'))
        self.info_group.setStyleSheet("color:#7a9bb5;border:1px solid rgba(80,130,180,0.15);border-radius:8px;margin-top:10px;font-family:'Calibri','Courier New',monospace;font-weight:bold;background:rgba(15,25,40,0.3);")
        info_layout = QHBoxLayout()
        self.coord_label = QLabel(tr('waiting_search'))
        self.coord_label.setStyleSheet("color:#7a9bb5;font-family:'Calibri','Courier New',monospace;font-weight:bold;font-size:14px;")
        info_layout.addWidget(self.coord_label)
        info_layout.addStretch()
        
        self.use_btn = QPushButton(tr('use_location'))
        self.use_btn.clicked.connect(self.use_location)
        self.use_btn.setStyleSheet("""
            QPushButton {
                background: #2a3a4a;
                color: #8aacb5;
                border: 1px solid #3a5a6a;
                border-radius: 8px;
                padding: 8px 20px;
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
        """)
        self.use_btn.setEnabled(False)
        info_layout.addWidget(self.use_btn)
        self.info_group.setLayout(info_layout)
        layout.addWidget(self.info_group)
        self.setLayout(layout)
        self.selected_lat = self.selected_lon = self.selected_name = None
    
    def update_language(self):
        self.title_label.setText(tr('search_location'))
        self.search_input.setPlaceholderText(tr('search_placeholder'))
        self.search_btn.setText(tr('search_btn'))
        self.hot_cities_label.setText(tr('hot_cities'))
        self.info_group.setTitle(tr('current_location'))
        self.coord_label.setText(tr('waiting_search'))
        self.use_btn.setText(tr('use_location'))
        for btn in self.city_buttons:
            key = btn.property('tr_key')
            if key: btn.setText(tr(key))
    
    def search_location(self):
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, tr('warning'), "请输入城市或地址名称")
            return
        now = time.time()
        if now - self.last_search_time < 1:
            QMessageBox.warning(self, tr('warning'), "请稍等1秒后再搜索")
            return
        self.last_search_time = now
        self.coord_label.setText(tr('searching_status'))
        self.result_list.clear()
        self.result_list.show()
        self.result_list.addItem(tr('search_please_wait'))
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={urllib.parse.quote(query)}&limit=10&addressdetails=1&accept-language=zh"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'SatelliteTracker/1.0'})
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            self.result_list.clear()
            self.current_results = []
            if not data:
                self.result_list.addItem(tr('no_results'))
                self.coord_label.setText("❌ " + tr('no_results'))
                return
            for item in data:
                display_name = item.get('display_name','')
                lat = item.get('lat','0')
                lon = item.get('lon','0')
                name_parts = display_name.split(',')
                short_name = ','.join(name_parts[:4]) if len(name_parts)>4 else display_name
                if len(short_name)>60: short_name = short_name[:57]+'...'
                display_text = f"{short_name}  ({float(lat):.4f}, {float(lon):.4f})"
                self.result_list.addItem(display_text)
                item_widget = self.result_list.item(self.result_list.count()-1)
                item_widget.setData(Qt.UserRole, (float(lat), float(lon), display_name))
                self.current_results.append((float(lat), float(lon), display_name))
            self.coord_label.setText(tr('search_results', count=len(data)))
        except Exception as e:
            self.result_list.clear()
            self.result_list.addItem("❌ " + tr('search_failed'))
            self.coord_label.setText("❌ " + tr('search_failed'))
    
    def select_result(self, item):
        data = item.data(Qt.UserRole)
        if data:
            lat, lon, name = data
            self.selected_lat, self.selected_lon, self.selected_name = lat, lon, name
            short_name = ','.join(name.split(',')[:3]) if len(name.split(','))>3 else name
            self.coord_label.setText(tr('lat_lon_format', name=short_name, lat=lat, lon=lon))
            self.use_btn.setEnabled(True)
            self.result_list.hide()
    
    def use_location(self):
        if self.selected_lat is not None:
            self.location_selected.emit(self.selected_lat, self.selected_lon, self.selected_name)
            self.use_btn.setEnabled(False)
            self.coord_label.setText(f"✅ {tr('location_applied')}")

class CoordinatesInputWidget(QWidget):
    coordinate_entered = pyqtSignal(float, float)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QGridLayout()
        preset_layout = QHBoxLayout()
        self.preset_label = QLabel(tr('preset'))
        self.preset_label.setStyleSheet("color:#a8d8ea;font-family:'Calibri','Courier New',monospace;font-weight:bold;")
        preset_layout.addWidget(self.preset_label)
        presets = [('preset_nanning',22.817,108.367),('preset_beijing',39.9042,116.4074),('preset_shanghai',31.2304,121.4737),('preset_guangzhou',23.1291,113.2644),('preset_shenzhen',22.5431,114.0579)]
        self.preset_buttons = []
        for key, lat, lon in presets:
            btn = QPushButton(tr(key))
            btn.setStyleSheet("background:rgba(30,40,55,0.6);color:#7a9bb5;border:1px solid rgba(80,130,180,0.15);border-radius:5px;padding:4px 10px;font-family:'Calibri','Courier New',monospace;font-weight:bold;font-size:11px;")
            btn.setProperty('tr_key', key)
            btn.clicked.connect(lambda checked, l=lat, n=lon, key=key: self.set_preset(l, n, key))
            preset_layout.addWidget(btn)
            self.preset_buttons.append(btn)
        preset_layout.addStretch()
        layout.addLayout(preset_layout, 0, 0, 1, 2)
        
        self.lat_label = QLabel(tr('latitude'))
        self.lat_label.setStyleSheet("color:#6a8a9a;font-family:'Calibri','Courier New',monospace;font-weight:bold;")
        self.lat_input = QLineEdit()
        self.lat_input.setPlaceholderText(tr('lat_placeholder'))
        self.lat_input.setStyleSheet("background:rgba(20,30,50,0.6);color:#8aacb5;border:1px solid rgba(80,130,180,0.15);border-radius:8px;padding:8px 12px;font-family:'Calibri','Courier New',monospace;font-weight:bold;")
        
        self.lon_label = QLabel(tr('longitude'))
        self.lon_label.setStyleSheet("color:#6a8a9a;font-family:'Calibri','Courier New',monospace;font-weight:bold;")
        self.lon_input = QLineEdit()
        self.lon_input.setPlaceholderText(tr('lon_placeholder'))
        self.lon_input.setStyleSheet("background:rgba(20,30,50,0.6);color:#8aacb5;border:1px solid rgba(80,130,180,0.15);border-radius:8px;padding:8px 12px;font-family:'Calibri','Courier New',monospace;font-weight:bold;")
        
        self.apply_btn = QPushButton(tr('apply_coords'))
        self.apply_btn.clicked.connect(self.apply_coordinates)
        self.apply_btn.setStyleSheet("""
            QPushButton {
                background: #2a3a4a;
                color: #8aacb5;
                border: 1px solid #3a5a6a;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                font-family: 'Calibri', 'Courier New', monospace;
                font-size: 13px;
            }
            QPushButton:hover { background: #3a4a5a; }
        """)
        
        layout.addWidget(self.lat_label, 1, 0)
        layout.addWidget(self.lat_input, 1, 1)
        layout.addWidget(self.lon_label, 2, 0)
        layout.addWidget(self.lon_input, 2, 1)
        layout.addWidget(self.apply_btn, 3, 0, 1, 2)
        self.setLayout(layout)
    
    def update_language(self):
        self.preset_label.setText(tr('preset'))
        for btn in self.preset_buttons:
            key = btn.property('tr_key')
            if key: btn.setText(tr(key))
        self.lat_label.setText(tr('latitude'))
        self.lat_input.setPlaceholderText(tr('lat_placeholder'))
        self.lon_label.setText(tr('longitude'))
        self.lon_input.setPlaceholderText(tr('lon_placeholder'))
        self.apply_btn.setText(tr('apply_coords'))
    
    def set_preset(self, lat, lon, key):
        """设置预设坐标"""
        self.lat_input.setText(str(lat))
        self.lon_input.setText(str(lon))
        
        # 获取翻译后的城市名
        city_name = tr(key)
        
        # 硬编码弹窗内容
        lang = get_language()
        if lang == 'zh':
            msg = f"已填入 {city_name} 的坐标\n纬度: {lat}\n经度: {lon}\n\n点击「应用坐标」生效"
        else:
            msg = f"Filled {city_name} coordinates\nLatitude: {lat}\nLongitude: {lon}\n\nClick \"Apply Coordinates\" to use"
        
        QMessageBox.information(self, tr('preset_title'), msg)
    
    def apply_coordinates(self):
        try:
            lat, lon = float(self.lat_input.text()), float(self.lon_input.text())
            if -90<=lat<=90 and -180<=lon<=180:
                self.coordinate_entered.emit(lat, lon)
            else:
                QMessageBox.warning(self, tr('error'), tr('coords_invalid'))
        except:
            QMessageBox.warning(self, tr('error'), tr('coords_invalid_num'))
