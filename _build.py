# -*- coding: utf-8 -*-
import os

OUT = r"E:\CAM自动化\nx-cam-automation\web\index.html"

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NX CAM 自动化面板</title>
<style>
  :root {
    --bg: #ffffff;
    --bg-secondary: #f8f9fa;
    --text: #2c2c2a;
    --text-secondary: #5f5e5a;
    --text-muted: #888780;
    --border: #d3d1c7;
    --accent: #534ab7;
    --accent-light: #eeedfe;
    --green: #1d9e75;
    --green-light: #e1f5ee;
    --amber: #ef9f27;
    --amber-light: #faeeda;
    --coral: #d85a30;
    --coral-light: #faece7;
    --radius: 12px;
    --radius-sm: 8px;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f1efe8;
    color: var(--text);
    line-height: 1.6;
    font-size: 13px;
    padding: 24px;
  }
  .container { max-width: 1100px; margin: 0 auto; }

  h1 { font-size: 20px; font-weight: 500; margin-bottom: 4px; }
  h2 { font-size: 15px; font-weight: 500; margin: 24px 0 12px; }
  h3 { font-size: 13px; font-weight: 500; }

  .header {
    background: var(--bg);
    border: 0.5px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 24px;
    margin-bottom: 20px;
  }
  .header-row {
    display: flex; justify-content: space-between; align-items: flex-start;
    flex-wrap: wrap; gap: 16px;
  }
  .header .meta { color: var(--text-secondary); font-size: 12px; }

  .stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
  }
  .stat-card {
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
    padding: 16px;
    border: 0.5px solid var(--border);
  }
  .stat-card .label { font-size: 12px; color: var(--text-muted); margin-bottom: 4px; }
  .stat-card .value { font-size: 28px; font-weight: 500; }

  .card {
    background: var(--bg);
    border: 0.5px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 24px;
    margin-bottom: 20px;
  }

  .tabs {
    display: flex; gap: 0; margin-bottom: 16px;
    border-bottom: 1px solid var(--border);
  }
  .tab {
    padding: 8px 16px; cursor: pointer;
    border: none; background: none;
    font-size: 13px; color: var(--text-secondary);
    border-bottom: 2px solid transparent;
    font-family: inherit;
  }
  .tab.active {
    color: var(--accent);
    border-bottom: 2px solid var(--accent);
  }
  .tab:hover { color: var(--text); }

  .process-flow {
    display: flex; align-items: center; gap: 8px;
    flex-wrap: wrap; padding: 12px 0;
    overflow-x: auto;
  }
  .process-step {
    background: var(--bg-secondary);
    border: 0.5px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 12px 16px;
    min-width: 140px;
    text-align: center;
    flex-shrink: 0;
  }
  .process-step .step-num {
    font-size: 11px; color: var(--text-muted); margin-bottom: 4px;
  }
  .process-step .step-tool {
    font-weight: 500; font-size: 14px;
  }
  .process-step .step-info {
    font-size: 11px; color: var(--text-secondary); margin-top: 4px;
  }
  .process-arrow {
    color: var(--text-muted); font-size: 16px;
    flex-shrink: 0;
  }

  table { width: 100%; border-collapse: collapse; }
  th {
    text-align: left; padding: 8px 12px;
    font-size: 12px; font-weight: 500; color: var(--text-secondary);
    border-bottom: 1px solid var(--border);
  }
  td {
    padding: 8px 12px; border-bottom: 0.5px solid var(--border);
  }
  tr:hover { background: var(--bg-secondary); }

  .badge {
    display: inline-block; padding: 2px 8px; border-radius: 10px;
    font-size: 11px; font-weight: 500;
  }
  .badge-drill { background: var(--accent-light); color: var(--accent); }
  .badge-chamfer { background: var(--amber-light); color: var(--amber); }
  .badge-mill { background: var(--green-light); color: var(--green); }
  .badge-center { background: var(--coral-light); color: var(--coral); }

  .combo-card {
    border: 0.5px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 16px;
    margin-bottom: 12px;
    cursor: pointer;
    transition: border-color 0.2s;
  }
  .combo-card:hover { border-color: var(--accent); }
  .combo-card.selected { border: 1.5px solid var(--accent); background: var(--accent-light); }

  .script-preview {
    background: #2c2c2a; color: #d3d1c7;
    border-radius: var(--radius-sm);
    padding: 16px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    line-height: 1.5;
    overflow-x: auto;
    white-space: pre-wrap;
    max-height: 400px;
    overflow-y: auto;
  }

  .param-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
  }
  .param-item { margin-bottom: 12px; }
  .param-item label {
    display: block; font-size: 12px; color: var(--text-secondary);
    margin-bottom: 4px;
  }
  .param-item input, .param-item select {
    width: 100%; padding: 8px 12px;
    border: 0.5px solid var(--border);
    border-radius: 6px; font-size: 13px;
    font-family: inherit;
  }

  .btn {
    padding: 8px 20px; border: 0.5px solid var(--border);
    border-radius: 6px; font-size: 13px; cursor: pointer;
    background: var(--bg); font-family: inherit;
  }
  .btn-primary {
    background: var(--accent); color: white; border: none;
  }
  .btn-primary:hover { opacity: 0.9; }
  .btn:hover { background: var(--bg-secondary); }

  .rule-row {
    display: flex; align-items: center; gap: 12px;
    padding: 8px 0; border-bottom: 0.5px solid var(--border);
  }
  .rule-label { width: 200px; font-weight: 500; flex-shrink: 0; }
  .rule-value { color: var(--text-secondary); }

  .empty-state {
    text-align: center; padding: 40px 20px;
    color: var(--text-muted);
  }

  input[type=number].param-inp {
    width: 70px; padding: 4px 8px;
    border: 0.5px solid var(--border);
    border-radius: 6px; font-size: 12px;
  }
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <div class="header-row">
      <div>
        <h1>NX CAM 自动化面板</h1>
        <p class="meta">配置刀具与工艺组合，一键下载可运行 Python 脚本（Siemens NX 12+）</p>
        <p class="meta">生成时间：<span id="genTime"></span></p>
      </div>
    </div>
  </div>

  <div class="stats" id="stats"></div>

  <div class="tabs">
    <button class="tab active" data-tab="combos" onclick="switchTab('combos')">工艺组合</button>
    <button class="tab" data-tab="tools" onclick="switchTab('tools')">刀具库</button>
    <button class="tab" data-tab="rules" onclick="switchTab('rules')">工艺规则</button>
    <button class="tab" data-tab="params" onclick="switchTab('params')">参数设置</button>
    <button class="tab" data-tab="script" onclick="switchTab('script')">脚本预览</button>
  </div>

  <div id="tab-content"></div>

