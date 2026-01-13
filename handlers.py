import bpy
import os
import time
import subprocess
import sys
from pathlib import Path


# Constants
TEMP_DIR = os.path.join(os.environ.get("TEMP", "/tmp"), "HERA")
HEARTBEAT_FILE = os.path.join(TEMP_DIR, "heartbeat.txt")
STATUS_FILE = os.path.join(TEMP_DIR, "status.txt")
WATCHDOG_PROCESS = None


def ensure_temp_dir():
    """Create the temp directory if it doesn't exist."""
    try:
        Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"[HERA] Failed to create temp directory: {e}")


def update_heartbeat():
    """Write current timestamp to heartbeat file."""
    try:
        ensure_temp_dir()
        with open(HEARTBEAT_FILE, "w") as f:
            f.write(str(time.time()))
    except Exception as e:
        print(f"[HERA] Failed to update heartbeat: {e}")


def set_status(status):
    """Write render status to status file."""
    try:
        ensure_temp_dir()
        with open(STATUS_FILE, "w") as f:
            f.write(status)
    except Exception as e:
        print(f"[HERA] Failed to set status: {e}")


def launch_watchdog():
    """Launch the watchdog script as a detached process."""
    global WATCHDOG_PROCESS
    
    prefs = bpy.context.preferences.addons[__package__].preferences
    if not prefs.enable_watchdog:
        return
    
    try:
        ensure_temp_dir()
        set_status("RENDERING")
        
        watchdog_path = os.path.join(os.path.dirname(__file__), "watchdog.py")
        blender_pid = os.getpid()
        
        # Use Blender's Python interpreter and detach the process
        python_exe = sys.executable
        WATCHDOG_PROCESS = subprocess.Popen(
            [python_exe, watchdog_path, str(blender_pid), TEMP_DIR],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.DETACHED_PROCESS if sys.platform == "win32" else 0
        )
        print(f"[HERA] Watchdog launched with PID {WATCHDOG_PROCESS.pid}")
    except Exception as e:
        print(f"[HERA] Failed to launch watchdog: {e}")


@bpy.app.handlers.persistent
def render_init(scene):
    """Handler called at the start of a render."""
    print("[HERA] Render started")
    launch_watchdog()


@bpy.app.handlers.persistent
def render_stats(scene):
    """Handler called for each render tile/sample completion."""
    update_heartbeat()


@bpy.app.handlers.persistent
def render_complete(scene):
    """Handler called when render completes successfully."""
    print("[HERA] Render completed")
    set_status("COMPLETED")


@bpy.app.handlers.persistent
def render_cancel(scene):
    """Handler called when render is cancelled."""
    print("[HERA] Render cancelled")
    set_status("CANCELLED")


def register_handlers():
    """Register all persistent handlers."""
    bpy.app.handlers.render_init.append(render_init)
    bpy.app.handlers.render_stats.append(render_stats)
    bpy.app.handlers.render_complete.append(render_complete)
    bpy.app.handlers.render_cancel.append(render_cancel)


def unregister_handlers():
    """Unregister all persistent handlers."""
    bpy.app.handlers.render_init.remove(render_init)
    bpy.app.handlers.render_stats.remove(render_stats)
    bpy.app.handlers.render_complete.remove(render_complete)
    bpy.app.handlers.render_cancel.remove(render_cancel)
