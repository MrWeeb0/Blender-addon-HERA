bl_info = {
    "name": "HERA",
    "blender": (3, 0, 0),
    "author": "The Argos Initiative",
    "version": (0, 1, 0),
    "location": "Render > Render Watchdog",
    "description": "Monitor Blender renders for freezes and crashes",
    "category": "Render",
}

import bpy
from . import handlers
from .preferences import HERA_AddonPreferences, HERA_PT_Preferences


def register():
    """Register the addon components."""
    bpy.utils.register_class(HERA_AddonPreferences)
    bpy.utils.register_class(HERA_PT_Preferences)
    handlers.register_handlers()


def unregister():
    """Unregister the addon components."""
    handlers.unregister_handlers()
    bpy.utils.unregister_class(HERA_PT_Preferences)
    bpy.utils.unregister_class(HERA_AddonPreferences)


if __name__ == "__main__":
    register()
