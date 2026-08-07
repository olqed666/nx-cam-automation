# ============================================================
# NX CAM Automation — Runner
#
# Place this file and nx_cam_engine.py in the same folder,
# edit CONFIG_FILE to point to your config, then run in NX:
#   NX > Ctrl+U > select this file
#
# Or generate a standalone script from the web frontend.
# ============================================================

import sys
import os

# Add src to path so we can import the engine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nx_cam_engine import run

# ============================================================
# Point this to your config file
# ============================================================

# Option 1: import a Python config
# from config.example_config import EXAMPLE_CONFIG as CONFIG

# Option 2: define inline
CONFIG = {
    "part_name": "My Part",
    "mill_subtype": "MILL",
    "tools": [
        {"name": "ZDD4",  "type": "drill", "diameter": 4.0,  "flute_length": 4,  "point_angle": 90},
        {"name": "ZD5.2", "type": "drill", "diameter": 5.2,  "flute_length": 20, "point_angle": 118},
        {"name": "DJ12",  "type": "drill", "diameter": 12.0, "flute_length": 3,  "point_angle": 90},
    ],
    "operations": [
        {"name": "OP_SPOT",   "op_type": "spot_drill", "tool_name": "ZDD4",  "spindle": 1500, "feed": 150, "depth": -2.0},
        {"name": "OP_DRILL",  "op_type": "peck_drill", "tool_name": "ZD5.2", "spindle": 1100, "feed": 150, "depth": -20.0},
        {"name": "OP_CHAMFER","op_type": "chamfer",    "tool_name": "DJ12",  "spindle": 3000, "feed": 150, "depth": -3.5},
    ],
}

# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    run(CONFIG)
