import serial
import time
from serial.tools import list_ports
from typing import Optional, Tuple

class ArduinoController:
    def __init__(self, port: Optional[str] = None, baud_rate: int = 115200):
        self.port = port
        self.baud_rate = baud_rate
        self.serial = None
        self.connected = False
    
    def auto_detect_port(self) -> Optional[str]:
        ports = list(list_ports.comports())
        if not ports:
            return None
        preferred_keywords = ["usb", "arduino", "wch", "cp210", "ch340", "modem", "serial"]
        for p in ports:
            text = f"{p.device} {p.description} {p.manufacturer}".lower()
            if any(k in text for k in preferred_keywords):
                return p.device
        return ports[0].device
    
    def connect(self) -> bool:
        if self.port is None:
            self.port = self.auto_detect_port()
        if self.port is None:
            return False
        try:
            self.serial = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2)
            self.connected = True
            return True
        except:
            self.connected = False
            return False
    
    def set_position(self, az: float, el: float):
        if not self.connected or self.serial is None:
            return
        try:
            az = max(0.0, min(360.0, az))
            el = max(0.0, min(90.0, el))
            cmd = f"AZ{az:.2f} EL{el:.2f}\n"
            self.serial.write(cmd.encode())
        except:
            pass
    
    def test_connection(self) -> bool:
        if not self.connected:
            return False
        try:
            self.serial.write(b"AZ\n")
            return True
        except:
            return False