</div>

<script>
// ============================================================
// 数据定义
// ============================================================

const TOOLS = [
  {name:"中心钻D4",   type:"中心钻", dia:4.0,  len:4,   flutes:2, use:"点窝"},
  {name:"钻头D5.2",   type:"钻头",   dia:5.2,  len:20,  flutes:2, use:"钻孔"},
  {name:"倒角刀D12",  type:"倒角刀", dia:12.0, len:3,   flutes:3, use:"去毛刺"},
  {name:"飞刀D30R5",  type:"飞刀",   dia:30.0, len:22,  flutes:5, use:"光平面", r:5},
];

const COMBOS = {
  "combo_A": {
    name: "示例组合A：中心钻→钻孔→倒角",
    desc: "通用钻孔工艺，适用于大多数零件",
    steps: [
      {name:"中心钻", tool:"中心钻D4",  depth:-2,   type:"spot_drill", spindle:1500, feed:150, note:"点窝"},
      {name:"钻孔",   tool:"钻头D5.2",  depth:-20,  type:"peck_drill", spindle:1100, feed:150, note:"G83啄钻"},
      {name:"倒角",   tool:"倒角刀D12", depth:-3.5, type:"drill",      spindle:3000, feed:150, note:"去毛刺（最后）"},
    ]
  },
};

const RULES = [
  {label:"中心钻深度",             value:"-2mm（铁律）"},
  {label:"钻孔前必须打中心钻",     value:"是"},
  {label:"D5以上钻孔模式",         value:"G83 啄钻"},
  {label:"啄钻默认量",             value:"3mm/次"},
  {label:"倒角位置",               value:"最后阶段"},
  {label:"坐标X/Y",                value:"分中/分中"},
  {label:"坐标Z",                  value:"顶部"},
];

// ============================================================
// 渲染
// ============================================================

