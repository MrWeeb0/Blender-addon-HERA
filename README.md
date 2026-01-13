# HERA - Blender Render Watchdog

## Quick Start

1. **Install the addon:**
   - Copy the `HERA` folder to your Blender addons directory:
     - Windows: `C:\Users\<YourUsername>\AppData\Roaming\Blender Foundation\Blender\<version>\scripts\addons`
     - macOS: `/Users/<YourUsername>/Library/Application Support/Blender/<version>/scripts/addons`
     - Linux: `~/.config/blender/<version>/scripts/addons`

2. **Enable the addon:**
   - Open Blender
   - Go to Edit > Preferences > Add-ons
   - Search for "HERA"
   - Check the box to enable

3. **Configure preferences:**
   - Freeze Threshold: Set detection time (30-300 seconds)
   - Sound Alerts: Toggle audio feedback
   - Custom Sound: Point to your own .wav files

4. **Start rendering:**
   - Press F12 (Image) or Ctrl+F12 (Animation)
   - The watchdog will automatically start monitoring
   - If a crash or freeze is detected, you'll get an alert

## Features

✅ **Automatic Monitoring** - Launches on F12 / Ctrl+F12  
✅ **Crash Detection** - Detects if Blender crashes mid-render  
✅ **Freeze Detection** - Alerts if render stalls for N seconds  
✅ **Always-on-Top Alerts** - Windows MessageBox that interrupts other windows  
✅ **Audio Feedback** - Customizable .wav sounds  
✅ **Detached Process** - Watchdog runs independently, no terminal window  
✅ **Zero Dependencies** - Uses only Python standard library (except psutil)

## How It Works

### Architecture

**Blender Addon (Internal)**
- Registers render event handlers (init, stats, complete, cancel)
- Writes heartbeat timestamps to `%TEMP%/HERA/heartbeat.txt`
- Launches external watchdog script on render start

**Watchdog Script (External, Detached Process)**
- Monitors Blender process PID
- Checks heartbeat file timestamps every 5 seconds
- Triggers alerts on crash or freeze detection

**Communication**
- Filesystem signals: `heartbeat.txt`, `status.txt` in `%TEMP%/HERA/`
- No IPC overhead, cross-platform compatible

### Triple-Check Detection

1. **Process Check**: Is Blender still running?
2. **Heartbeat Check**: Has the heartbeat updated in the last N seconds?
3. **Status Check**: Has render completed successfully?

## Installation Requirements

- Windows 10/11
- Blender 3.0+
- Python 3.6+ (Blender's bundled Python)
- `psutil` package (run: `pip install psutil` in Blender's Python)

## MVP Scope

This is a minimum viable product covering:
- ✅ Phase 1: Core addon heartbeat system
- ✅ Phase 2: Watchdog monitoring with alerts
- ✅ Phase 3: Integration bridge (subprocess, detached process)

Planned for future releases:
- [ ] Phase 4: Advanced cleanup and false-positive handling
- [ ] Phase 5: Documentation and release automation

## Troubleshooting

**Watchdog not starting?**
- Check that `psutil` is installed in Blender's Python
- Verify temp directory permissions

**No alerts appearing?**
- Enable sound alerts in preferences
- Check that sound files exist in `sounds/` directory

**Terminal window appearing?**
- This shouldn't happen with `DETACHED_PROCESS` flag
- If it does, check Windows event logs

## License

MIT License - See LICENSE file for details
