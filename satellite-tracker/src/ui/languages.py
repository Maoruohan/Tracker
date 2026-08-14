"""
多语言支持 - 中英双语（完整版）
"""

LANGUAGES = {
    'zh': {
        # 通用
        'app_title': '🛰️ 卫星跟踪系统',
        'system_ready': '🟢 系统就绪',
        'searching': '⏳ 搜索中...',
        'search_failed': '❌ 搜索失败',
        'network_error': '❌ 网络连接失败',
        'success': '✅ 成功',
        'error': '❌ 错误',
        'warning': '⚠️ 警告',
        'loading': '⏳ 加载中...',
        'initializing': '等待启动...',
        
        # 标签页
        'tab_tracking': '📡 跟踪',
        'tab_location': '📍 位置',
        
        # 跟踪页面
        'satellite_selection': '📡 卫星选择',
        'target': '目标:',
        'satellite': '卫星:',
        'start_tracking': '▶ 开始跟踪',
        'stop_tracking': '⏹ 停止',
        'tracking': '跟踪中',
        'stopped': '已停止',
        'idle': '空闲',
        'fetching_tle': '⏳ 获取轨道数据中...',
        'tle_loaded': '📡 TLE: 已加载',
        'tle_ready': '📡 TLE: 就绪',
        'tle_failed': '❌ 获取失败',
        
        # 数据显示
        'telemetry': '📊 遥测数据',
        'satellite_name': '🛰️ 卫星:',
        'azimuth': '🎯 方位角:',
        'elevation': '📐 仰角:',
        'range': '📏 距离:',
        'status': '📊 状态:',
        'elapsed': '⏱️ 用时:',
        'degrees': '°',
        'kilometers': 'km',
        
        # 天球图
        'sky_map': '🗺️ 天球图',
        'north': 'N',
        'south': 'S',
        'east': 'E',
        'west': 'W',
        'zenith': '+',
        'satellite_symbol': '●',
        
        # 位置页面
        'search_location': '🔍 搜索位置',
        'search_placeholder': '输入城市、乡镇、街道名称...',
        'search_btn': '🔍 搜索',
        'hot_cities': '🌍 热门城市:',
        'manual_input': '✏️ 手动输入坐标',
        'current_location': '📍 当前位置',
        'use_location': '✅ 使用此位置',
        'waiting_search': '等待搜索...',
        'search_results': '✅ 找到 {count} 个结果，请点击选择',
        'no_results': '❌ 未找到结果，请尝试其他关键词',
        'preset': '📌 预设:',
        'latitude': '纬度:',
        'longitude': '经度:',
        'apply_coords': '✅ 应用坐标',
        'location_updated': '📍 位置已更新！',
        'coords_invalid': '❌ 坐标超出有效范围！\n纬度: -90 到 90\n经度: -180 到 180',
        'coords_invalid_num': '❌ 请输入有效的数字！',
        'lat_placeholder': '纬度 (如: 22.817)',
        'lon_placeholder': '经度 (如: 108.367)',
        
        # 状态栏
        'system_status': '📊 系统状态',
        'arduino_offline': '🔌 Arduino: 离线',
        'arduino_connected': '🔌 Arduino: 已连接',
        'arduino_failed': '🔌 Arduino: 连接失败',
        'arduino_disabled': '🔌 Arduino: 已禁用',
        'tle_ready_status': '📡 TLE: 就绪',
        'tle_loaded_status': '📡 TLE: 已加载',
        
        # 错误消息
        'sat_not_found': '❌ 找不到卫星 "{sat}"！',
        'tle_fetch_failed': '❌ 获取 {sat} 轨道数据失败',
        'location_updated_msg': '📍 {name}\n纬度: {lat:.6f}\n经度: {lon:.6f}',
        'custom_location': '📍 自定义坐标 ({lat:.4f}, {lon:.4f})',
        
        # 搜索状态
        'searching_status': '⏳ 搜索中...',
        'search_please_wait': '⏳ 正在搜索，请稍候...',
        'search_network_error': '无法连接到地图服务，请检查网络连接',
        'search_error': '搜索时发生错误: {error}',
        'selected': '✅ 已选择: {name}',
        'location_applied': '✅ 位置已应用！',
        'preset_filled': '已填入 {name} 的坐标\n纬度: {lat}\n经度: {lon}\n\n点击「应用坐标」生效',
        'preset_title': '预设',
        
        # 坐标格式
        'lat_lon_format': '📍 {name} (纬度: {lat:.6f}, 经度: {lon:.6f})',
        'coords_format': '📍 {name} ({lat:.4f}, {lon:.4f})',
        
        # 时间
        'hours': '{:02d}:{:02d}:{:02d}',
        
        # 预设城市
        'preset_nanning': '南宁',
        'preset_beijing': '北京',
        'preset_shanghai': '上海',
        'preset_guangzhou': '广州',
        'preset_shenzhen': '深圳',
        'preset_chengdu': '成都',
        'preset_hangzhou': '杭州',
        'preset_wuhan': '武汉',
        
        # 设置页面
        'settings': '设置',
        'tracking_settings': '跟踪参数',
        'tracking_interval': '跟踪间隔',
        'tle_update': 'TLE更新间隔',
        'position_read': '位置读取间隔',
        'gear_ratio': '方位角齿轮比',
        'seconds': '秒',
        'minutes': '分钟',
        'ratio': '倍',
        'arduino_settings': 'Arduino参数',
        'baud_rate': '波特率',
        'enable_arduino': '启用Arduino',
        'cache_settings': '缓存参数',
        'cache_max_age': '缓存有效期',
        'days': '天',
        'clear_cache': '清空缓存',
        'save_settings': '保存设置',
        'reset_defaults': '恢复默认',
        'settings_saved': '设置已保存！',
        'save_failed': '保存失败',
        'reset_confirm': '确定要恢复所有默认设置吗？',
        'reset_done': '已恢复默认设置！',
        'clear_cache_confirm': '确定要清空所有TLE缓存吗？',
        'cache_cleared': '缓存已清空！',
        'cache_empty': '缓存文件夹为空。',
        'info': '信息',
    },
    'en': {
        # General
        'app_title': '🛰️ Satellite Tracking System',
        'system_ready': '🟢 System Ready',
        'searching': '⏳ Searching...',
        'search_failed': '❌ Search Failed',
        'network_error': '❌ Network Connection Failed',
        'success': '✅ Success',
        'error': '❌ Error',
        'warning': '⚠️ Warning',
        'loading': '⏳ Loading...',
        'initializing': 'Waiting to start...',
        
        # Tabs
        'tab_tracking': '📡 Tracking',
        'tab_location': '📍 Location',
        
        # Tracking page
        'satellite_selection': '📡 Satellite Selection',
        'target': 'Target:',
        'satellite': 'Satellite:',
        'start_tracking': '▶ Start Tracking',
        'stop_tracking': '⏹ Stop',
        'tracking': 'Tracking',
        'stopped': 'Stopped',
        'idle': 'Idle',
        'fetching_tle': '⏳ Fetching TLE data...',
        'tle_loaded': '📡 TLE: Loaded',
        'tle_ready': '📡 TLE: Ready',
        'tle_failed': '❌ Fetch Failed',
        
        # Data display
        'telemetry': '📊 Telemetry Data',
        'satellite_name': '🛰️ Satellite:',
        'azimuth': '🎯 Azimuth:',
        'elevation': '📐 Elevation:',
        'range': '📏 Range:',
        'status': '📊 Status:',
        'elapsed': '⏱️ Elapsed:',
        'degrees': '°',
        'kilometers': 'km',
        
        # Sky map
        'sky_map': '🗺️ Sky Map',
        'north': 'N',
        'south': 'S',
        'east': 'E',
        'west': 'W',
        'zenith': '+',
        'satellite_symbol': '●',
        
        # Location page
        'search_location': '🔍 Search Location',
        'search_placeholder': 'Enter city, town, or street name...',
        'search_btn': '🔍 Search',
        'hot_cities': '🌍 Hot Cities:',
        'manual_input': '✏️ Manual Coordinate Input',
        'current_location': '📍 Current Location',
        'use_location': '✅ Use This Location',
        'waiting_search': 'Waiting for search...',
        'search_results': '✅ Found {count} results, click to select',
        'no_results': '❌ No results found, try different keywords',
        'preset': '📌 Presets:',
        'latitude': 'Latitude:',
        'longitude': 'Longitude:',
        'apply_coords': '✅ Apply Coordinates',
        'location_updated': '📍 Location Updated!',
        'coords_invalid': '❌ Coordinates out of valid range!\nLatitude: -90 to 90\nLongitude: -180 to 180',
        'coords_invalid_num': '❌ Please enter valid numbers!',
        'lat_placeholder': 'Latitude (e.g., 22.817)',
        'lon_placeholder': 'Longitude (e.g., 108.367)',
        
        # Status bar
        'system_status': '📊 System Status',
        'arduino_offline': '🔌 Arduino: Offline',
        'arduino_connected': '🔌 Arduino: Connected',
        'arduino_failed': '🔌 Arduino: Failed',
        'arduino_disabled': '🔌 Arduino: Disabled',
        'tle_ready_status': '📡 TLE: Ready',
        'tle_loaded_status': '📡 TLE: Loaded',
        
        # Error messages
        'sat_not_found': '❌ Satellite "{sat}" not found!',
        'tle_fetch_failed': '❌ Failed to fetch TLE for {sat}',
        'location_updated_msg': '📍 {name}\nLatitude: {lat:.6f}\nLongitude: {lon:.6f}',
        'custom_location': '📍 Custom Coordinates ({lat:.4f}, {lon:.4f})',
        
        # Search status
        'searching_status': '⏳ Searching...',
        'search_please_wait': '⏳ Searching, please wait...',
        'search_network_error': 'Cannot connect to map service, please check network',
        'search_error': 'Search error: {error}',
        'selected': '✅ Selected: {name}',
        'location_applied': '✅ Location Applied!',
        'preset_filled': 'Filled {name} coordinates\nLatitude: {lat}\nLongitude: {lon}\n\nClick "Apply Coordinates" to use',
        'preset_title': 'Preset',
        
        # Location format
        'lat_lon_format': '📍 {name} (Lat: {lat:.6f}, Lon: {lon:.6f})',
        'coords_format': '📍 {name} ({lat:.4f}, {lon:.4f})',
        
        # Time
        'hours': '{:02d}:{:02d}:{:02d}',
        
        # Preset cities (English names)
        'preset_nanning': 'Nanning',
        'preset_beijing': 'Beijing',
        'preset_shanghai': 'Shanghai',
        'preset_guangzhou': 'Guangzhou',
        'preset_shenzhen': 'Shenzhen',
        'preset_chengdu': 'Chengdu',
        'preset_hangzhou': 'Hangzhou',
        'preset_wuhan': 'Wuhan',
        
        # Settings page
        'settings': 'Settings',
        'tracking_settings': 'Tracking Settings',
        'tracking_interval': 'Tracking Interval',
        'tle_update': 'TLE Update Interval',
        'position_read': 'Position Read Interval',
        'gear_ratio': 'Azimuth Gear Ratio',
        'seconds': 's',
        'minutes': 'min',
        'ratio': 'x',
        'arduino_settings': 'Arduino Settings',
        'baud_rate': 'Baud Rate',
        'enable_arduino': 'Enable Arduino',
        'cache_settings': 'Cache Settings',
        'cache_max_age': 'Cache Max Age',
        'days': 'days',
        'clear_cache': 'Clear Cache',
        'save_settings': 'Save Settings',
        'reset_defaults': 'Reset Defaults',
        'settings_saved': 'Settings saved!',
        'save_failed': 'Save failed',
        'reset_confirm': 'Reset all settings to default?',
        'reset_done': 'Defaults restored!',
        'clear_cache_confirm': 'Clear all TLE cache?',
        'cache_cleared': 'Cache cleared!',
        'cache_empty': 'Cache folder is empty.',
        'info': 'Info',
    }
}

class Translator:
    """翻译器 - 管理当前语言"""
    
    _instance = None
    _current_lang = 'zh'
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._lang = 'zh'
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def set_language(self, lang):
        if lang in LANGUAGES:
            self._lang = lang
            return True
        return False
    
    def get_language(self):
        return self._lang
    
    def tr(self, key, **kwargs):
        lang_dict = LANGUAGES.get(self._lang, LANGUAGES['zh'])
        text = lang_dict.get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except:
                return text
        return text
    
    def get_all_texts(self):
        return LANGUAGES.get(self._lang, LANGUAGES['zh'])

_translator = Translator.get_instance()

def tr(key, **kwargs):
    return _translator.tr(key, **kwargs)

def set_language(lang):
    return _translator.set_language(lang)

def get_language():
    return _translator.get_language()