function renderStats() {
  const uniqueTypes = new Set(TOOLS.map(t=>t.type)).size;
  document.getElementById('stats').innerHTML = [
    {label:'刀具总数', value:TOOLS.length},
    {label:'刀具类型', value:uniqueTypes},
    {label:'工艺组合', value:Object.keys(COMBOS).length},
    {label:'工艺规则', value:RULES.length},
  ].map(s => `<div class="stat-card"><div class="label">${s.label}</div><div class="value">${s.value}</div></div>`).join('');
}

function typeBadge(type) {
  const map = {
    "中心钻": "badge-center",
    "钻头":   "badge-drill",
    "倒角刀": "badge-chamfer",
    "飞刀":   "badge-mill",
    "铣刀":   "badge-mill",
    "圆鼻刀": "badge-mill",
    "球刀":   "badge-mill",
    "精铣刀": "badge-mill",
    "粗铣刀": "badge-mill",
    "铰刀":   "badge-drill",
    "丝锥":   "badge-drill",
    "镗刀":   "badge-drill",
    "T型刀":  "badge-mill",
    "燕尾刀": "badge-mill",
  };
  return `<span class="badge ${map[type]||'badge-drill'}">${type}</span>`;
}

function renderTools() {
  let rows = TOOLS.map((t,i) => `
    <tr>
      <td>${i+1}</td>
      <td style="font-weight:500">${t.name}</td>
      <td>${typeBadge(t.type)}</td>
      <td>⌀${t.dia}mm</td>
      <td>刃长${t.len}mm</td>
      <td>${t.flutes}刃</td>
      <td style="color:var(--text-secondary)">${t.use}</td>
    </tr>
  `).join('');

  return `
    <div class="card">
      <h2>刀具库（${TOOLS.length}把）</h2>
      <div style="overflow-x:auto">
        <table>
          <thead>
            <tr>
              <th>#</th><th>刀具名称</th><th>类型</th>
              <th>直径</th><th>刃长</th><th>刃数</th><th>用途</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
      <p style="margin-top:12px;font-size:12px;color:var(--text-muted)">
        直接修改上方 TOOLS 数组可增减刀具，或导入 JSON 配置文件。
      </p>
    </div>
  `;
}

function renderCombos() {
  return Object.entries(COMBOS).map(([key, combo]) => {
    const stepsHtml = combo.steps.map((s, i) => `
      <div class="process-step">
        <div class="step-num">第${i+1}步</div>
        <div class="step-tool">${s.name}</div>
        <div class="step-info">${s.tool}</div>
        <div class="step-info">深${s.depth}mm | S${s.spindle} F${s.feed}</div>
        <div class="step-info" style="margin-top:4px;font-weight:500">${s.note}</div>
      </div>
    `).join('<div class="process-arrow">→</div>');

    return `
      <div class="combo-card" onclick="selectCombo('${key}')" id="combo-${key}">
        <h3>${combo.name}</h3>
        <p style="color:var(--text-secondary);margin:4px 0 12px">${combo.desc}</p>
        <div class="process-flow">
          ${stepsHtml}
        </div>
        <div style="margin-top:12px">
          <span style="font-size:12px;color:var(--text-muted)">
            ${combo.steps.length}个工序 | 用刀数：${new Set(combo.steps.map(s=>s.tool)).size}
          </span>
        </div>
      </div>
    `;
  }).join('');
}

function renderRules() {
  return `
    <div class="card">
      <h2>工艺规则（硬性约定）</h2>
      ${RULES.map(r => `
        <div class="rule-row">
          <span class="rule-label">${r.label}</span>
          <span class="rule-value">${r.value}</span>
        </div>
      `).join('')}
      <p style="margin-top:12px;font-size:12px;color:var(--text-muted)">
        直接修改上方 RULES 数组可增删规则。
      </p>
    </div>
  `;
}

let selectedCombo = 'combo_A';

function selectCombo(key) {
  selectedCombo = key;
  const card = document.getElementById('combo-'+key);
  if (card) {
    document.querySelectorAll('.combo-card').forEach(c => c.classList.remove('selected'));
    card.classList.add('selected');
  }
  switchTab('script');
}

