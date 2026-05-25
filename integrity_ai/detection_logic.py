# integrity_ai/detection_logic.py

# -------------------------------
# Threshold Configuration
# -------------------------------
THRESHOLDS = {
    "tab_switch": 3,
    "focus_loss": 5,
    "voice_detect": 2,
    "gaze_off": 5
}

# -------------------------------
# Detection Logic
# -------------------------------
def detect_malpractice(events):
    """
    events = {
        "tab_switch": int,
        "focus_loss": int,
        "voice_detect": int,
        "gaze_off": int
    }
    """
    flags = []
    if events.get("tab_switch", 0) > THRESHOLDS["tab_switch"]:
        flags.append("High Tab Switching")
    if events.get("focus_loss", 0) > THRESHOLDS["focus_loss"]:
        flags.append("Screen Focus Loss")
    if events.get("voice_detect", 0) > THRESHOLDS["voice_detect"]:
        flags.append("Multiple Voices Detected")
    if events.get("gaze_off", 0) > THRESHOLDS["gaze_off"]:
        flags.append("Frequent Gaze Deviation")
    return flags
