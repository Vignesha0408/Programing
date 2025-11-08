# pro_round_clock.py
import tkinter as tk
from tkinter import simpledialog, colorchooser, messagebox
import time, math, os, json, threading, sys
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL not available. Install with: pip install Pillow")
HOME = os.path.expanduser("~")
CFG = os.path.join(HOME, ".pro_round_clock.json")
DEFAULTS = {
    "size": 240,
    "theme": "dark",
    "topmost": True,
    "opacity": 1.0,
    "show_digital": True,
    "x": 100,
    "y": 100
}
def load_settings():
    try:
        with open(CFG,"r") as f:
            d = json.load(f)
        for k,v in DEFAULTS.items():
            if k not in d: d[k]=v
        return d
    except Exception:
        return DEFAULTS.copy()
def save_settings(s):
    try:
        with open(CFG,"w") as f:
            json.dump(s, f)
    except Exception:
        pass
S = load_settings()
IS_WINDOWS = sys.platform.startswith("win")
if IS_WINDOWS:
    import ctypes
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    CreateEllipticRgn = gdi32.CreateEllipticRgn
    SetWindowRgn = user32.SetWindowRgn
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", S["topmost"])
root.wm_attributes("-topmost", S["topmost"])
root.geometry(f"{S['size']}x{S['size']}+{S['x']}+{S['y']}")
root.resizable(False, False)
TRANSPARENT_KEY = "#f0f1f2"
size = S["size"]
canvas = tk.Canvas(root, width=size, height=size, highlightthickness=0)
canvas.pack(fill="both", expand=True)
THEMES = {
    "dark": {
        "bg": "#000000", "fg": "#e6fff0", "accent": "#00e676", "sec": "#ff3b30"
    },
    "light": {
        "bg": "#ffffff", "fg": "#202020", "accent": "#0066cc", "sec": "#cc0000"
    },
    "neon": {
        "bg": "#060018", "fg": "#00ffd5", "accent": "#ff00ff", "sec": "#ffea00"
    }
}
def apply_theme(name):
    global THEME
    THEME = THEMES.get(name, THEMES["dark"])
    root.config(bg=THEME["bg"])
    canvas.config(bg=THEME["bg"])
    S["theme"] = name
    save_settings(S)
apply_theme(S["theme"])
def animate_size_change(new_size):
    current_size = S["size"]
    steps = 10
    step_size = (new_size - current_size) / steps
    def animate_step(step):
        if step < steps:
            intermediate_size = int(current_size + step_size * (step + 1))
            S["size"] = intermediate_size
            enforce_round_shape()
            root.after(20, lambda: animate_step(step + 1))
        else:
            S["size"] = new_size
            enforce_round_shape()
            save_settings(S)
    animate_step(0)
def animate_opacity_change(new_opacity):
    current_opacity = S["opacity"]
    steps = 10
    step_opacity = (new_opacity - current_opacity) / steps
    def animate_step(step):
        if step < steps:
            intermediate_opacity = current_opacity + step_opacity * (step + 1)
            S["opacity"] = intermediate_opacity
            try:
                root.attributes("-alpha", intermediate_opacity)
            except Exception:
                pass
            root.after(20, lambda: animate_step(step + 1))
        else:
            S["opacity"] = new_opacity
            try:
                root.attributes("-alpha", new_opacity)
            except Exception:
                pass
            save_settings(S)
    animate_step(0)
def enforce_round_shape():
    global size
    size = S["size"]
    root.geometry(f"{size}x{size}+{S.get('x',100)}+{S.get('y',100)}")
    canvas.config(width=size, height=size)
    if IS_WINDOWS:
        hwnd = root.winfo_id()
        rgn = CreateEllipticRgn(0,0,size,size)
        SetWindowRgn(hwnd, rgn, True)
    else:
        try:
            root.config(bg=TRANSPARENT_KEY)
            canvas.config(bg=TRANSPARENT_KEY)
            root.wm_attributes("-transparentcolor", TRANSPARENT_KEY)
        except Exception:
            pass
enforce_round_shape()
drag = {"x":0,"y":0}
def start_drag(e):
    drag["x"]=e.x
    drag["y"]=e.y
    if S.get("topmost", True):
        root.attributes("-topmost", True)
        root.lift()
def do_drag(e):
    x = root.winfo_pointerx() - drag["x"]
    y = root.winfo_pointery() - drag["y"]
    root.geometry(f"+{x}+{y}")
    S["x"]=x; S["y"]=y
    if S.get("topmost", True):
        root.lift()
def end_drag(e):
    save_settings(S)
    if S.get("topmost", True):
        root.lift()
root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", do_drag)
root.bind("<ButtonRelease-1>", end_drag)
def dblclick(e):
    sw = root.winfo_screenwidth(); sh = root.winfo_screenheight()
    nx = sw//2 - S["size"]//2
    ny = sh//2 - S["size"]//2
    root.geometry(f"+{nx}+{ny}")
    S["x"]=nx; S["y"]=ny; save_settings(S)
    if S.get("topmost", True):
        root.lift()
