import ephem
import math
from datetime import datetime, UTC
from typing import Tuple

class SatelliteTracker:
    def __init__(self, lat: str, lon: str, alt: float):
        self.observer = ephem.Observer()
        self.observer.lat = lat
        self.observer.lon = lon
        self.observer.elevation = alt
        self.observer.pressure = 0
        self.current_tle = None
        self.current_name = None
    
    def set_tle(self, name: str, tle1: str, tle2: str):
        self.current_name = name
        self.current_tle = (tle1, tle2)
    
    def compute_position(self) -> Tuple[float, float, float, float]:
        if self.current_tle is None:
            return 0.0, 0.0, 0.0, 0.0
        self.observer.date = ephem.Date(datetime.now(UTC))
        sat = ephem.readtle(self.current_name, self.current_tle[0], self.current_tle[1])
        sat.compute(self.observer)
        az = math.degrees(float(sat.az))
        raw_el = math.degrees(float(sat.alt))
        rng_km = sat.range / 1000.0
        if raw_el < 0:
            target_az = az
            target_el = 0.0
        elif raw_el <= 90:
            target_az = az
            target_el = raw_el
        else:
            target_az = (az + 180.0) % 360.0
            target_el = 180.0 - raw_el
        return target_az, target_el, rng_km, raw_el
