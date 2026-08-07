# ============================================================
# NX CAM Automation — Configuration format & example
#
# Define your tools and operations here. Copy this file to
# my_config.py and fill in your own factory''s data.
#
# Tool definition fields:
#   name          (str)  Tool name — ASCII only (no Chinese, no /)
#   type          (str)  "drill" or "mill"
#   diameter      (float) mm
#   flute_length  (float) mm (optional, default 10)
#   flutes        (int)   For mill tools (optional, default 2)
#   corner_radius (float) For mill tools, R value (optional, default 0)
#   point_angle   (float) For drill tools, degrees (optional, default 118)
#
# Operation definition fields:
#   name      (str)   Operation name — ASCII only
#   op_type   (str)   One of: spot_drill, drill, peck_drill, chamfer,
#                      face_mill, planar_mill, cavity_mill, zlevel
#   tool_name (str)   Must match a tool name above
#   spindle   (int)   Spindle RPM
#   feed      (int)   Feed rate mm/min
#   depth     (float) Cut depth (negative = downward)
#   note      (str)   Optional description
# ============================================================

# ============================================================
# Example configuration — replace with your own factory data
# ============================================================

EXAMPLE_CONFIG = {
    "part_name": "Example Part",

    # Mill tool subtype in NX: "MILL", "BALL_MILL", "CHAMFER_MILL", "MILLING_TOOL"
    "mill_subtype": "MILL",

    "tools": [
        # Center drill
        {"name": "ZDD4",   "type": "drill", "diameter": 4.0,  "flute_length": 4,  "point_angle": 90},
        # Twist drill
        {"name": "ZD5.2",  "type": "drill", "diameter": 5.2,  "flute_length": 20, "point_angle": 118},
        # Chamfer tool
        {"name": "DJ12",   "type": "drill", "diameter": 12.0, "flute_length": 3,  "point_angle": 90},
        # End mill
        {"name": "XD10R",  "type": "mill",  "diameter": 10.0, "flute_length": 23, "flutes": 2},
        # Bull-nose cutter
        {"name": "D50R08", "type": "mill",  "diameter": 50.0, "flute_length": 18, "flutes": 2, "corner_radius": 0.8},
    ],

    "operations": [
        # Center drill (spot) — always do this first before drilling
        {"name": "OP_SPOT",   "op_type": "spot_drill",  "tool_name": "ZDD4",   "spindle": 1500, "feed": 150, "depth": -2.0,  "note": "Spot drill"},
        # Peck drill (G83) for deep holes
        {"name": "OP_DRILL",  "op_type": "peck_drill",  "tool_name": "ZD5.2",  "spindle": 1100, "feed": 150, "depth": -20.0, "note": "Peck drill G83"},
        # Chamfer — always last
        {"name": "OP_CHAMFER","op_type": "chamfer",     "tool_name": "DJ12",   "spindle": 3000, "feed": 150, "depth": -3.5,  "note": "Chamfer last"},
    ],
}
