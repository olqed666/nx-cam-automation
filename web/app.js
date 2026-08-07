
// ============================================================
// COMBOS
// ============================================================
const COMBOS = {
  "combo_A": {
    name: "Combo A: Center Drill -> Drill -> Chamfer",
    desc: "Most common drilling combo, covers ~70% of parts",
    steps: [
      { name: "Center Drill", tool: "ZDD4",  depth: -2.0,  type: "spot_drill",  spindle: 1500, feed: 150, note: "Spot (always -2mm)" },
      { name: "Drill",        tool: "ZD5.2", depth: -20.0, type: "peck_drill",  spindle: 1100, feed: 150, note: "G83 peck Q3" },
      { name: "Chamfer",      tool: "DJ12",  depth: -3.5,  type: "chamfer",     spindle: 3000, feed: 150, note: "Deburring (last)" },
    ]
  },
  "combo_B": {
    name: "Combo B: Face Mill -> Center Drill -> Drill -> Chamfer",
    desc: "Parts needing top surface milled flat before drilling",
    steps: [
      { name: "Face Mill",    tool: "XD10R", depth: -16.0, type: "face_mill",   spindle: 6000, feed: 1500, note: "Mill top flat" },
      { name: "Center Drill", tool: "ZDD4",  depth: -2.0,  type: "spot_drill",  spindle: 1500, feed: 150,  note: "Spot (always -2mm)" },
      { name: "Drill",        tool: "ZD6.8", depth: -19.0, type: "peck_drill",  spindle: 1100, feed: 150,  note: "G83 peck" },
      { name: "Chamfer",      tool: "DJ12",  depth: -4.4,  type: "chamfer",     spindle: 3000, feed: 150,  note: "Deburring (last)" },
    ]
  },
  "combo_C": {
    name: "Combo C: Finish (Fly Cutter / Ball Mill)",
    desc: "Simple parts needing only one finishing pass",
    steps: [
      { name: "Finish", tool: "D30R5", depth: -57.5, type: "face_mill", spindle: 6000, feed: 1500, note: "Fly cutter finish" },
    ]
  },
  "combo_D": {
    name: "Combo D: Rough -> Semi-Finish -> Finish",
    desc: "Cavity parts, three-knife strategy",
    steps: [
      { name: "Rough",       tool: "D50R08", depth: -30.0,  type: "cavity_mill", spindle: 4000, feed: 2000, note: "Rough, stock 0.3" },
      { name: "Semi-Finish", tool: "XD10R",  depth: -29.7,  type: "cavity_mill", spindle: 5000, feed: 1500, note: "Semi, stock 0.1" },
      { name: "Finish",      tool: "XD10F",  depth: -30.0,  type: "cavity_mill", spindle: 6000, feed: 1200, note: "Finish to bottom" },
    ]
  },
};

const RULES = [
  { label: "Center drill depth",        value: "-2mm (fixed)" },
  { label: "Center drill before drill", value: "Required" },
  { label: "Drill mode (D5+)",          value: "G83 peck drill" },
  { label: "Default peck depth",        value: "3mm / stroke" },
  { label: "Chamfer position",          value: "Always last" },
  { label: "Mill tool type in NX",      value: "mill_planar (not mill!)" },
  { label: "Tool names",                value: "ASCII only (no Chinese, no /)" },
  { label: "FindObject safety",         value: "Wrap in try/except; throws, not None" },
];

const MILL_SUBTYPE = "MILL";

// ============================================================
// STATE
// ============================================================
let selectedCombo = "combo_A";
let comboData = JSON.parse(JSON.stringify(COMBOS));
let toolsData = JSON.parse(JSON.stringify(TOOLS));

// ============================================================
// RENDER: Stats
// ============================================================
function renderStats() {
  const uniqueTypes = new Set(toolsData.map(t => t.type)).size;
  document.getElementById("stats").innerHTML = [
    { label: "Tools",          value: toolsData.length },
    { label: "Tool Types",     value: uniqueTypes },
    { label: "Process Combos", value: Object.keys(comboData).length },
    { label: "Rules",          value: RULES.length },
  ].map(s => '<div class="stat-card"><div class="label">' + s.label + '</div><div class="value">' + s.value + '</div></div>').join("");
}

