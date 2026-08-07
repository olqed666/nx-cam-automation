# NX 12 CAM Python API 参考文档

> 从 `D:\Program Files\Siemens\NX 12.0\UGOPEN\NXOpen\` C++ 头文件提取
> Python NXOpen 是 C++ API 的直接包装，类名/方法名完全一致

## 1. 获取 CAM 环境

```python
import NXOpen
import NXOpen.CAM

theSession = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work
camSetup = workPart.CAMSetup
camGroupCol = camSetup.CAMGroupCollection       # 刀具/组集合
camOpCol = camSetup.OperationCollection          # 工序集合
```

## 2. 刀具创建 API

### 2.1 钻头类（中心钻/钻头/倒角刀）

```python
# 1. 创建刀具对象
tool = camGroupCol.CreateTool(
    machineRoot,              # 父组：camGroupCol.FindObject("GENERIC_MACHINE")
    "drill",                  # type
    "DRILLING_TOOL",          # subtype
    NXOpen.CAM.NCGroupCollection.UseDefaultName.FalseValue,
    "ZD5.2"                   # 刀具名（ASCII，不能有中文/斜杠）
)

# 2. 获取 Builder
builder = camGroupCol.CreateDrillStdToolBuilder(tool)

# 3. 设置参数
builder.TlDiameterBuilder.Value = 5.2        # 直径
builder.TlFluteLnBuilder.Value = 20          # 刃长
builder.TlPointAngBuilder.Value = 118        # 尖角（中心钻90, 钻头118, 倒角90）
builder.TlTipDiameterBuilder.Value = 0       # 尖端直径（倒角刀用）
builder.TlIncludedAngBuilder.Value = 118     # 包含角
builder.TlNumFlutesBuilder.Value = 2         # 刃数

# 4. 提交
builder.Commit()
builder.Destroy()
```

### 2.2 铣刀类（铣刀/飞刀/圆鼻刀/球刀/精铣刀）

```python
# 1. 创建刀具对象 — ⚠️ type 是 "mill_planar"（不是 "mill"！）
# 实际 NX 12 模板的 type 命名是 "mill_planar"
tool = camGroupCol.CreateTool(
    machineRoot,
    "mill_planar",            # ← 注意：不是 "mill"
    "MILL",                   # subtype（候选: MILL / BALL_MILL / CHAMFER_MILL / MILLING_TOOL）
    NXOpen.CAM.NCGroupCollection.UseDefaultName.FalseValue,
    "XD10R"
)

# 2. 获取 Builder — CreateMillToolBuilder
builder = camGroupCol.CreateMillToolBuilder(tool)

# 3. 设置参数
builder.TlDiameterBuilder.Value = 10.0       # 直径
builder.TlFluteLnBuilder.Value = 23          # 刃长
builder.TlNumFlutesBuilder.Value = 2         # 刃数
builder.TlLowCorRadBuilder.Value = 0.0       # 下圆角半径（圆鼻刀/飞刀的 R 值）
builder.TlUpCorRadBuilder.Value = 0.0        # 上圆角半径
builder.TlHeightBuilder.Value = 50           # 总长度
builder.TlShankDiaBuilder.Value = 10.0       # 柄径
builder.TlTaperAngBuilder.Value = 0.0        # 锥角
builder.SetTlDirection(NXOpen.CAM.MillingToolBuilder.ToolDirectionTypes.ToolDirectionTypesClw)  # 顺时针