root.bind("<Double-Button-1>", dblclick)
def increase_size():
    if S["size"] < 600:
        animate_size_change(min(600, S["size"] + 20))
def decrease_size():
    if S["size"] > 120:
        animate_size_change(max(120, S["size"] - 20))
def set_opacity():
    val = simpledialog.askfloat("Opacity", "0.2 - 1.0", initialvalue=S.get("opacity",1.0), minvalue=0.2, maxvalue=1.0)
    if val:
        animate_opacity_change(val)
def increase_opacity():
    if S["opacity"] < 1.0:
        animate_opacity_change(min(1.0, S["opacity"] + 0.1))
def decrease_opacity():
    if S["opacity"] > 0.2:
        animate_opacity_change(max(0.2, S["opacity"] - 0.1))
def toggle_topmost():
    S["topmost"] = not S.get("topmost", True)
    root.attributes("-topmost", S["topmost"])
    save_settings(S)
def ensure_always_on_top():
    """Ensure the clock stays on top of all windows."""
    try:
        # Multiple approaches to ensure always on top
        root.wm_attributes("-topmost", True)
        root.attributes("-topmost", True)
        root.lift()
        # Force focus to help maintain topmost status
        root.focus_force()
    except Exception:
        pass
    # Check more frequently to maintain topmost status
    root.after(100, ensure_always_on_top)  # Check every 100ms for maximum responsiveness

# Start the always-on-top enforcement
ensure_always_on_top()

def toggle_digital():
    S["show_digital"] = not S.get("show_digital", True)
    save_settings(S)
def cycle_themes():
    themes = list(THEMES.keys())
    current_index = themes.index(S["theme"])
    next_index = (current_index + 1) % len(themes)
    apply_theme(themes[next_index])
    save_settings(S)
def quit_all():
    save_settings(S)
    root.destroy()
    sys.exit(0)
def set_theme():
    theme_window = tk.Toplevel(root)
    theme_window.title("Select Theme")
    theme_window.geometry("300x200")
    theme_window.resizable(False, False)
    theme_window.transient(root)
    theme_window.grab_set()
    preview_canvas = tk.Canvas(theme_window, width=100, height=100, highlightthickness=0)
    preview_canvas.pack(pady=10)
    selected_theme = tk.StringVar(value=S["theme"])
    def preview_theme(theme_name):
        theme = THEMES.get(theme_name, THEMES["dark"])
        preview_canvas.config(bg=theme["bg"])
        cx, cy = 50, 50
        r = 40
        preview_canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=theme["bg"], outline=theme["fg"], width=2)
        preview_canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill=theme["accent"], outline=theme["fg"])
        preview_canvas.create_line(cx, cy, cx+r*0.7, cy, fill=theme["fg"], width=2)
        preview_canvas.create_line(cx, cy, cx, cy-r*0.6, fill=theme["fg"], width=1)
        preview_canvas.create_text(cx, cy+r*0.3, text="12", fill=theme["fg"], font=("Helvetica", 8))
    for i, theme_name in enumerate(THEMES.keys()):
        rb = tk.Radiobutton(
            theme_window, 
            text=theme_name.capitalize(), 
            variable=selected_theme, 
            value=theme_name,
            command=lambda t=theme_name: preview_theme(t)
        )
        rb.pack(anchor="w", padx=20, pady=2)
    preview_theme(S["theme"])
    def apply_selected_theme():
        apply_theme(selected_theme.get())
        save_settings(S)
        theme_window.destroy()
    button_frame = tk.Frame(theme_window)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Apply", command=apply_selected_theme).pack(side="left", padx=5)
    tk.Button(button_frame, text="Cancel", command=theme_window.destroy).pack(side="left", padx=5)
def set_size():
    size_window = tk.Toplevel(root)
    size_window.title("Adjust Size")
    size_window.geometry("300x100")
    size_window.resizable(False, False)
    size_window.transient(root)
    size_window.grab_set()
    size_label = tk.Label(size_window, text=f"Size: {S['size']}px")
    size_label.pack(pady=5)
    size_slider = tk.Scale(
        size_window, 
        from_=120, 
        to=600, 
        orient="horizontal", 
        length=250,
        command=lambda val: update_size_preview(int(val), size_label)
    )
    size_slider.set(S["size"])
    size_slider.pack(pady=10)
    button_frame = tk.Frame(size_window)
    button_frame.pack(pady=5)
    def apply_size():
        new_size = size_slider.get()
        animate_size_change(new_size)
        size_window.destroy()
    tk.Button(button_frame, text="Apply", command=apply_size).pack(side="left", padx=5)
    tk.Button(button_frame, text="Cancel", command=size_window.destroy).pack(side="left", padx=5)
def update_size_preview(new_size, label):
    label.config(text=f"Size: {new_size}px")
    S["size"] = new_size
    enforce_round_shape()
menu = tk.Menu(root, tearoff=0)
menu.add_command(label="Exit", command=quit_all)
def popup(e):
    menu.tk_popup(e.x_root, e.y_root)
