"""
Monitor - Notification System
Handles Windows MessageBox alerts and audio playback
"""

import ctypes
import winsound
import os
from pathlib import Path


def trigger_alert(alert_type):
    """
    Trigger an alert notification.
    
    Args:
        alert_type: "CRASH", "FREEZE", or "SUCCESS"
    """
    title = "HERA Render Watchdog"
    
    if alert_type == "CRASH":
        message = "⚠️ Blender render crashed!"
        sound_file = "error.wav"
    elif alert_type == "FREEZE":
        message = "❄️ Blender render appears frozen!"
        sound_file = "error.wav"
    elif alert_type == "SUCCESS":
        message = "✓ Blender render completed successfully!"
        sound_file = "success.wav"
    else:
        message = "Unknown alert"
        sound_file = None
    
    # Show Windows MessageBox (Always on Top with MB_SYSTEMMODAL)
    show_message_box(message, title)
    
    # Play audio alert
    if sound_file:
        play_sound(sound_file)


def show_message_box(message, title):
    """Display a Windows MessageBox with Always-on-Top flag."""
    try:
        MB_OK = 0
        MB_ICONWARNING = 0x30
        MB_SYSTEMMODAL = 0x1000  # Always on top
        
        ctypes.windll.user32.MessageBoxW(
            None,
            message,
            title,
            MB_OK | MB_ICONWARNING | MB_SYSTEMMODAL
        )
    except Exception as e:
        print(f"[Monitor] Failed to show MessageBox: {e}")


def play_sound(sound_name):
    """Play a .wav sound file."""
    try:
        # Get the addon directory
        addon_dir = os.path.dirname(__file__)
        sounds_dir = os.path.join(addon_dir, "sounds")
        sound_path = os.path.join(sounds_dir, sound_name)
        
        if os.path.exists(sound_path):
            winsound.PlaySound(sound_path, winsound.SND_FILENAME)
        else:
            # Fallback to system sound if custom file not found
            print(f"[Monitor] Sound file not found: {sound_path}")
            winsound.Beep(1000, 500)
    except Exception as e:
        print(f"[Monitor] Failed to play sound: {e}")