# 4. 提交
builder.Commit()
builder.Destroy()
```

### 2.3 其他钻头类刀具 Builder

| 刀具类型 | Builder 方法 |
|---------|-------------|
| 标准钻头 | `CreateDrillStdToolBuilder` |
| 中心钻 | `CreateDrillSpotdrillToolBuilder` |
| 倒角刀 | `CreateDrillCtskToolBuilder` |
| 铰刀 | `CreateDrillReamerToolBuilder` |
| 锪刀 | `CreateDrillCounterboreToolBuilder` / `CreateDrillSpotfaceToolBuilder` |
| 丝锥 | `CreateDrillTapToolBuilder` |
| 阶梯钻 | `CreateDrillStepToolBuilder` |
| 镗刀 | `CreateDrillBoreToolBuilder` |
| 螺纹铣 | `CreateDrillThreadMillToolBuilder` |

### 2.4 其他铣刀类刀具 Builder

| 刀具类型 | Builder 方法 |
|---------|-------------|
| 铣刀 | `CreateMillToolBuilder` |
| 成型铣刀 | `CreateMillFormToolBuilder` |
| T 型刀 | `CreateTToolBuilder` |
| 螺纹刀 | `CreateThreadToolBuilder` |
| 槽刀 | `CreateGrooveToolBuilder` |
| 鼓形刀 | `CreateBarrelToolBuilder` |
| 定制刀 | `CreateFormToolBuilder` |
| 通用刀 | `CreateGenericToolBuilder` |
| 探针 | `CreateProbeToolBuilder` |

## 3. 安全查找对象

```python
def safe_find(camGroupCol, name):
    """FindObject 不存在时抛异常，不是返回 None"""
    try:
        return camGroupCol.FindObject(name)
    except NXOpen.NXException:
        return None
```

## 4. 工序创建 API

### 4.1 创建工序（通用方法）

```python
# 需要找到4个父组
programGroup = camGroupCol.FindObject("PROGRAM")        # 程序组
methodGroup = camGroupCol.FindObject("MILL_ROUGH")      # 方法组（MILL_ROUGH/MILL_SEMI_FINISH/MILL_FINISH/DRILL_METHOD）
toolGroup = camGroupCol.FindObject("ZD5.2")             # 刀具组（刚创建的刀具名）
geometryGroup = camGroupCol.FindObject("WORKPIECE")     # 几何体组（WORKPIECE/MCS_MILL）

# 创建工序
operation = camOpCol.Create(
    programGroup,           # 父程序组
    methodGroup,            # 父方法组
    toolGroup,              # 父刀具组
    geometryGroup,          # 父几何体组
    "drill",                # type（见下方对照表）
    "DRILLING",             # subtype（见下方对照表）
    NXOpen.CAM.OperationCollection.UseDefaultName.FalseValue,
    "OP_DRILL_1"            # 工序名
)
```

### 4.2 工序 Builder

创建工序后，用对应 Builder 设置参数：

```python
# 钻孔工序（点对点）
builder = camOpCol.CreatePointToPointBuilder(operation)

# 面铣工序
builder = camOpCol.CreateFaceMillingBuilder(operation)

# 型腔铣工序
builder = camOpCol.CreateCavityMillingBuilder(operation)

# 平面铣工序
builder = camOpCol.CreatePlanarMillingBuilder(operation)

# 等高铣工序
builder = camOpCol.CreateZlevelMillingBuilder(operation)

# 倒角铣工序
builder = camOpCol.CreateChamferMillingBuilder(operation)

# 刻字工序
builder = camOpCol.CreateEngravingBuilder(operation)

# 插铣工序
builder = camOpCol.CreatePlungeMillingBuilder(operation)

# 孔钻削工序（基于特征）
builder = camOpCol.CreateHoleDrillingBuilder(operation)

# 孔加工工序（基于特征）
builder = camOpCol.CreateHoleMakingBuilder(operation)

# 设置参数后提交
builder.Commit()
builder.Destroy()
```

### 4.3 工序参数设置（已确认 API）

```python
# 转速（主轴）
builder.FeedsBuilder.SpindleRpmBuilder.Value = 1500

# 切削进给
builder.FeedsBuilder.FeedCutBuilder.Value = 150

# 孔深度（钻孔类工序）
builder.HoleDepth.Value = -20