// ============================================================
// TYPE BADGES
// ============================================================
function typeBadge(type) {
  var map = {
    "Center Drill": "badge-drill", "Drill": "badge-drill",
    "Chamfer": "badge-chamfer",
    "Fly Cutter": "badge-mill", "Bull Nose": "badge-mill",
    "End Mill": "badge-mill", "Finish Mill": "badge-mill",
    "Ball Mill": "badge-mill",
  };
  return '<span class="badge ' + (map[type] || "badge-drill") + '">' + type + '</span>';
}

// ============================================================
// RENDER: Tools
// ============================================================
function renderTools() {
  var addForm = [
    '<div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;align-items:flex-end">',
    '<div class="param-item" style="margin:0"><label>Name</label><input id="newToolName" placeholder="e.g. ZD10" style="width:90px"></div>',
    '<div class="param-item" style="margin:0"><label>Type</label><select id="newToolType" style="width:120px">',
    '<option>Drill</option><option>Center Drill</option><option>Chamfer</option>',
    '<option>End Mill</option><option>Fly Cutter</option><option>Bull Nose</option>',
    '<option>Ball Mill</option><option>Finish Mill</option>',
    '</select></div>',
    '<div class="param-item" style="margin:0"><label>Dia mm</label><input id="newToolDia" type="number" step="0.1" style="width:70px"></div>',
    '<div class="param-item" style="margin:0"><label>Length mm</label><input id="newToolLen" type="number" step="0.1" style="width:70px"></div>',
    '<div class="param-item" style="margin:0"><label>Flutes</label><input id="newToolFlutes" type="number" step="1" value="2" style="width:60px"></div>',
    '<div class="param-item" style="margin:0"><label>Use</label><input id="newToolUse" style="width:100px"></div>',
    '<button class="btn btn-primary" onclick="addTool()">+ Add</button>',
    '</div>'
  ].join("");

  var rows = toolsData.map(function(t, i) {
    return '<tr>' +
      '<td>' + (i + 1) + '</td>' +
      '<td style="font-weight:500">' + t.name + '</td>' +
      '<td>' + typeBadge(t.type) + '</td>' +
      '<td>D' + t.dia + '</td>' +
      '<td>L' + t.len + '</td>' +
      '<td>' + t.flutes + ' flutes</td>' +
      '<td style="color:var(--text-secondary)">' + t.use + '</td>' +
      '<td><button class="btn" style="padding:2px 8px;font-size:11px" onclick="removeTool(' + i + ')">X</button></td>' +
      '</tr>';
  }).join("");

  return '<div class="card">' +
    '<h2>Tool Library (' + toolsData.length + ' tools)</h2>' +
    '<p style="color:var(--text-secondary);margin-bottom:12px">Add, edit, or remove tools. Changes apply to script generation.</p>' +
    addForm +
    '<div style="overflow-x:auto"><table><thead><tr>' +
    '<th>#</th><th>Name</th><th>Type</th><th>Dia</th><th>Length</th><th>Flutes</th><th>Use</th><th></th>' +
    '</tr></thead><tbody>' + rows + '</tbody></table></div>' +
    '</div>';
}

function addTool() {
  var name = document.getElementById("newToolName").value.trim();
  var type = document.getElementById("newToolType").value;
  var dia = parseFloat(document.getElementById("newToolDia").value);
  var len = parseFloat(document.getElementById("newToolLen").value);
  var flutes = parseInt(document.getElementById("newToolFlutes").value);
  var use = document.getElementById("newToolUse").value.trim();
  if (!name || isNaN(dia) || isNaN(len)) { alert("Fill name, dia, and length"); return; }
  toolsData.push({ name: name, type: type, dia: dia, len: len, flutes: flutes, use: use });
  renderStats();
  switchTab("tools");
}

function removeTool(i) { toolsData.splice(i, 1); renderStats(); switchTab("tools"); }

