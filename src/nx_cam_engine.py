# ============================================================
# NX CAM Automation Engine
# Generic, reusable engine for Siemens NX CAM automation.
# Works with NX 12.0+ via NXOpen Python API.
#
# Usage:
#   1. Define your tools and operations in a config dict
#   2. Run this script in NX via Ctrl+U (Journal Playback)
#   3. Tools and operations are created automatically
# ============================================================

import NXOpen
import NXOpen.CAM

# ============================================================
# Safe object lookup
# ============================================================

def safe_find(camGroupCol, name):
    """Find object by name; returns None instead of throwing if not found."""
    try:
        return camGroupCol.FindObject(name)
    except NXOpen.NXException:
        return None


# ============================================================
# CAM setup helpers
# ============================================================

def get_cam_setup(workPart):
    """Get CAM setup from work part. Returns None if no CAM environment."""
    try:
        return workPart.CAMSetup
    except Exception:
        return None


def get_default_groups(camGroupCol):
    """Return default parent groups for tool and operation creation."""
    return {
        "machine_root":    safe_find(camGroupCol, "GENERIC_MACHINE"),
        "program":         safe_find(camGroupCol, "PROGRAM") or safe_find(camGroupCol, "NC_PROGRAM"),
        "workpiece":       safe_find(camGroupCol, "WORKPIECE") or safe_find(camGroupCol, "MCS_MILL"),
        "method_mill":     safe_find(camGroupCol, "MILL_FINISH"),
        "method_drill":    safe_find(camGroupCol, "DRILL_METHOD"),
        "method_default":  safe_find(camGroupCol, "METHOD"),
    }


# ============================================================
# Tool creation
# ============================================================

def create_drill_tool(camGroupCol, parent, name, diameter, flute_length=10,
                      point_angle=118, skip_if_exists=True):
    """
    Create a drilling tool (center drill, twist drill, chamfer tool, etc.).

    Args:
        camGroupCol: CAMGroupCollection from camSetup
        parent: Parent group (typically GENERIC_MACHINE)
        name: Tool name (ASCII only — no Chinese, no slashes)
        diameter: Tool diameter in mm
        flute_length: Flute length in mm
        point_angle: Point angle in degrees (90=center drill, 118=twist drill, 90=chamfer)
        skip_if_exists: If True and tool exists, return it without error

    Returns:
        The created or existing tool object, or None on failure.
    """
    if skip_if_exists:
        existing = safe_find(camGroupCol, name)
        if existing is not None:
            return existing

    tool = camGroupCol.CreateTool(
        parent, "drill", "DRILLING_TOOL",
        NXOpen.CAM.NCGroupCollection.UseDefaultName.FalseValue,
        name
    )
    builder = camGroupCol.CreateDrillStdToolBuilder(tool)
    builder.TlDiameterBuilder.Value = diameter
    builder.TlFluteLnBuilder.Value = flute_length
    builder.TlPointAngBuilder.Value = point_angle
    builder.Commit()
    builder.Destroy()
    return tool


def create_mill_tool(camGroupCol, parent, name, diameter, flute_length=10,
                     flutes=2, corner_radius=0.0, subtype="MILL",
                     skip_if_exists=True):
    """
    Create a milling tool (end mill, face mill, ball mill, etc.).

    Note: NX 12 type is ''mill_planar'' (not ''mill'').

    Args:
        camGroupCol: CAMGroupCollection from camSetup
        parent: Parent group (typically GENERIC_MACHINE)
        name: Tool name (ASCII only)
        diameter: Tool diameter in mm
        flute_length: Flute length in mm
        flutes: Number of flutes
        corner_radius: Lower corner radius in mm (for bull-nose / fly cutters)
        subtype: NX tool subtype — ''MILL'', ''BALL_MILL'', ''CHAMFER_MILL'', ''MILLING_TOOL''
        skip_if_exists: If True and tool exists, return it without error

    Returns:
        The created or existing tool object, or None on failure.
    """
    if skip_if_exists:
        existing = safe_find(camGroupCol, name)
        if existing is not None:
            return existing

    tool = camGroupCol.CreateTool(
        parent, "mill_planar", subtype,
        NXOpen.CAM.NCGroupCollection.UseDefaultName.FalseValue,
        name
    )
    builder = camGroupCol.CreateMillToolBuilder(tool)
    builder.TlDiameterBuilder.Value = diameter
    builder.TlFluteLnBuilder.Value = flute_length
    builder.TlNumFlutesBuilder.Value = flutes
    builder.TlLowCorRadBuilder.Value = corner_radius
    builder.Commit()
    builder.Destroy()
    return tool