function renderScriptPreview() {
  const combo = COMBOS[selectedCombo];
  const code = generateProductionScript(selectedCombo);
  return `
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px">
        <h2 style="margin:0">脚本预览 — ${combo.name}</h2>
        <div>
          ${Object.entries(COMBOS).map(([k,c]) => `
            <button class="btn" style="margin-right:6px;${k===selectedCombo?'background:var(--accent-light);border-color:var(--accent);':''}"
              onclick="selectCombo('${k}')">${c.name.split('：')[0]}</button>
          `).join('')}
          <button class="btn btn-primary" onclick="downloadScript()" style="margin-left:12px">⬇ 下载 .py 文件</button>
        </div>
      </div>
      <p style="color:var(--text-secondary);margin-bottom:12px">
        下方是可直接在 NX 12 中运行的 Python 脚本。<br>
        点击「下载 .py」保存到桌面 → 拷贝到工厂 → NX Ctrl+U 运行。
      </p>
      <div class="script-preview">${escapeHtml(code)}</div>
    </div>
  `;
}

// ============================================================
// 工具函数
// ============================================================

function toolToInternal(name) {
  return name.replace(/[\u4e00-\u9fff]/g, '').replace(/[\/\s]/g, '');
}

function isMillTool(type) {
  const millTypes = ['飞刀','铣刀','圆鼻刀','球刀','精铣刀','粗铣刀','T型刀','燕尾刀'];
  return millTypes.includes(type);
}

function getPointAngle(toolName) {
  if (toolName.indexOf('中心钻') >= 0) return 90;
  if (toolName.indexOf('倒角') >= 0) return 90;
  return 118;
}

// ============================================================
// 参数设置
// ============================================================
const MILL_SUBTYPE = "MILL";
const PARAMS_STATE = {};

function getEdit(comboKey, idx) {
  const comboEdits = PARAMS_STATE[comboKey] || {};
  return comboEdits[idx] || {};
}

function saveParam(comboKey, idx, field, value) {
  if (!PARAMS_STATE[comboKey]) PARAMS_STATE[comboKey] = {};
  if (!PARAMS_STATE[comboKey][idx]) PARAMS_STATE[comboKey][idx] = {};
  PARAMS_STATE[comboKey][idx][field] = parseFloat(value);
}

function resetParams(comboKey) {
  if (confirm('确定恢复 "' + (COMBOS[comboKey] ? COMBOS[comboKey].name : comboKey) + '" 的全部默认参数？')) {
    delete PARAMS_STATE[comboKey];
    switchTab('params');
  }
}

// ============================================================
// 脚本生成
// ============================================================

