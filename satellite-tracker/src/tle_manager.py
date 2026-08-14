import os
import time
import requests
from datetime import datetime
from typing import Optional, Tuple

class TLEManager:
    def __init__(self, cache_dir="tle_cache", max_age_days=7):
        self.cache_dir = cache_dir
        self.max_age_days = max_age_days
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _get_cache_path(self, norad_id):
        return os.path.join(self.cache_dir, f"{norad_id}.txt")
    
    def _is_cache_valid(self, norad_id):
        path = self._get_cache_path(norad_id)
        if not os.path.exists(path):
            return False
        mtime = datetime.fromtimestamp(os.path.getmtime(path))
        age = datetime.now() - mtime
        return age.days < self.max_age_days
    
    def _tle_matches_norad(self, tle1, norad_id):
        try:
            return int(tle1[2:7].strip()) == int(norad_id)
        except:
            return False
    
    def _save_cache(self, norad_id, name, tle1, tle2):
        path = self._get_cache_path(norad_id)
        with open(path, "w", encoding="utf-8") as f:
            f.write(name.strip() + "\n")
            f.write(tle1.strip() + "\n")
            f.write(tle2.strip() + "\n")
    
    def _load_cache(self, norad_id):
        path = self._get_cache_path(norad_id)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        if len(lines) >= 3:
            return lines[0], lines[1], lines[2]
        return None
    
    def _fetch_from_celestrak(self, norad_id, sat_name):
        url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=TLE"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                lines = [line.strip() for line in response.text.splitlines() if line.strip()]
                if len(lines) >= 3:
                    name_line = lines[0]
                    tle1 = lines[1]
                    tle2 = lines[2]
                    if tle1.startswith("1 ") and tle2.startswith("2 "):
                        if self._tle_matches_norad(tle1, norad_id):
                            return name_line, tle1, tle2
        except:
            pass
        return None
    
    def fetch_tle(self, norad_id, sat_name, force_refresh=False):
        if not force_refresh and self._is_cache_valid(norad_id):
            cached = self._load_cache(norad_id)
            if cached:
                return cached
        result = self._fetch_from_celestrak(norad_id, sat_name)
        if result:
            name, tle1, tle2 = result
            self._save_cache(norad_id, name, tle1, tle2)
            return result
        cached = self._load_cache(norad_id)
        if cached:
            return cached
        return None