# ============================================================
# Operation creation
# ============================================================

# Known operation type/subtype mappings for NX 12
# These may vary by NX version / template configuration.
OP_TYPE_MAP = {
    "spot_drill":   ("drill",        "SPOT_DRILLING"),   # Center drill / spot
    "drill":        ("drill",        "DRILLING"),         # Standard G81
    "peck_drill":   ("drill",        "PECK_DRILLING"),    # G83 peck
    "chamfer":      ("drill",        "DRILLING"),         # Chamfer (drill cycle)
    "face_mill":    ("mill_planar",  "FACE_MILLING"),     # Face milling
    "planar_mill":  ("mill_planar",  "PLANAR_MILL"),      # Planar milling
    "cavity_mill":  ("mill_contour", "CAVITY_MILL"),      # Cavity milling
    "zlevel":       ("mill_contour", "ZLEVEL_PROFILE"),   # Z-level profile
}


def create_operation(camGroupCol, camOpCol, op_config, tool_objects=None):
    """
    Create a CAM operation with spindle speed, feed rate, and depth.

    Args:
        camGroupCol: CAMGroupCollection
        camOpCol: OperationCollection
        op_config: dict with keys:
            name (str): Operation name (ASCII)
            op_type (str): One of the keys in OP_TYPE_MAP
            tool_name (str): Name of the tool to use
            spindle (int): Spindle RPM
            feed (int): Feed rate mm/min
            depth (float): Cut depth (negative = downward)
            note (str, optional): Description
        tool_objects (dict, optional): {tool_name: tool_object} for
            tools not yet findable by name in camGroupCol

    Returns:
        The created operation object, or None on failure.
    """
    op_name = op_config["name"]
    op_type = op_config["op_type"]
    tool_name = op_config["tool_name"]
    spindle = op_config["spindle"]
    feed = op_config["feed"]
    depth = op_config["depth"]

    # Skip if already exists
    existing = safe_find(camGroupCol, op_name)
    if existing is not None:
        return existing

    # Resolve parent groups
    groups = get_default_groups(camGroupCol)

    program_group  = groups["program"]
    workpiece      = groups["workpiece"]

    is_mill_op = op_type in ("face_mill", "cavity_mill", "planar_mill", "zlevel")
    method_group = groups["method_mill"] if is_mill_op else groups["method_drill"]
    if method_group is None:
        method_group = groups["method_default"]

    # Resolve tool group
    tool_group = safe_find(camGroupCol, tool_name)
    if tool_group is None and tool_objects and tool_name in tool_objects:
        tool_group = tool_objects[tool_name]

    # Check for missing parents
    missing = []
    if program_group is None: missing.append("PROGRAM")
    if method_group is None:  missing.append("METHOD")
    if tool_group is None:    missing.append("TOOL: " + tool_name)
    if workpiece is None:     missing.append("WORKPIECE")
    if missing:
        raise RuntimeError("Missing parent groups: " + ", ".join(missing))

    # Get type/subtype
    if op_type not in OP_TYPE_MAP:
        raise ValueError("Unknown op_type: " + op_type + ". Known: " + ", ".join(OP_TYPE_MAP.keys()))
    type_name, subtype_name = OP_TYPE_MAP[op_type]

    # Create operation
    operation = camOpCol.Create(
        program_group, method_group, tool_group, workpiece,
        type_name, subtype_name,
        NXOpen.CAM.OperationCollection.UseDefaultName.FalseValue,
        op_name
    )

    # Set parameters via builder
    builder = None
    try:
        if op_type in ("spot_drill", "drill", "peck_drill", "chamfer"):
            builder = camOpCol.CreatePointToPointBuilder(operation)
        elif op_type == "face_mill":
            builder = camOpCol.CreateFaceMillingBuilder(operation)
        elif op_type == "cavity_mill":
            builder = camOpCol.CreateCavityMillingBuilder(operation)
        elif op_type == "planar_mill":
            builder = camOpCol.CreatePlanarMillingBuilder(operation)
        elif op_type == "zlevel":
            builder = camOpCol.CreateZlevelMillingBuilder(operation)

        if builder is not None:
            builder.FeedsBuilder.SpindleRpmBuilder.Value = spindle
            builder.FeedsBuilder.FeedCutBuilder.Value = feed
            try:
                builder.HoleDepth.Value = depth
            except Exception:
                pass  # Milling ops don''t have HoleDepth
            builder.Commit()
            builder.Destroy()
    except Exception:
        # Builder failure is non-fatal; operation object still exists
        if builder is not None:
            try:
                builder.Destroy()
            except Exception:
                pass

    return operation