function generateProductionScript(comboKey) {
  const combo = COMBOS[comboKey];
  const steps = combo.steps;

  let lines = [
    '# ============================================================',
    '# NX CAM 自动化脚本 — ' + combo.name,
    '# NX 12+ | 由 NX CAM 自动化面板生成',
    '# ============================================================',
    '"""',
    '用法：NX中打开 .prt → Ctrl+U → 选本文件 → 运行',
    '"""',
    '',
    'import NXOpen',
    'import NXOpen.CAM',
    '',
    '# ===== 铣刀 subtype（如 MILL 不行，改 MILLING_TOOL 试） =====',
    'MILL_SUBTYPE = "' + MILL_SUBTYPE + '"',
    '',
    '# ===== 用户参数 =====',
    'PART_NAME = "' + combo.desc + '"',
  ];

  steps.forEach((s, i) => {
    const internal = toolToInternal(s.tool);
    const t = TOOLS.find(x => x.name === s.tool);
    const edit = getEdit(comboKey, i);
    const dia = edit.dia !== undefined ? edit.dia : (t ? t.dia : 4.0);
    const flute = edit.flute !== undefined ? edit.flute : (t ? t.len : 10);
    const flutes = edit.flutes !== undefined ? edit.flutes : (t ? t.flutes : 2);
    const cornerR = edit.cornerR !== undefined ? edit.cornerR : (t && t.r ? t.r : 0.0);
    const millType = isMillTool(t ? t.type : '钻头');
    const pAngle = edit.pAngle !== undefined ? edit.pAngle : getPointAngle(s.tool);

    lines.push('');
    lines.push('# --- 刀具' + (i+1) + ': ' + s.name + ' (' + s.tool + ') ---');
    lines.push('NAME_' + (i+1) + '      = "' + internal + '"');
    lines.push('DIA_' + (i+1) + '       = ' + dia + '       # 直径 mm');
    lines.push('FLUTE_' + (i+1) + '     = ' + flute + '      # 刃长 mm');
    if (millType) {
      lines.push('FLUTES_' + (i+1) + '    = ' + flutes + '       # 刃数');
      lines.push('CORNER_R_' + (i+1) + ' = ' + cornerR + '     # 下圆角半径 mm');
    } else {
      lines.push('PANGLE_' + (i+1) + '    = ' + pAngle + '     # 尖角 度');
    }
  });

  lines.push('');
  lines.push('# ===== 自动化逻辑 =====');
  lines.push('');
  lines.push('def safe_find(camGroupCol, name):');
  lines.push('    try:');
  lines.push('        return camGroupCol.FindObject(name)');
  lines.push('    except NXOpen.NXException:');
  lines.push('        return None');
  lines.push('');

  lines.push('def create_drill_tool(camGroupCol, machineRoot, name, dia, flute, pangle):');
  lines.push('    """创建钻头类刀具（中心钻/钻头/倒角刀）"""');
  lines.push('    tool = camGroupCol.CreateTool(machineRoot, "drill", "DRILLING_TOOL",');
  lines.push('        NXOpen.CAM.NCGroupCollection.UseDefaultName.FalseValue, name)');
  lines.push('    builder = camGroupCol.CreateDrillStdToolBuilder(tool)');
  lines.push('    builder.TlDiameterBuilder.Value = dia');
  lines.push('    builder.TlFluteLnBuilder.Value = flute');
  lines.push('    builder.TlPointAngBuilder.Value = pangle');
  lines.push('    builder.Commit()');
  lines.push('    builder.Destroy()');
  lines.push('');

  lines.push('def create_mill_tool(camGroupCol, machineRoot, name, dia, flute, flutes, corner_r):');
  lines.push('    """创建铣刀类刀具（铣刀/飞刀/圆鼻刀/球刀）"""');
  lines.push('    tool = camGroupCol.CreateTool(machineRoot, "mill_planar", MILL_SUBTYPE,');
  lines.push('        NXOpen.CAM.NCGroupCollection.UseDefaultName.FalseValue, name)');
  lines.push('    builder = camGroupCol.CreateMillToolBuilder(tool)');
  lines.push('    builder.TlDiameterBuilder.Value = dia');
  lines.push('    builder.TlFluteLnBuilder.Value = flute');
  lines.push('    builder.TlNumFlutesBuilder.Value = flutes');
  lines.push('    builder.TlLowCorRadBuilder.Value = corner_r');
  lines.push('    builder.Commit()');
  lines.push('    builder.Destroy()');
  lines.push('');

  lines.push('def main():');
  lines.push('    theSession = NXOpen.Session.GetSession()');
  lines.push('    workPart = theSession.Parts.Work');
  lines.push('    camSetup = workPart.CAMSetup');
  lines.push('    camGroupCol = camSetup.CAMGroupCollection');
  lines.push('    camOpCol = camSetup.OperationCollection');
  lines.push('    machineRoot = camGroupCol.FindObject("GENERIC_MACHINE")');
  lines.push('');
  lines.push('    listing = theSession.ListingWindow');
  lines.push('    listing.Open()');
  lines.push('    print("  NX CAM — ' + combo.name + '")');
  lines.push('    print("  ' + combo.desc + '")');
  lines.push('');

  steps.forEach((s, i) => {
    const idx = i+1;
    const t = TOOLS.find(x => x.name === s.tool);
    const millType = isMillTool(t ? t.type : '钻头');

    lines.push('    # [' + idx + '/' + steps.length + '] ' + s.name + '：' + s.tool);
    lines.push('    print("[' + idx + '/' + steps.length + '] ' + s.name + '：' + s.tool + '")');
    lines.push('    tool_' + idx + ' = safe_find(camGroupCol, NAME_' + idx + ')');
    lines.push('    if tool_' + idx + ' is None:');
    if (millType) {
      lines.push('        create_mill_tool(camGroupCol, machineRoot, NAME_' + idx + ', DIA_' + idx + ', FLUTE_' + idx + ', FLUTES_' + idx + ', CORNER_R_' + idx + ')');
    } else {
      lines.push('        create_drill_tool(camGroupCol, machineRoot, NAME_' + idx + ', DIA_' + idx + ', FLUTE_' + idx + ', PANGLE_' + idx + ')');
    }
    lines.push('        print("       -> 创建完成")');
    lines.push('    else:');
    lines.push('        print("       -> 已存在，跳过")');
    lines.push('');
  });

  lines.push('    print("")');
  lines.push('    print("---- 创建工序 ----")');
  lines.push('');
  lines.push('    program_group = safe_find(camGroupCol, "PROGRAM") or safe_find(camGroupCol, "NC_PROGRAM")');
  lines.push('    geom_group = safe_find(camGroupCol, "WORKPIECE") or safe_find(camGroupCol, "MCS_MILL")');
  lines.push('    method_mill = safe_find(camGroupCol, "MILL_FINISH")');
  lines.push('    method_drill = safe_find(camGroupCol, "DRILL_METHOD")');
  lines.push('');

  steps.forEach((s, i) => {
    const idx = i+1;
    const isMillOp = s.type === 'face_mill' || s.type === 'cavity_mill';
    const edit = getEdit(comboKey, i);
    const spindle = edit.spindle !== undefined ? edit.spindle : s.spindle;
    const feed = edit.feed !== undefined ? edit.feed : s.feed;
    const depth = edit.depth !== undefined ? edit.depth : s.depth;

    let opT, opST;
    if (s.type === 'spot_drill')     { opT = 'drill';        opST = 'SPOT_DRILLING'; }
    else if (s.type === 'peck_drill') { opT = 'drill';        opST = 'PECK_DRILLING'; }
    else if (s.type === 'face_mill')  { opT = 'mill_planar';  opST = 'FACE_MILLING'; }
    else if (s.type === 'cavity_mill'){ opT = 'mill_contour'; opST = 'CAVITY_MILL'; }
    else                              { opT = 'drill';        opST = 'DRILLING'; }

    lines.push('    # 工序 ' + (i+1) + ': ' + s.name + '（' + s.note + '）');
    lines.push('    if safe_find(camGroupCol, "OP_' + (i+1) + '") is None:');
    lines.push('        method_group = method_mill if ' + (isMillOp ? 'True' : 'False') + ' else method_drill');
    lines.push('        if method_group is None: method_group = safe_find(camGroupCol, "METHOD")');
    lines.push('        op = camOpCol.Create(program_group, method_group, tool_' + idx + ', geom_group,');
    lines.push('            "' + opT + '", "' + opST + '",');
    lines.push('            NXOpen.CAM.OperationCollection.UseDefaultName.FalseValue, "OP_' + (i+1) + '")');
    lines.push('        try:');
    if (s.type === 'face_mill') {
      lines.push('            b = camOpCol.CreateFaceMillingBuilder(op)');
    } else if (s.type === 'cavity_mill') {
      lines.push('            b = camOpCol.CreateCavityMillingBuilder(op)');
    } else {
      lines.push('            b = camOpCol.CreatePointToPointBuilder(op)');
    }
    lines.push('            b.FeedsBuilder.SpindleRpmBuilder.Value = ' + spindle);
    lines.push('            b.FeedsBuilder.FeedCutBuilder.Value = ' + feed);
    lines.push('            try:');
    lines.push('                b.HoleDepth.Value = ' + depth);
    lines.push('            except Exception:');
    lines.push('                pass');
    lines.push('            b.Commit()');
    lines.push('            b.Destroy()');
    lines.push('            print("       -> 工序创建完成 (S' + spindle + ' F' + feed + ' 深' + depth + ')")');
    lines.push('        except Exception as e:');
    lines.push('            print("       !! Builder 设置失败：" + str(e))');
    lines.push('    else:');
    lines.push('        print("       -> 工序已存在，跳过")');
    lines.push('');
  });

  lines.push('    print("")');
  lines.push('    print("  ✔ ' + steps.length + ' 把刀具 + ' + steps.length + ' 个工序已就绪")');
  lines.push('    print("  下一步：双击每个工序，指定孔/面（几何体）")');
  lines.push('    print("  工序导航器 -> 机床视图 可查看")');
  lines.push('    listing.Close()');
  lines.push('');
  lines.push('if __name__ == "__main__":');
  lines.push('    main()');

  return lines.join('\n');
}