// ============================================================
// RENDER: Combos
// ============================================================
function renderCombos() {
  return Object.entries(comboData).map(function(entry) {
    var key = entry[0], combo = entry[1];
    var stepsHtml = combo.steps.map(function(s, i) {
      return '<div class="process-step">' +
        '<div class="step-num">Step ' + (i + 1) + '</div>' +
        '<div class="step-tool">' + s.name + '</div>' +
        '<div class="step-info">' + s.tool + '</div>' +
        '<div class="step-info">depth ' + s.depth + ' | S' + s.spindle + ' F' + s.feed + '</div>' +
        '<div class="step-info" style="margin-top:4px;font-weight:500">' + s.note + '</div>' +
        '</div>';
    }).join('<div class="process-arrow">-></div>');

    return '<div class="combo-card" onclick="selectCombo(\'' + key + '\')" id="combo-' + key + '">' +
      '<h3>' + combo.name + '</h3>' +
      '<p style="color:var(--text-secondary);margin:4px 0 12px">' + combo.desc + '</p>' +
      '<div class="process-flow">' + stepsHtml + '</div>' +
      '<div style="margin-top:12px">' +
      '<span style="font-size:12px;color:var(--text-muted)">' +
      combo.steps.length + ' ops | ' + new Set(combo.steps.map(function(s){return s.tool})).size + ' unique tools' +
      '</span></div></div>';
  }).join("");
}

// ============================================================
// RENDER: Rules / Settings
// ============================================================
function renderRules() {
  var rulesHtml = RULES.map(function(r) {
    return '<div class="rule-row"><span class="rule-label">' + r.label + '</span><span class="rule-value">' + r.value + '</span></div>';
  }).join("");
  return '<div class="card">' +
    '<h2>Settings & Rules</h2>' +
    rulesHtml +
    '<div class="rule-row" style="margin-top:12px"><span class="rule-label">Mill tool subtype</span><span class="rule-value"><code>' + MILL_SUBTYPE + '</code></span></div>' +
    '<div style="margin-top:16px">' +
    '<div class="upload-area" onclick="importJSON()">Click to import JSON config file (tools + combos)</div>' +
    '<input type="file" id="fileInput" accept=".json" style="display:none" onchange="handleFileImport(event)">' +
    '</div></div>';
}

// ============================================================
// PARAMS STATE
// ============================================================
var PARAMS_STATE = {};

function getEdit(comboKey, idx) {
  return (PARAMS_STATE[comboKey] || {})[idx] || {};
}

function saveParam(comboKey, idx, field, value) {
  if (!PARAMS_STATE[comboKey]) PARAMS_STATE[comboKey] = {};
  if (!PARAMS_STATE[comboKey][idx]) PARAMS_STATE[comboKey][idx] = {};
  PARAMS_STATE[comboKey][idx][field] = parseFloat(value);
}

function resetParams(comboKey) {
  if (confirm("Reset all params for this combo?")) {
    delete PARAMS_STATE[comboKey];
    switchTab("params");
  }
}

// ============================================================
// HELPERS
// ============================================================
function getPointAngle(toolName) {
  if (toolName.indexOf("ZDD") === 0) return 90;
  if (toolName.indexOf("DJ") === 0) return 90;
  return 118;
}

var MILL_TYPES = ["Fly Cutter", "Bull Nose", "End Mill", "Finish Mill", "Ball Mill"];
function isMillType(type) { return MILL_TYPES.indexOf(type) >= 0; }

function toolToInternal(name) {
  return name.replace(/[^A-Za-z0-9.]/g, "");
}