# 钻孔循环类型（PointToPointBuilder.CycleTypes 枚举）
#  G83啄钻 → CycleTypesPeckDrill
#  G81标准 → CycleTypesStandardDrill
#  深孔    → CycleTypesStandardDrillDeep
# 注：具体设置方法待实测，NX 12 可能通过 Cycle 对象 SetCycleType("PECK_DRILL")
```

### 4.3 type/subtype 对照表

| 工序类型 | type | subtype |
|---------|------|---------|
| 钻孔（点对点） | `drill` | `DRILLING` |
| 面铣 | `mill_planar` | `FACE_MILLING` |
| 平面铣 | `mill_planar` | `PLANAR_MILL` |
| 型腔铣 | `mill_contour` | `CAVITY_MILL` |
| 等高轮廓铣 | `mill_contour` | `ZLEVEL_PROFILE` |
| 固定轴轮廓铣 | `mill_contour` | `FIXED_CONTOUR` |
| 刻字 | `mill_planar` | `TEXT_ENGRAVING` |
| 插铣 | `mill_contour` | `PLUNGE_MILLING` |

> **注意**：以上 type/subtype 为 NX 常见值，实际可能因模板配置不同而异。
> 建议在 NX 中录一段 Journal 确认实际值。

## 5. 默认组查找

```python
# 机床根（刀具的父节点）
machineRoot = camGroupCol.FindObject("GENERIC_MACHINE")

# 程序根
programRoot = camGroupCol.FindObject("PROGRAM")

# 几何体根
mcsRoot = camGroupCol.FindObject("MCS_MILL")
workpiece = camGroupCol.FindObject("WORKPIECE")