function setParamCombo(key) {
  selectedCombo = key;
  switchTab('params');
}

function renderParams() {
  const combo = COMBOS[selectedCombo];

  const comboBtns = Object.entries(COMBOS).map(([k,c]) => `
    <button class="btn" style="margin-right:6px;${k===selectedCombo?'background:var(--accent-light);border-color:var(--accent);':''}"
      onclick="setParamCombo('${k}')">${c.name.split('：')[0]}</button>
  `).join('');

  const rows = combo.steps.map((s, i) => {
    const t = TOOLS.find(x => x.name === s.tool);
    const millType = isMillTool(t ? t.type : '钻头');
    const edit = getEdit(selectedCombo, i);
    const dia     = edit.dia     !== undefined ? edit.dia     : (t ? t.dia : 4.0);
    const flute   = edit.flute   !== undefined ? edit.flute   : (t ? t.len : 10);
    const flutes  = edit.flutes  !== undefined ? edit.flutes  : (t ? t.flutes : 2);
    const cornerR = edit.cornerR !== undefined ? edit.cornerR : (t && t.r ? t.r : 0.0);
    const pAngle  = edit.pAngle  !== undefined ? edit.pAngle  : getPointAngle(s.tool);
    const spindle = edit.spindle !== undefined ? edit.spindle : s.spindle;
    const feed    = edit.feed    !== undefined ? edit.feed    : s.feed;
    const depth   = edit.depth   !== undefined ? edit.depth   : s.depth;

    const inp = (field, val, step) => `
      <input type="number" step="${step}" style="width:70px;padding:4px 8px;border:0.5px solid var(--border);border-radius:6px;font-size:12px"
        value="${val}" onchange="saveParam('${selectedCombo}', ${i}, '${field}', this.value)">`;

    return `
      <tr>
        <td style="font-weight:500">${i+1}. ${s.name}</td>
        <td style="color:var(--text-secondary)">${s.tool}</td>
        <td>${inp('dia', dia, '0.1')} mm</td>
        <td>${inp('flute', flute, '0.1')} mm</td>
        ${millType
          ? `<td>${inp('flutes', flutes, '1')} 刃</td><td>${inp('cornerR', cornerR, '0.1')} mm</td>`
          : `<td>${inp('pAngle', pAngle, '1')} °</td><td>—</td>`}
        <td>S ${inp('spindle', spindle, '10')}</td>
        <td>F ${inp('feed', feed, '10')}</td>
        <td>深${inp('depth', depth, '0.1')}</td>
      </tr>`;
  }).join('');

  return `
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px">
        <h2 style="margin:0">参数设置 — ${combo.name}</h2>
        <div>
          ${comboBtns}
          <button class="btn" onclick="resetParams('${selectedCombo}')" style="margin-left:8px">↩ 恢复默认</button>
          <button class="btn btn-primary" onclick="downloadScript()" style="margin-left:8px">⬇ 下载 .py</button>
        </div>
      </div>
      <p style="color:var(--text-secondary);margin-bottom:12px">
        直接改数值，改完立即生效。<br>
        去「脚本预览」可看新脚本，或点「下载 .py」直接保存 → 拷贝到工厂 → NX Ctrl+U 运行。
      </p>
      <div style="overflow-x:auto">
        <table>
          <thead>
            <tr>
              <th>工序</th><th>刀具</th><th>直径</th><th>刃长</th>
              <th>刃数/尖角</th><th>圆角R</th><th>转速S</th><th>进给F</th><th>深度</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    </div>
  `;
}

function downloadScript() {
  const code = generateProductionScript(selectedCombo);
  const filename = `nx_cam_${selectedCombo}.py`;
  const blob = new Blob([code], {type: 'text/plain'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function switchTab(tab) {
  document.querySelectorAll('.tab').forEach(t => {
    t.classList.toggle('active', t.getAttribute('data-tab') === tab);
  });

  const content = document.getElementById('tab-content');
  if (tab === 'tools')     content.innerHTML = renderTools();
  else if (tab === 'combos')  content.innerHTML = renderCombos();
  else if (tab === 'rules')   content.innerHTML = renderRules();
  else if (tab === 'params')  content.innerHTML = renderParams();
  else if (tab === 'script')  content.innerHTML = renderScriptPreview();
}

// ============================================================
// 初始化
// ============================================================
renderStats();
document.getElementById('tab-content').innerHTML = renderCombos();
document.getElementById('genTime').textContent = new Date().toLocaleString('zh-CN');
</script>
</body>
</html>'''

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'OK: {len(html)} bytes -> {OUT}')