// ============================================================
// RENDER: Params editor
// ============================================================
function renderParams() {
  var combo = comboData[selectedCombo];

  var comboBtns = Object.entries(comboData).map(function(entry) {
    var k = entry[0], c = entry[1];
    var active = k === selectedCombo ? "background:var(--accent-light);border-color:var(--accent);" : "";
    return '<button class="btn" style="margin-right:6px;' + active + '" onclick="selectComboParams(\'' + k + '\')">' + c.name.split(":")[0] + '</button>';
  }).join("");

  var rows = combo.steps.map(function(s, i) {
    var t = toolsData.find(function(x) { return x.name === s.tool; });
    var millType = t && isMillType(t.type);
    var edit = getEdit(selectedCombo, i);

    var dia     = edit.dia     !== undefined ? edit.dia     : (t ? t.dia    : 4.0);
    var flute   = edit.flute   !== undefined ? edit.flute   : (t ? t.len    : 10);
    var flutes  = edit.flutes  !== undefined ? edit.flutes  : (t ? t.flutes : 2);
    var cornerR = edit.cornerR !== undefined ? edit.cornerR : (t && t.r ? t.r : 0.0);
    var pAngle  = edit.pAngle  !== undefined ? edit.pAngle  : getPointAngle(s.tool);
    var spindle = edit.spindle !== undefined ? edit.spindle : s.spindle;
    var feed    = edit.feed    !== undefined ? edit.feed    : s.feed;
    var depth   = edit.depth   !== undefined ? edit.depth   : s.depth;

    function inp(field, val, step) {
      return '<input type="number" class="param-inp" step="' + step + '" value="' + val + '" onchange="saveParam(\'' + selectedCombo + '\', ' + i + ', \'' + field + '\', this.value)">';
    }

    return '<tr>' +
      '<td style="font-weight:500">' + (i+1) + '. ' + s.name + '</td>' +
      '<td style="color:var(--text-secondary)">' + s.tool + '</td>' +
      '<td>' + inp("dia", dia, "0.1") + ' mm</td>' +
      '<td>' + inp("flute", flute, "0.1") + ' mm</td>' +
      (millType
        ? '<td>' + inp("flutes", flutes, "1") + ' fl</td><td>' + inp("cornerR", cornerR, "0.1") + ' mm</td>'
        : '<td>' + inp("pAngle", pAngle, "1") + ' deg</td><td>--</td>') +
      '<td>S ' + inp("spindle", spindle, "10") + '</td>' +
      '<td>F ' + inp("feed", feed, "10") + '</td>' +
      '<td>Z ' + inp("depth", depth, "0.1") + '</td>' +
      '</tr>';
  }).join("");

  return '<div class="card">' +
    '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px">' +
    '<h2 style="margin:0">Edit Parameters - ' + combo.name + '</h2>' +
    '<div>' + comboBtns +
    '<button class="btn" onclick="resetParams(\'' + selectedCombo + '\')" style="margin-left:8px">Reset Defaults</button>' +
    '<button class="btn btn-primary" onclick="downloadScript()" style="margin-left:8px">Download .py</button>' +
    '</div></div>' +
    '<p style="color:var(--text-secondary);margin-bottom:12px">Edit values directly. Changes apply to script preview and downloaded scripts immediately.</p>' +
    '<div style="overflow-x:auto"><table><thead><tr>' +
    '<th>Op</th><th>Tool</th><th>Dia</th><th>Length</th><th>Flutes/Angle</th><th>Corner R</th><th>Spindle S</th><th>Feed F</th><th>Depth Z</th>' +
    '</tr></thead><tbody>' + rows + '</tbody></table></div>' +
    '</div>';
}

// ============================================================
// SCRIPT GENERATOR
// ============================================================
var OP_TYPE_MAP = {
  spot_drill:  ["drill",        "SPOT_DRILLING"],
  drill:       ["drill",        "DRILLING"],
  peck_drill:  ["drill",        "PECK_DRILLING"],
  chamfer:     ["drill",        "DRILLING"],
  face_mill:   ["mill_planar",  "FACE_MILLING"],
  cavity_mill: ["mill_contour", "CAVITY_MILL"],
};

