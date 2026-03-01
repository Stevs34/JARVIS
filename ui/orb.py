import tkinter as tk
import math
import time
import threading

_root = None
_canvas = None
_state = "idle"
_pulse = 0
_rings = []
_running = False

def set_orb_state(state):
    """Set orb state from anywhere — thread safe"""
    global _state
    _state = state

def _get_colours(state):
    if state == "idle":
        return "#00b4ff", "#0066cc"
    elif state == "listening":
        return "#00ffb4", "#00cc88"
    elif state == "processing":
        return "#ffa500", "#cc6600"
    elif state == "speaking":
        return "#00ff64", "#00cc44"
    return "#00b4ff", "#0066cc"

def _animate():
    global _pulse, _rings, _state

    if not _running:
        return

    _pulse = (_pulse + 0.05) % (2 * math.pi)
    _canvas.delete("all")

    cx, cy = 150, 150
    core_colour, glow_colour = _get_colours(_state)

    # Update rings
    global _rings
    _rings = [r + 0.025 for r in _rings if r < 1.5]
    if _state == "listening":
        if not _rings or _rings[-1] > 0.4:
            if len(_rings) < 3:
                _rings.append(0)

    # Draw expanding rings
    for ring in _rings:
        radius = int(55 + ring * 90)
        alpha = max(0, int(255 * (1 - ring / 1.5)))
        alpha_hex = format(alpha, '02x')
        colour = core_colour + alpha_hex if len(core_colour) == 7 else core_colour
        try:
            _canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                outline=core_colour, width=2
            )
        except:
            pass

    # Draw outer glow layers
    pulse_offset = int(4 * math.sin(_pulse))
    for i in range(6):
        size = 110 + i * 10 + pulse_offset
        opacity = max(0, 60 - i * 10)
        _canvas.create_oval(
            cx - size // 2, cy - size // 2,
            cx + size // 2, cy + size // 2,
            fill=glow_colour, outline=""
        )

    # Draw core
    core_size = int(80 + pulse_offset * 2)
    _canvas.create_oval(
        cx - core_size // 2, cy - core_size // 2,
        cx + core_size // 2, cy + core_size // 2,
        fill=core_colour, outline=""
    )

    # Draw inner bright core
    _canvas.create_oval(
        cx - 25, cy - 25,
        cx + 25, cy + 25,
        fill="white", outline=""
    )

    # Draw rotating arc when processing
    if _state == "processing":
        angle = (_pulse * 180 / math.pi) % 360
        _canvas.create_arc(
            cx - 65, cy - 65,
            cx + 65, cy + 65,
            start=angle, extent=120,
            outline=core_colour, width=3, style=tk.ARC
        )

    # Draw speaking bars
    if _state == "speaking":
        bar_count = 5
        bar_width = 6
        bar_gap = 10
        total_width = bar_count * (bar_width + bar_gap)
        start_x = cx - total_width // 2
        for i in range(bar_count):
            height = int(18 + 14 * math.sin(_pulse * 3 + i * 0.8))
            x = start_x + i * (bar_width + bar_gap)
            _canvas.create_rectangle(
                x, cy - height // 2,
                x + bar_width, cy + height // 2,
                fill=core_colour, outline=""
            )

    _root.after(30, _animate)

def launch_orb():
    """Launch orb — call from main thread"""
    global _root, _canvas, _running

    _root = tk.Tk()
    _root.title("JARVIS")
    _root.geometry("300x300")
    _root.configure(bg="black")
    _root.attributes("-topmost", True)
    _root.overrideredirect(True)  # Remove window border

    # Position bottom right
    screen_w = _root.winfo_screenwidth()
    screen_h = _root.winfo_screenheight()
    _root.geometry(f"300x300+{screen_w - 320}+{screen_h - 350}")

    _canvas = tk.Canvas(
        _root, width=300, height=300,
        bg="black", highlightthickness=0
    )
    _canvas.pack()

    _running = True
    _animate()
    _root.mainloop()

def stop_orb():
    global _running
    _running = False
    if _root:
        _root.destroy()