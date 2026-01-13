"""
Monitor - External Watchdog Script
Runs as a detached process to monitor Blender render status
"""

import sys
import time
import os
import psutil
from monitor import trigger_alert


def is_process_running(pid):
    """Check if a process with given PID is still running."""
    try:
        return psutil.pid_exists(pid)
    except Exception:
        return False


def read_heartbeat(heartbeat_file):
    """Read the heartbeat timestamp from file."""
    try:
        if not os.path.exists(heartbeat_file):
            return None
        with open(heartbeat_file, "r") as f:
            content = f.read().strip()
            return float(content) if content else None
    except Exception:
        return None


def read_status(status_file):
    """Read the render status from file."""
    try:
        if not os.path.exists(status_file):
            return None
        with open(status_file, "r") as f:
            return f.read().strip()
    except Exception:
        return None


def main():
    """Main watchdog loop."""
    if len(sys.argv) < 3:
        print("Usage: watchdog.py <blender_pid> <temp_dir>")
        sys.exit(1)
    
    blender_pid = int(sys.argv[1])
    temp_dir = sys.argv[2]
    heartbeat_file = os.path.join(temp_dir, "heartbeat.txt")
    status_file = os.path.join(temp_dir, "status.txt")
    
    # Get freeze threshold (default 60 seconds)
    freeze_threshold = 60
    
    last_heartbeat_time = time.time()
    
    print(f"[HERA Watchdog] Started monitoring Blender PID {blender_pid}")
    
    while True:
        time.sleep(5)
        
        # Check 1: Is Blender process still alive?
        if not is_process_running(blender_pid):
            status = read_status(status_file)
            if status != "COMPLETED":
                print("[HERA Watchdog] Blender process crashed!")
                trigger_alert("CRASH")
            break
        
        # Check 2: Has status already been set to completed?
        status = read_status(status_file)
        if status == "COMPLETED":
            print("[HERA Watchdog] Render completed successfully")
            trigger_alert("SUCCESS")
            break
        
        if status == "CANCELLED":
            print("[HERA Watchdog] Render was cancelled")
            break
        
        # Check 3: Is the heartbeat still updating?
        heartbeat = read_heartbeat(heartbeat_file)
        if heartbeat is not None:
            last_heartbeat_time = heartbeat
        else:
            # First read, use current time
            last_heartbeat_time = time.time()
        
        time_since_heartbeat = time.time() - last_heartbeat_time
        if time_since_heartbeat > freeze_threshold:
            print(f"[HERA Watchdog] Render frozen for {time_since_heartbeat:.1f}s")
            trigger_alert("FREEZE")
            break


if __name__ == "__main__":
    main()
