import bpy


class HERA_AddonPreferences(bpy.types.AddonPreferences):
    """Addon preferences for HERA Render Watchdog."""
    
    bl_idname = __package__
    
    enable_watchdog: bool = bpy.props.BoolProperty(
        name="Enable Watchdog",
        description="Enable render monitoring",
        default=True
    )
    
    freeze_threshold: int = bpy.props.IntProperty(
        name="Freeze Threshold (seconds)",
        description="Seconds without heartbeat before flagging as frozen",
        default=60,
        min=30,
        max=300
    )
    
    enable_sound: bool = bpy.props.BoolProperty(
        name="Enable Sound Alerts",
        description="Play audio alerts on render issues",
        default=True
    )
    
    custom_sound_path: str = bpy.props.StringProperty(
        name="Custom Sound Path",
        description="Path to custom .wav file for alerts",
        default="",
        subtype="FILE_PATH"
    )


class HERA_PT_Preferences(bpy.types.AddonPreferences):
    """Preferences panel UI for HERA."""
    
    bl_label = "HERA Render Watchdog"
    bl_space_type = "PREFERENCES"
    bl_region_type = "WINDOW"
    
    def draw(self, context):
        layout = self.layout
        prefs = context.preferences.addons[__package__].preferences
        
        layout.prop(prefs, "enable_watchdog")
        layout.prop(prefs, "freeze_threshold")
        layout.prop(prefs, "enable_sound")
        layout.prop(prefs, "custom_sound_path")
