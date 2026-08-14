
"""
Map Widget for location selection using OpenStreetMap
"""

import sys
import json
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Map Location Picker</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body {{ margin: 0; padding: 0; background: #0a0a1a; }}
        #map {{ height: 600px; width: 100%; }}
        .leaflet-control-zoom {{ border: 1px solid #00d4ff !important; }}
        .leaflet-control-zoom a {{ background: rgba(10, 10, 30, 0.9) !important; color: #00d4ff !important; }}
        .leaflet-control-zoom a:hover {{ background: rgba(0, 212, 255, 0.3) !important; }}
        .leaflet-popup-content-wrapper {{ background: rgba(10, 10, 30, 0.95) !important; color: #00d4ff !important; border: 1px solid #00d4ff; }}
        .leaflet-popup-tip {{ background: rgba(10, 10, 30, 0.95) !important; }}
        .search-box {{
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background: rgba(10, 10, 30, 0.95);
            border: 1px solid #00d4ff;
            border-radius: 8px;
            padding: 10px 15px;
            width: 400px;
            max-width: 80%;
        }}
        .search-box input {{
            background: transparent;
            border: none;
            color: #00d4ff;
            font-size: 14px;
            width: 100%;
            outline: none;
            font-family: 'Courier New', monospace;
        }}
        .search-box input::placeholder {{
            color: #4a6a8a;
        }}
        .use-btn {{
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background: #00d4ff;
            color: #0a0a1a;
            border: none;
            border-radius: 8px;
            padding: 12px 30px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            font-family: 'Courier New', monospace;
        }}
        .use-btn:hover {{
            opacity: 0.9;
        }}
    </style>
</head>
<body>
    <div class="search-box">
        <input type="text" id="searchInput" placeholder="🔍 Search city or address..." />
    </div>
    <div id="map"></div>
    <button class="use-btn" onclick="confirmLocation()">✅ Use This Location</button>
    
    <script>
        var map = L.map('map').setView([{lat}, {lon}], 10);
        
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap',
            maxZoom: 19
        }}).addTo(map);
        
        var marker = L.marker([{lat}, {lon}], {{draggable: true}}).addTo(map);
        var popup = L.popup();
        
        function updateLocation(lat, lon) {{
            marker.setLatLng([lat, lon]);
            map.setView([lat, lon], 15);
            getLocationName(lat, lon);
        }}
        
        function getLocationName(lat, lon) {{
            fetch('https://nominatim.openstreetmap.org/reverse?format=json&lat=' + lat + '&lon=' + lon + '&zoom=18&addressdetails=1')
                .then(response => response.json())
                .then(data => {{
                    var name = data.display_name || lat + ', ' + lon;
                    popup.setContent('📍 <b>' + name + '</b><br>Lat: ' + lat.toFixed(6) + '<br>Lon: ' + lon.toFixed(6));
                    popup.openOn(map);
                    window.locationData = {{lat: lat, lon: lon, name: name}};
                }})
                .catch(() => {{
                    popup.setContent('📍 Lat: ' + lat.toFixed(6) + ', Lon: ' + lon.toFixed(6));
                    popup.openOn(map);
                    window.locationData = {{lat: lat, lon: lon, name: lat.toFixed(6) + ', ' + lon.toFixed(6)}};
                }});
        }}
        
        marker.on('dragend', function() {{
            var pos = marker.getLatLng();
            updateLocation(pos.lat, pos.lng);
        }});
        
        map.on('click', function(e) {{
            updateLocation(e.latlng.lat, e.latlng.lng);
        }});
        
        function confirmLocation() {{
            if (window.locationData) {{
                var data = window.locationData;
                window.pywebview._confirm(data.lat, data.lon, data.name);
            }}
        }}
        
        function searchLocation(query) {{
            if (!query) return;
            fetch('https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(query) + '&limit=1')
                .then(response => response.json())
                .then(data => {{
                    if (data.length > 0) {{
                        var lat = parseFloat(data[0].lat);
                        var lon = parseFloat(data[0].lon);
                        updateLocation(lat, lon);
                    }}
                }})
                .catch(() => {{}});
        }}
        
        document.getElementById('searchInput').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                searchLocation(this.value);
            }}
        }});
        
        getLocationName({lat}, {lon});
    </script>
</body>
</html>
"""

class MapWidget(QWidget):
    def __init__(self, config, location_callback):
        super().__init__()
        self.config = config
        self.location_callback = location_callback
        self.current_lat = float(config['observer']['latitude'])
        self.current_lon = float(config['observer']['longitude'])
        self.current_name = "Custom Location"
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        info_group = QGroupBox("📍 Current Location")
        info_layout = QHBoxLayout()
        
        lat = self.config['observer']['latitude']
        lon = self.config['observer']['longitude']
        self.coord_label = QLabel(f"Lat: {lat}, Lon: {lon}")
        self.coord_label.setStyleSheet("color: #00d4ff; font-weight: bold; font-family: 'Courier New', monospace; font-size: 14px;")
        
        info_layout.addWidget(self.coord_label)
        info_layout.addStretch()
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        self.web_view = QWebEngineView()
        self.web_view.setMinimumHeight(550)
        
        html = HTML_TEMPLATE.format(lat=lat, lon=lon)
        self.web_view.setHtml(html)
        
        self.web_view.page().runJavaScript("""
            window.pywebview = {
                _confirm: function(lat, lon, name) {
                    var event = new CustomEvent('locationConfirmed', {
                        detail: {lat: lat, lon: lon, name: name}
                    });
                    document.dispatchEvent(event);
                }
            };
        """)
        
        self.web_view.page().runJavaScript("""
            document.addEventListener('locationConfirmed', function(e) {
                window._pendingLocation = e.detail;
            });
        """)
        
        layout.addWidget(self.web_view)
        self.setLayout(layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_location)
        self.timer.start(500)
    
    def check_location(self):
        js = """
        (function() {
            if (window._pendingLocation) {
                var data = window._pendingLocation;
                window._pendingLocation = null;
                return JSON.stringify(data);
            }
            return null;
        })();
        """
        self.web_view.page().runJavaScript(js, self.handle_location_result)
    
    def handle_location_result(self, result):
        if result:
            try:
                data = json.loads(result)
                lat = data.get('lat')
                lon = data.get('lon')
                name = data.get('name', f"{lat:.6f}, {lon:.6f}")
                
                if lat and lon:
                    self.current_lat = float(lat)
                    self.current_lon = float(lon)
                    self.current_name = name
                    
                    self.coord_label.setText(f"📍 {name} (Lat: {lat:.6f}, Lon: {lon:.6f})")
                    self.config['observer']['latitude'] = str(lat)
                    self.config['observer']['longitude'] = str(lon)
                    
                    if self.location_callback:
                        self.location_callback(str(lat), str(lon), name)
                    
                    QMessageBox.information(self, "Success", f"✅ Location updated to:\n{name}")
            except:
                pass
    
    def update_location(self, lat, lon, name):
        self.current_lat = lat
        self.current_lon = lon
        self.current_name = name
        self.coord_label.setText(f"📍 {name} (Lat: {lat:.6f}, Lon: {lon:.6f})")
        js = f'updateLocation({lat}, {lon})'
        self.web_view.page().runJavaScript(js)
    
    def search_location(self, query):
        if query:
            js = f'searchLocation("{query}")'
            self.web_view.page().runJavaScript(js)