function generateScript(comboKey) {
  var combo = comboData[comboKey];
  var steps = combo.steps;

  var lines = [
    "# ============================================================",
    "# NX CAM Automation - " + combo.name,
    "# Generated by nx-cam-automation web tool",
    "# Run: NX > Ctrl+U > select this file",
    "# ============================================================",
    '"""',
    "Usage: Open .prt in NX > Ctrl+U > select this file > run",
    '"""',
    "",
    "import NXOpen",
    "import NXOpen.CAM",
    "",
    "# ===== Mill tool subtype (change if needed: BALL_MILL / MILLING_TOOL) =====",
    'MILL_SUBTYPE = "' + MILL_SUBTYPE + '"',
    "",
    "# ===== User parameters =====",
    'PART_NAME = "' + combo.desc + '"',
  ];

  // Tool params
  steps.forEach(function(s, i) {
    var internal = toolToInternal(s.tool);
    var t = toolsData.find(function(x) { return x.name === s.tool; });
    var edit = getEdit(comboKey, i);
    var dia     = edit.dia     !== undefined ? edit.dia     : (t ? t.dia    : 4.0);
    var flute   = edit.flute   !== undefined ? edit.flute   : (t ? t.len    : 10);
    var flutes  = edit.flutes  !== undefined ? edit.flutes  : (t ? t.flutes : 2);
    var cornerR = edit.cornerR !== undefined ? edit.cornerR : (t && t.r ? t.r : 0.0);
    var pAngle  = edit.pAngle  !== undefined ? edit.pAngle  : getPointAngle(s.tool);
    var millType = t ? isMillType(t.type) : false;

    var idx = i + 1;
    lines.push("");
    lines.push("# --- Tool " + idx + ": " + s.name + " (" + s.tool + ") ---");
    lines.push("NAME_" + idx + "      = "" + internal + """);
    lines.push("DIA_" + idx + "       = " + dia + "       # diameter mm");
    lines.push("FLUTE_" + idx + "     = " + flute + "      # flute length mm");
    if (millType) {
      lines.push("FLUTES_" + idx + "    = " + flutes + "       # number of flutes");
      lines.push("CORNER_R_" + idx + " = " + cornerR + "     # lower corner radius mm");
    } else {
      lines.push("PANGLE_" + idx + "    = " + pAngle + "     # point angle deg");
    }
  });

  lines.push("");
  lines.push("# ===== Automation logic =====");
  lines.push("");
  lines.push("def safe_find(camGroupCol, name):");
  lines.push("    try:");
  lines.push("        return camGroupCol.FindObject(name)");
  lines.push("    except NXOpen.NXException:");
  lines.push("        return None");
  lines.push("");
  lines.push("def create_drill_tool(camGroupCol, machineRoot, name, dia, flute, pangle):");
  lines.push('    """Create drill-type tool (center drill / twist drill / chamfer)"""');
  lines.push('    tool = camGroupCol.CreateTool(machineRoot, "drill", "DRILLING_TOOL",');
  lines.push("        NXOpen.CAM.NCGroupCollection.UseDefaultName.FalseValue, name)");
  lines.push("    builder = camGroupCol.CreateDrillStdToolBuilder(tool)");
  lines.push("    builder.TlDiameterBuilder.Value = dia");
  lines.push("    builder.TlFluteLnBuilder.Value = flute");
  lines.push("    builder.TlPointAngBuilder.Value = pangle");
  lines.push("    builder.Commit()");
  lines.push("    builder.Destroy()");
  lines.push("");
  lines.push("def create_mill_tool(camGroupCol, machineRoot, name, dia, flute, flutes, corner_r):");
  lines.push('    """Create mill-type tool (end mill / bull nose / ball mill)"""');
  lines.push('    tool = camGroupCol.CreateTool(machineRoot, "mill_planar", MILL_SUBTYPE,');
  lines.push("        NXOpen.CAM.NCGroupCollection.UseDefaultName.FalseValue, name)");
  lines.push("    builder = camGroupCol.CreateMillToolBuilder(tool)");
  lines.push("    builder.TlDiameterBuilder.Value = dia");
  lines.push("    builder.TlFluteLnBuilder.Value = flute");
  lines.push("    builder.TlNumFlutesBuilder.Value = flutes");
  lines.push("    builder.TlLowCorRadBuilder.Value = corner_r");
  lines.push("    builder.Commit()");
  lines.push("    builder.Destroy()");
  lines.push("");
  lines.push("def main():");
  lines.push("    theSession = NXOpen.Session.GetSession()");
  lines.push("    workPart = theSession.Parts.Work");
  lines.push("    camSetup = workPart.CAMSetup");
  lines.push("    camGroupCol = camSetup.CAMGroupCollection");
  lines.push("    camOpCol = camSetup.OperationCollection");
  lines.push('    machineRoot = camGroupCol.FindObject("GENERIC_MACHINE")');
  lines.push("");
  lines.push("    listing = theSession.ListingWindow");
  lines.push("    listing.Open()");
  lines.push('    print("  NX CAM - " + PART_NAME)');
  lines.push("");

  // Tool creation
  steps.forEach(function(s, i) {
    var idx = i + 1;
    var t = toolsData.find(function(x) { return x.name === s.tool; });
    var millType = t ? isMillType(t.type) : false;
    lines.push("    # [" + idx + "/" + steps.length + "] " + s.name + " - " + s.tool);
    lines.push('    print("[" + str(' + idx + ') + "/" + str(' + steps.length + ')] ' + s.name + ' - ' + s.tool + '")');
    lines.push("    tool_" + idx + " = safe_find(camGroupCol, NAME_" + idx + ")");
    lines.push("    if tool_" + idx + " is None:");
    if (millType) {
      lines.push("        create_mill_tool(camGroupCol, machineRoot, NAME_" + idx + ", DIA_" + idx + ", FLUTE_" + idx + ", FLUTES_" + idx + ", CORNER_R_" + idx + ")");
    } else {
      lines.push("        create_drill_tool(camGroupCol, machineRoot, NAME_" + idx + ", DIA_" + idx + ", FLUTE_" + idx + ", PANGLE_" + idx + ")");
    }
    lines.push('        print("       -> created")');
    lines.push("    else:");
    lines.push('        print("       -> exists, skipped")');
    lines.push("");
  });

  // Operation creation
  lines.push('    print("")');
  lines.push('    print("---- Creating operations ----")');
  lines.push("");
  lines.push("    # Find parent groups");
  lines.push('    program_group = safe_find(camGroupCol, "PROGRAM") or safe_find(camGroupCol, "NC_PROGRAM")');
  lines.push('    geom_group = safe_find(camGroupCol, "WORKPIECE") or safe_find(camGroupCol, "MCS_MILL")');
  lines.push('    method_mill = safe_find(camGroupCol, "MILL_FINISH")');
  lines.push('    method_drill = safe_find(camGroupCol, "DRILL_METHOD")');
  lines.push("");

  steps.forEach(function(s, i) {
    var idx = i + 1;
    var isMillOp = s.type === "face_mill" || s.type === "cavity_mill";
    var ts = OP_TYPE_MAP[s.type] || ["drill", "DRILLING"];
    var edit = getEdit(comboKey, i);
    var spindle = edit.spindle !== undefined ? edit.spindle : s.spindle;
    var feed    = edit.feed    !== undefined ? edit.feed    : s.feed;
    var depth   = edit.depth   !== undefined ? edit.depth   : s.depth;

    lines.push("    # Op " + (i+1) + ": " + s.name + " - " + s.note);
    lines.push('    if safe_find(camGroupCol, "OP_' + (i+1) + '") is None:');
    lines.push("        method_group = method_mill if " + (isMillOp ? "True" : "False") + " else method_drill");
    lines.push('        if method_group is None: method_group = safe_find(camGroupCol, "METHOD")');
    lines.push('        op_type, op_subtype = ["' + ts[0] + '", "' + ts[1] + '"]');
    lines.push("        op = camOpCol.Create(program_group, method_group, tool_" + idx + ", geom_group,");
    lines.push("            op_type, op_subtype,");
    lines.push('            NXOpen.CAM.OperationCollection.UseDefaultName.FalseValue, "OP_' + (i+1) + '")');
    lines.push("        try:");
    if (s.type === "face_mill")
      lines.push("            b = camOpCol.CreateFaceMillingBuilder(op)");
    else if (s.type === "cavity_mill")
      lines.push("            b = camOpCol.CreateCavityMillingBuilder(op)");
    else
      lines.push("            b = camOpCol.CreatePointToPointBuilder(op)");
    lines.push("            b.FeedsBuilder.SpindleRpmBuilder.Value = " + spindle);
    lines.push("            b.FeedsBuilder.FeedCutBuilder.Value = " + feed);
    lines.push("            try:");
    lines.push("                b.HoleDepth.Value = " + depth);
    lines.push("            except Exception:");
    lines.push("                pass");
    lines.push("            b.Commit()");
    lines.push("            b.Destroy()");
    lines.push('            print("       -> op created (S' + str(' + spindle + ') + ' F' + str(' + feed + ') + ' depth ' + str(' + depth + ') + ')")');
    lines.push("        except Exception as e:");
    lines.push('            print("       !! builder failed: " + str(e))');
    lines.push("    else:");
    lines.push('        print("       -> op exists, skipped")');
    lines.push("");
  });

  lines.push('    print("")');
  lines.push('    print("  Done: ' + steps.length + ' tools, ' + steps.length + ' ops")');
  lines.push('    print("  Next: double-click each operation to assign holes/faces")');
  lines.push("    listing.Close()");
  lines.push("");
  lines.push('if __name__ == "__main__":');
  lines.push("    main()");

  return lines.join("\n");
}

