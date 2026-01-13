# HERA Development Setup

## Python Dependencies

### For Blender's Python Environment
```bash
# Run this in Blender's Python interpreter
# Navigate to Blender's Python directory and run:
python -m pip install psutil
```

## File Structure

```
HERA/
├── __init__.py              # Main addon file
├── handlers.py              # Render event handlers
├── preferences.py           # Addon preferences UI
├── watchdog.py              # External monitoring script
├── monitor.py               # Alert system (MessageBox + Sound)
├── sounds/                  # Sound alert files
│   ├── success.wav          # (Add custom sound)
│   ├── error.wav            # (Add custom sound)
│   └── stopped.wav          # (Add custom sound)
├── README.md                # User documentation
└── LICENSE                  # MIT License
```

## Setup Instructions

1. **Install addon:**
   - Copy `HERA` folder to Blender addons directory

2. **Install psutil:**
   - Find your Blender Python: `Edit > Preferences > System > Python`
   - Open terminal/PowerShell
   - Run: `<blender_python_path>/python -m pip install psutil`

3. **Add sound files:**
   - Place custom .wav files in `sounds/` directory
   - Or leave empty to use system beep fallback

4. **Enable addon:**
   - Edit > Preferences > Add-ons > Enable HERA

## Deployment Checklist

- [x] Core addon registration
- [x] Render event handlers
- [x] Filesystem communication
- [x] Watchdog monitoring loop
- [x] Alert system (MessageBox + Sound)
- [x] Preferences panel
- [x] Documentation
- [ ] Custom sound files (user-provided)
- [ ] Testing across Blender versions 3.0-4.x
- [ ] Release packaging