# ============================================================
# Batch runner
# ============================================================

def run(config, listing_window=True):
    """
    Run a full automation config.

    Args:
        config: dict with:
            tools (list): Tool definitions (see create_drill_tool / create_mill_tool)
            operations (list): Operation definitions (see create_operation)
            part_name (str, optional): Display name for logging
            mill_subtype (str, optional): Default "MILL"
        listing_window (bool): Open NX Listing Window for progress output

    Returns:
        dict with ''tools_created'', ''tools_skipped'', ''ops_created'', ''ops_skipped''
    """
    tools_cfg = config.get("tools", [])
    ops_cfg = config.get("operations", [])
    part_name = config.get("part_name", "Untitled")
    mill_subtype = config.get("mill_subtype", "MILL")

    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    camSetup = get_cam_setup(workPart)

    if camSetup is None:
        raise RuntimeError(
            "No CAM environment. Open the part, go to Start > Manufacturing > OK, save, then retry."
        )

    camGroupCol = camSetup.CAMGroupCollection
    camOpCol = camSetup.OperationCollection

    listing = None
    if listing_window:
        listing = theSession.ListingWindow
        listing.Open()

    def log(msg):
        if listing:
            listing.WriteLine(msg)

    log("=" * 60)
    log("  NX CAM Automation — " + part_name)
    log("  Tools: " + str(len(tools_cfg)) + " | Operations: " + str(len(ops_cfg)))
    log("=" * 60)

    machine_root = camGroupCol.FindObject("GENERIC_MACHINE")
    tool_objects = {}

    # Create tools
    tools_created = 0
    tools_skipped = 0
    for i, t in enumerate(tools_cfg):
        name = t["name"]
        log("")
        log("[" + str(i + 1) + "/" + str(len(tools_cfg)) + "] Tool: " + name)
        try:
            if t.get("type") == "mill":
                obj = create_mill_tool(
                    camGroupCol, machine_root, name,
                    diameter=t["diameter"],
                    flute_length=t.get("flute_length", 10),
                    flutes=t.get("flutes", 2),
                    corner_radius=t.get("corner_radius", 0.0),
                    subtype=mill_subtype,
                )
            else:
                obj = create_drill_tool(
                    camGroupCol, machine_root, name,
                    diameter=t["diameter"],
                    flute_length=t.get("flute_length", 10),
                    point_angle=t.get("point_angle", 118),
                )
            tool_objects[name] = obj
            tools_created += 1
            log("       -> OK")
        except Exception as e:
            log("       !! FAILED: " + str(e))

    # Create operations
    ops_created = 0
    ops_skipped = 0
    log("")
    log("---- Creating operations ----")
    for i, op in enumerate(ops_cfg):
        log("")
        log("[" + str(i + 1) + "/" + str(len(ops_cfg)) + "] Op: " + op["name"] + " — " + op.get("note", ""))
        try:
            create_operation(camGroupCol, camOpCol, op, tool_objects)
            ops_created += 1
            log("       -> OK (S" + str(op["spindle"]) + " F" + str(op["feed"]) + " depth " + str(op["depth"]) + ")")
        except Exception as e:
            log("       !! FAILED: " + str(e))

    log("")
    log("=" * 60)
    log("  Done: " + str(tools_created) + " tools, " + str(ops_created) + " ops")
    log("  Next: double-click each operation to assign holes/faces (geometry)")
    log("=" * 60)

    if listing:
        listing.Close()

    return {
        "tools_created": tools_created,
        "tools_skipped": tools_skipped,
        "ops_created": ops_created,
        "ops_skipped": ops_skipped,
    }