// ============================================================
// NAVIGATION
// ============================================================
function selectCombo(key) { selectedCombo = key; switchTab("script"); }
function selectComboParams(key) { selectedCombo = key; switchTab("params"); }

function switchTab(tab) {
  document.querySelectorAll(".tab").forEach(function(t) {
    t.classList.toggle("active", t.getAttribute("data-tab") === tab);
  });
  var content = document.getElementById("tab-content");
  if (tab === "tools")   content.innerHTML = renderTools();
  if (tab === "combos")  content.innerHTML = renderCombos();
  if (tab === "rules")   content.innerHTML = renderRules();
  if (tab === "params")  content.innerHTML = renderParams();
  if (tab === "script")  content.innerHTML = renderScriptPreview();
}

function renderScriptPreview() {
  var combo = comboData[selectedCombo];
  var code = generateScript(selectedCombo);

  var comboBtns = Object.entries(comboData).map(function(entry) {
    var k = entry[0], c = entry[1];
    var active = k === selectedCombo ? "background:var(--accent-light);border-color:var(--accent);" : "";
    return '<button class="btn" style="margin-right:6px;' + active + '" onclick="selectCombo(\'' + k + '\')">' + c.name.split(":")[0] + '</button>';
  }).join("");

  return '<div class="card">' +
    '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px">' +
    '<h2 style="margin:0">Script Preview - ' + combo.name + '</h2>' +
    '<div>' + comboBtns +
    '<button class="btn btn-primary" onclick="downloadScript()" style="margin-left:12px">Download .py File</button>' +
    '</div></div>' +
    '<p style="color:var(--text-secondary);margin-bottom:12px">Ready-to-run Python script for NX 12+. Download and copy to factory PC, then Ctrl+U in NX.</p>' +
    '<div class="script-preview">' + escapeHtml(code) + '</div>' +
    '</div>';
}

// ============================================================
// DOWNLOAD
// ============================================================
function downloadScript() {
  var code = generateScript(selectedCombo);
  var filename = "nx_cam_" + selectedCombo + ".py";
  var blob = new Blob([code], { type: "text/plain" });
  var url = URL.createObjectURL(blob);
  var a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// ============================================================
// IMPORT / EXPORT JSON
// ============================================================
function importJSON() { document.getElementById("fileInput").click(); }

function handleFileImport(event) {
  var file = event.target.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function(e) {
    try {
      var data = JSON.parse(e.target.result);
      if (data.tools)  toolsData = data.tools;
      if (data.combos) comboData = data.combos;
      renderStats();
      switchTab("tools");
    } catch (err) {
      alert("Invalid JSON file: " + err.message);
    }
  };
  reader.readAsText(file);
}

// ============================================================
// INIT
// ============================================================
renderStats();
document.getElementById("tab-content").innerHTML = renderCombos();