root.bind("<Button-3>", popup)
center = lambda: (S["size"]//2, S["size"]//2)
def draw_clock(smooth=False):
    global hover_items
    canvas.delete("all")
    hover_items = []
    sz = S["size"]
    cx, cy = sz//2, sz//2
    r = int(sz*0.47)
    face = canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=THEME["bg"], outline=THEME["fg"], width=3)
    hover_items.append(face)
    for i in range(60):
        ang = math.radians(i*6)
        x1 = cx + (r-6)*math.sin(ang)
        y1 = cy - (r-6)*math.cos(ang)
        if i%5==0:
            x2 = cx + (r-14)*math.sin(ang); y2 = cy - (r-14)*math.cos(ang)
            tick = canvas.create_line(x1,y1,x2,y2, fill=THEME["fg"], width=3)
            hover_items.append(tick)
        else:
            x2 = cx + (r-10)*math.sin(ang); y2 = cy - (r-10)*math.cos(ang)
            tick = canvas.create_line(x1,y1,x2,y2, fill=THEME["fg"], width=1)
            hover_items.append(tick)
    for hnum in range(1,13):
        ang = math.radians(hnum*30)
        tx = cx + (r-28)*math.sin(ang)
        ty = cy - (r-28)*math.cos(ang)
        num = canvas.create_text(tx,ty, text=str(hnum), fill=THEME["fg"], font=("Helvetica", max(8, sz//20), "bold"))
        hover_items.append(num)
    center_dot = canvas.create_oval(cx-6, cy-6, cx+6, cy+6, fill=THEME["accent"], outline=THEME["fg"])
    hover_items.append(center_dot)
    t = time.time()
    lt = time.localtime(t)
    sec = lt.tm_sec + (t - int(t))
    minute = lt.tm_min + sec/60.0
    hour = (lt.tm_hour % 12) + minute/60.0
    hour_len = r * 0.5
    min_len = r * 0.72
    sec_len = r * 0.84
    hx = cx + hour_len * math.sin(math.radians(hour*30))
    hy = cy - hour_len * math.cos(math.radians(hour*30))
    mx = cx + min_len * math.sin(math.radians(minute*6))
    my = cy - min_len * math.cos(math.radians(minute*6))
    sx = cx + sec_len * math.sin(math.radians(sec*6))
    sy = cy - sec_len * math.cos(math.radians(sec*6))
    hour_hand = canvas.create_line(cx,cy,hx,hy, fill=THEME["fg"], width=max(2, S["size"]//30), capstyle="round")
    min_hand = canvas.create_line(cx,cy,mx,my, fill=THEME["fg"], width=max(1, S["size"]//45), capstyle="round")
    sec_hand = canvas.create_line(cx,cy,sx,sy, fill=THEME["sec"], width=max(1, S["size"]//80), capstyle="round")
    hover_items.extend([hour_hand, min_hand, sec_hand])
    if S.get("show_digital", True):
        timestr = time.strftime("%I:%M:%S %p").lstrip("0")
        digital_time = canvas.create_text(cx, cy + r*0.45, text=timestr, fill=THEME["fg"], font=("Monospace", max(9, S["size"]//16)))
        hover_items.append(digital_time)
    try:
        logo_y_pos = cy - r*0.30
        logo_elements = []
        if PIL_AVAILABLE:
            try:
                img = Image.open("titan-logo.jpg")
                img_width = max(30, S["size"]//8)
                img_height = max(15, S["size"]//16)
                img = img.resize((img_width, img_height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                logo_image = canvas.create_image(cx, logo_y_pos, image=photo)
                canvas.image = photo
                logo_elements.append(logo_image)
            except Exception as e:
                rect_width = max(30, S["size"]//8)
                rect_height = max(15, S["size"]//16)
                logo_rect = canvas.create_rectangle(
                    cx - rect_width//2, logo_y_pos - rect_height//2,
                    cx + rect_width//2, logo_y_pos + rect_height//2,
                    fill=THEME["accent"], outline=THEME["fg"], width=1)
                logo_elements.append(logo_rect)
        else:
            rect_width = max(30, S["size"]//8)
            rect_height = max(15, S["size"]//16)
            logo_rect = canvas.create_rectangle(
                cx - rect_width//2, logo_y_pos - rect_height//2,
                cx + rect_width//2, logo_y_pos + rect_height//2,
                fill=THEME["accent"], outline=THEME["fg"], width=1)
            logo_elements.append(logo_rect)
        hover_items.extend(logo_elements)
    except Exception as e:
        pass
def update_clock():
    draw_clock()
    root.after(100, update_clock)
update_clock()

# === Fade-In Effect ===
root.attributes('-alpha', 0.0)
def fade_in(alpha=0.0):  # Changed to float type
    if alpha < 1.0:
        root.attributes('-alpha', alpha)
        root.after(30, lambda: fade_in(alpha + 0.05))
fade_in()

# === Enhanced Always-On-Top Function ===
# Function already defined above, removing duplicate definition
# Start the always-on-top enforcement
# ensure_always_on_top()  # This is already called above

# === Run Application ===
root.mainloop()