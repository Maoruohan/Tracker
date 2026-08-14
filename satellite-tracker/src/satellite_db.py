SATELLITES = {
    "METEOR M1": ("METEOR-M", 35865),
    "METEOR-M": ("METEOR-M", 35865),
    "METEOR M2": ("METEOR M2", 40069),
    "METEOR-M2": ("METEOR M2", 40069),
    "METEOR M2-2": ("METEOR M2-2", 44387),
    "METEOR-M2-2": ("METEOR M2-2", 44387),
    "METEOR M2-3": ("METEOR M2-3", 57166),
    "METEOR-M2-3": ("METEOR M2-3", 57166),
    "METEOR M2-4": ("METEOR M2-4", 59051),
    "METEOR-M2-4": ("METEOR M2-4", 59051),
    "ISS": ("ISS (ZARYA)", 25544),
    "ISS (ZARYA)": ("ISS (ZARYA)", 25544),
    "TIANGONG": ("CSS (TIANHE-1)", 48274),
    "CSS": ("CSS (TIANHE-1)", 48274),
    "CSS (TIANHE-1)": ("CSS (TIANHE-1)", 48274),
    "NOAA 15": ("NOAA 15", 25338),
    "NOAA-15": ("NOAA 15", 25338),
    "NOAA 18": ("NOAA 18", 28654),
    "NOAA-18": ("NOAA 18", 28654),
    "NOAA 19": ("NOAA 19", 33591),
    "NOAA-19": ("NOAA 19", 33591),
    "NOAA 20": ("JPSS-1", 43013),
    "NOAA-20": ("JPSS-1", 43013),
    "JPSS-1": ("JPSS-1", 43013),
    "NOAA 21": ("NOAA 21", 54234),
    "NOAA-21": ("NOAA 21", 54234),
    "JPSS-2": ("NOAA 21", 54234),
}

ALIASES = {
    "METEORM1": "METEOR M1",
    "METEORM2": "METEOR M2",
    "METEORM22": "METEOR M2-2",
    "METEORM23": "METEOR M2-3",
    "METEORM24": "METEOR M2-4",
    "ISSZARYA": "ISS",
    "SPACESTATION": "ISS",
    "TIANGONGSPACESTATION": "TIANGONG",
    "CHINESESPACESTATION": "CSS (TIANHE-1)",
    "NOAA15": "NOAA 15",
    "NOAA18": "NOAA 18",
    "NOAA19": "NOAA 19",
    "NOAA20": "NOAA 20",
    "NOAA21": "NOAA 21",
}

def normalize_key(text):
    return text.strip().upper().replace("-", "").replace("_", "").replace(" ", "")

def find_satellite(user_input):
    raw = user_input.strip().upper()
    if raw in SATELLITES:
        return SATELLITES[raw]
    key = normalize_key(raw)
    if key in ALIASES:
        return SATELLITES[ALIASES[key]]
    for sat_key, sat_val in SATELLITES.items():
        if normalize_key(sat_key) == key:
            return sat_val
    return None

def get_all_satellites():
    return sorted(SATELLITES.keys())
