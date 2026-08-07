# NX CAM Automation

A reusable, open-source automation framework for Siemens NX CAM. Define your tools and process combinations, then generate ready-to-run Python scripts that create all tools and operations in NX automatically.

## What it does

Instead of spending 15 minutes manually clicking in NX to create tools, set speeds/feeds, and configure operations, you:

1. Open `web/index.html` in a browser
2. Configure your tools and process combos (or import a JSON config)
3. Tweak parameters if needed
4. Download a `.py` script
5. Run it in NX via `Ctrl+U`
6. The script creates all tools and operations automatically
7. You just double-click each operation to assign holes/faces (the one manual step NX requires)

## Project structure

```
nx-cam-automation/
├── src/
│   └── nx_cam_engine.py      # Core engine: tool creation, operation creation, batch runner
├── config/
│   └── example_config.py     # Example configuration (replace with your own factory data)
├── web/
│   ├── index.html            # Web frontend entry point
│   ├── style.css             # Styles
│   └── app.js                # Data, rendering, and script generation logic
├── docs/
│   └── NX12_CAM_API_参考.md   # NX CAM API reference (Chinese)
├── tests/
│   └── test_mill_api.py      # Debug script to test mill tool API on your NX version
├── run_nx_cam.py             # Quick-start runner (edit config, Ctrl+U in NX)
└── README.md
```

## Quick start

### Web frontend (recommended)

```bash
# Open in any browser
open web/index.html
```

Configure tools and combos in the UI, download scripts. No install needed.

### Direct NX script

1. Edit `run_nx_cam.py` or create your own config
2. Copy to factory PC
3. In NX: `Ctrl+U` -> select the `.py` file
4. The Listing Window shows progress

## Configuration format

Tools:
```python
{"name": "ZDD4",   "type": "drill", "diameter": 4.0,  "flute_length": 4,  "point_angle": 90}
{"name": "XD10R",  "type": "mill",  "diameter": 10.0, "flute_length": 23, "flutes": 2}
```

Operations:
```python
{"name": "OP_SPOT",  "op_type": "spot_drill", "tool_name": "ZDD4",  "spindle": 1500, "feed": 150, "depth": -2.0}
{"name": "OP_DRILL", "op_type": "peck_drill", "tool_name": "ZD5.2", "spindle": 1100, "feed": 150, "depth": -20.0}
```

See `config/example_config.py` and `src/nx_cam_engine.py` for full API docs.

## Supported operation types

| op_type       | Description              | NX type        | NX subtype       |
|---------------|--------------------------|----------------|------------------|
| `spot_drill`  | Center drill / spot      | `drill`        | `SPOT_DRILLING`  |
| `drill`       | Standard drill (G81)     | `drill`        | `DRILLING`       |
| `peck_drill`  | Peck drill (G83)         | `drill`        | `PECK_DRILLING`  |
| `chamfer`     | Chamfer / deburring      | `drill`        | `DRILLING`       |
| `face_mill`   | Face milling             | `mill_planar`  | `FACE_MILLING`   |
| `planar_mill` | Planar milling           | `mill_planar`  | `PLANAR_MILL`    |
| `cavity_mill` | Cavity milling           | `mill_contour` | `CAVITY_MILL`    |
| `zlevel`      | Z-level profile          | `mill_contour` | `ZLEVEL_PROFILE` |

## Important NX gotchas

1. **Tool names must be ASCII** — no Chinese characters, no slashes. Use `ZDD4` not `中心钻/4`.
2. **`FindObject` throws, does not return `None`** — always wrap in `try/except`.
3. **Mill tool type is `mill_planar`**, not `mill`.
4. **Blank `.prt` files have no CAM environment** — manually enter `Start > Manufacturing > OK` once, then save.
5. **Operations need manual geometry assignment** — after script runs, double-click each op and assign holes/faces.

## Requirements

- Siemens NX 12.0+ (tested on 12.0.2.9)
- NXOpen Python API (bundled with NX)
- No additional Python packages needed (runs inside NX's Python)

## License

MIT

## Credits

Developed for factory CNC automation. The web frontend and engine are designed to be generic — plug in your own tool library and process combos.
