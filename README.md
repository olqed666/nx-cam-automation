# NX CAM 自动化

一个可重用的西门子 NX CAM 自动化框架。定义你的刀具和工艺组合，生成可直接运行的 Python 脚本，自动在 NX 中创建所有刀具和操作。

## 功能特性

代替手动点击 NX 创建刀具、设置转速进给、配置工序：
1. 在浏览器打开 web/index.html
2. 配置你的刀具和工艺组合（或导入 JSON 配置）
3. 调整参数（直径、转速、深度等）
4. 下载 .py 脚本
5. 复制到工厂电脑，在 NX 按 Ctrl+U 运行
6. 脚本自动创建所有刀具和工序
7. 你只需要双击每个工序，指定孔/面（NX 唯一需要手动的步骤）

## 项目结构


nx-cam-automation/
├── src/                      # 核心代码目录
│   └── nx_cam_engine.py      # NX CAM 自动化核心引擎
├── config/                   # 配置目录
│   └── example_config.py     # 示例配置（替换为你自己工厂的刀具/工艺）
├── web/                      # Web 前端（汉化版）
│   ├── index.html            # 前端入口，全中文界面
│   ├── style.css             # 样式
│   └── app.js                # 数据渲染和脚本生成逻辑
├── docs/                     # 文档目录
│   └── NX12_CAM_API_参考.md  # NX CAM API 中文参考文档
├── tests/                    # 调试脚本
│   └── test_mill_api.py      # 调试 NX 铣刀 API
├── run_nx_cam.py             # 快速启动脚本
└── README.md                 # 中文使用说明文档

## 使用指南

### Web 前端（推荐）

在任意浏览器打开：web/index.html，可视化配置刀具和工艺，一键下载可执行脚本，无需编程。

### 直接用 NX 脚本

1. 编辑 
un_nx_cam.py 或创建你的配置
2. 复制到工厂电脑
3. 在 NX 里按 Ctrl+U，选择 .py 文件运行
4. 窗口输出进度

## 配置格式

- 刀具：JSON 结构，定义名称、类型、直径、长度等
- 工序：定义名称、类型、用哪个刀具、转速、进给、深度

完整说明见 config/example_config.py。

## 支持的工序类型

| 类型           | 说明               |
|----------------|--------------------|
| spot_drill   | 中心钻/点窝         |
| drill        | 标准钻孔           |
| peck_drill   | 深孔啄钻           |
| chamfer      | 倒角/去毛刺         |
| ace_mill    | 面铣               |
| planar_mill  | 平面铣             |
| cavity_mill  | 型腔铣             |
| zlevel       | 等高轮廓铣         |

## NX 注意事项


1. 空白零件需先手动进入加工模块，保存后再运行脚本
2. 脚本运行后，每个工序需要手动指定孔/面

## 许可证

MIT