# 方法根
methodRough = camGroupCol.FindObject("MILL_ROUGH")
methodSemiFinish = camGroupCol.FindObject("MILL_SEMI_FINISH")
methodFinish = camGroupCol.FindObject("MILL_FINISH")
methodDrill = camGroupCol.FindObject("DRILL_METHOD")
methodMillFinish = camGroupCol.FindObject("MILL_FINISH")
```

## 6. 刀具参数对照表

### 钻头类（DrillToolBuilder 继承自 MillingToolBuilder）

| 参数 | Builder 属性 | 说明 |
|------|-------------|------|
| 直径 | `TlDiameterBuilder.Value` | 刀具直径 |
| 刃长 | `TlFluteLnBuilder.Value` | 螺旋槽长度 |
| 尖角 | `TlPointAngBuilder.Value` | 钻尖角度（中心钻90, 钻头118） |
| 尖端直径 | `TlTipDiameterBuilder.Value` | 倒角刀尖端直径 |
| 包含角 | `TlIncludedAngBuilder.Value` | |
| 刃数 | `TlNumFlutesBuilder.Value` | |
| 总长 | `TlHeightBuilder.Value` | |
| 柄径 | `TlShankDiaBuilder.Value` | |

### 铣刀类（MillingToolBuilder）

| 参数 | Builder 属性 | 说明 |
|------|-------------|------|
| 直径 | `TlDiameterBuilder.Value` | 刀具直径 |
| 刃长 | `TlFluteLnBuilder.Value` | 切削刃长度 |
| 刃数 | `TlNumFlutesBuilder.Value` | |
| 下圆角半径 | `TlLowCorRadBuilder.Value` | 圆鼻刀/飞刀的 R 值 |
| 上圆角半径 | `TlUpCorRadBuilder.Value` | |
| 总长 | `TlHeightBuilder.Value` | |
| 柄径 | `TlShankDiaBuilder.Value` | |
| 锥角 | `TlTaperAngBuilder.Value` | |
| 旋转方向 | `SetTlDirection(...)` | CLW/CCLW |

### 球刀特殊处理

球刀的 corner_r = 直径/2，用 MillingToolBuilder 创建时设 `TlLowCorRadBuilder.Value = dia/2`

## 7. InheritableDoubleBuilder 用法

很多参数是 InheritableDoubleBuilder 类型，设置方式：

```python
builder.TlDiameterBuilder.Value = 10.0        # 设置值
val = builder.TlDiameterBuilder.Value          # 读取值
```

## 8. 已验证的 API（NX 12.0.2.9 实测）

| 操作 | API | 状态 |
|------|-----|------|
| 获取机床根组 | `camGroupCol.FindObject("GENERIC_MACHINE")` | ✅ 已验证 |
| 创建钻头刀具 | `camGroupCol.CreateTool(parent, "drill", "DRILLING_TOOL", ...)` | ✅ 已验证 |
| 钻头 Builder | `camGroupCol.CreateDrillStdToolBuilder(tool)` | ✅ 已验证 |
| 设置钻头直径 | `builder.TlDiameterBuilder.Value = dia` | ✅ 已验证 |
| 提交创建 | `builder.Commit() → builder.Destroy()` | ✅ 已验证 |
| 创建铣刀刀具 | `camGroupCol.CreateTool(parent, "mill_planar", "MILL", ...)` | ⏳ 待张工验证 |
| 铣刀 Builder | `camGroupCol.CreateMillToolBuilder(tool)` | ⏳ 待张工验证 |
| 设置铣刀圆角 | `builder.TlLowCorRadBuilder.Value = r` | ⏳ 待张工验证 |
| 创建工序 | `camOpCol.Create(prog, method, tool, geom, type, subtype, ...)` | ⏳ 待张工验证 |

## 9. CreateTool type/subtype 对照表（已确认）

### 铣刀类（type="mill_planar"）

| subtype | 用途 |
|---------|------|
| `MILL` | 通用铣刀（直柄平底） |
| `BALL_MILL` | 球刀 |
| `CHAMFER_MILL` | 倒角铣刀（不是钻头） |
| `SPHERICAL_MILL` | 球形铣刀 |
| `T_CUTTER` | T 型刀 |
| `BARREL` | 鼓形刀 |
| `MILLING_TOOL` | NX 早期版本通用铣刀（NX 12 可能已废弃） |

### 钻头类（type="drill"）

| subtype | 用途 |
|---------|------|
| `DRILLING_TOOL` | 标准钻头（已验证） |
| `COUNTERSINKING_TOOL` | 沉头钻（倒角钻） |
| `COUNTERBORING_TOOL` | 锪孔钻 |
| `SPOTDRILLING_TOOL` | 中心钻 |
| `REAMER` | 铰刀 |
| `TAP` | 丝锥 |

## 10. 工序 type/subtype 对照表（从模板 .prt 提取）

### 钻孔类（type="drill"）— 从 drill.prt 提取

| subtype | 用途 |
|---------|------|
| `SPOT_DRILLING` | 中心钻（点窝） |
| `DRILLING` | 标准钻孔（G81） |
| `PECK_DRILLING` | 啄钻（G83，深孔） |
| `BREAKCHIP_DRILLING` | 断屑钻 |

### 铣削类（type="mill_planar"）— 从 mill_planar.prt 提取

| subtype | 用途 |
|---------|------|
| `FACE_MILLING` | 面铣（光平面） |
| `PLANAR_MILL` | 平面铣 |
| `THREAD_MILLING` | 螺纹铣 |

### 型腔铣（type="mill_contour"）

| subtype | 用途 |
|---------|------|
| `CAVITY_MILL` | 型腔铣（开粗/半精/精光） |

> ⚠️ 以上工序 subtype 从 NX 12 模板 .prt 提取，**待张工实测确认**

## 9. 文件路径

| 文件 | 路径 |
|------|------|
| NX 安装目录 | `D:\Program Files\Siemens\NX 12.0` |
| API 头文件 | `D:\Program Files\Siemens\NX 12.0\UGOPEN\NXOpen\` |
| Python 示例 | `D:\Program Files\Siemens\NX 12.0\UGOPEN\SampleNXOpenApplications\Python\` |
| UGII_BASE_DIR | `D:\Program Files\Siemens\NX 12.0` |
