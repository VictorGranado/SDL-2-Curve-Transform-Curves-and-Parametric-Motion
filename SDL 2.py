import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


# -----------------------------
# Math helpers (Unit 2 focused)
# -----------------------------

def parabola_xy(t, a=1.0, h=0.0, k=0.0):
    # y = a(x-h)^2 + k, param x = t
    x = t
    y = a * (t - h) ** 2 + k
    return x, y

def ellipse_xy(theta, a=3.0, b=2.0, h=0.0, k=0.0):
    # (x-h)^2/a^2 + (y-k)^2/b^2 = 1
    x = h + a * np.cos(theta)
    y = k + b * np.sin(theta)
    return x, y

def hyperbola_xy(t, a=2.0, b=1.5, h=0.0, k=0.0, branch=1):
    # (x-h)^2/a^2 - (y-k)^2/b^2 = 1
    # param: x = h + branch*a*cosh(t), y = k + b*sinh(t)
    x = h + branch * a * np.cosh(t)
    y = k + b * np.sinh(t)
    return x, y

def motion_ellipse(t, a=3.0, b=2.0, omega=1.0, h=0.0, k=0.0):
    # x = h + a cos(omega t), y = k + b sin(omega t)
    x = h + a * np.cos(omega * t)
    y = k + b * np.sin(omega * t)
    return x, y

def motion_ellipse_v(t, a=3.0, b=2.0, omega=1.0):
    # dx/dt = -a*omega*sin(omega t), dy/dt = b*omega*cos(omega t)
    vx = -a * omega * np.sin(omega * t)
    vy =  b * omega * np.cos(omega * t)
    return vx, vy

def motion_ellipse_a(t, a=3.0, b=2.0, omega=1.0):
    # d2x/dt2 = -a*omega^2*cos(omega t), d2y/dt2 = -b*omega^2*sin(omega t)
    ax = -a * (omega ** 2) * np.cos(omega * t)
    ay = -b * (omega ** 2) * np.sin(omega * t)
    return ax, ay

def motion_parabola_param(t, p=1.0, speed=1.0, h=0.0, k=0.0):
    # A simple param curve shaped like a parabola:
    # x = h + speed*t, y = k + p*(speed*t)^2
    u = speed * t
    x = h + u
    y = k + p * (u ** 2)
    return x, y

def motion_parabola_v(t, p=1.0, speed=1.0):
    # x = speed*t, y = p*(speed*t)^2
    # vx = speed
    # vy = 2p*(speed*t)*speed = 2p*speed^2*t
    vx = speed
    vy = 2.0 * p * (speed ** 2) * t
    return vx, vy

def motion_parabola_a(t, p=1.0, speed=1.0):
    # ax = 0
    # ay = 2p*speed^2
    ax = 0.0
    ay = 2.0 * p * (speed ** 2)
    return ax, ay


# -----------------------------
# GUI App
# -----------------------------

class SDL2CurvedMotionApp(tk.Tk):

    def _build_help_tab(self):
        # Scrollable text area
        frame = ttk.Frame(self.tab_help)
        frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)

        help_text = """
    SDL 2 — Curved Motion Visualizer (Unit 2)
    ========================================

    This tool has two main parts:
    1) Transform Curves
    2) Parametric Motion

    --------------------------------------------------------------------
    TAB 1: Transform Curves
    --------------------------------------------------------------------
    What you see:
    - Dashed curve: the “original / centered” curve (no translation).
    - Solid curve: the transformed curve after your changes.

    Controls:
    - Curve Type:
    * Parabola
    * Ellipse
    * Hyperbola

    - Translation (h, k):
    * h shifts left/right:
        +h = shift right
        -h = shift left
    * k shifts up/down:
        +k = shift up
        -k = shift down

    - Stretching / Parameters:
    * Ellipse:
        a = horizontal radius (wider/narrower)
        b = vertical radius (taller/shorter)
    * Hyperbola:
        a and b control how “wide/tall” the branch opens
    * Parabola:
        a controls how steep/narrow the parabola is

    - Hyperbola Branch:
    * Right (+) shows the right branch
    * Left (-) shows the left branch

    - Plot Range:
    Use this to zoom in/out. Hyperbolas can grow fast, so increasing the range helps.

    How to interpret:
    - Translation moves the curve without changing its shape.
    - Stretching changes width/height/steepness.

    Good Transform Test Cases:
    - Ellipse translation:
    Curve: Ellipse
    a=4, b=2, h=3, k=-2, range -8 to 8

    - Ellipse stretching:
    Curve: Ellipse
    h=0, k=0
    Try a=5, b=1 then a=2, b=5

    - Parabola steepness (same vertex):
    Curve: Parabola
    h=-2, k=1
    Try a=0.25 then a=2.0

    - Hyperbola branch flip:
    Curve: Hyperbola
    a=2, b=1, h=2, k=0
    Switch branch between Right and Left.

    --------------------------------------------------------------------
    TAB 2: Parametric Motion
    --------------------------------------------------------------------
    What you see:
    - A path curve (the motion track)
    - A moving point traveling along the path
    - Two arrows at the moving point:
    * Velocity vector: direction of motion “right now”
    * Acceleration vector: how velocity is changing “right now”
    - Readout shows:
    * time t
    * speed = magnitude of velocity

    Controls:
    - Motion Path:
    * Ellipse/Circle
    * Parabola-like

    - Center (h, k):
    Shifts the entire path.

    - Ellipse/Circle parameters:
    * a, b = ellipse radii
    * omega = how fast the point moves (bigger omega = faster)

    - Parabola-like parameters:
    * p = how “curved” the parabola is
    * speed = how fast x increases

    - v_scale and a_scale:
    These only scale arrow size so they’re easier to see.

    - Render Path:
    Updates the plot once.
    - Start / Stop:
    Animates the moving point.

    How to interpret:
    - Velocity arrow should look tangent to the curve (it points the direction you’re moving).
    - Acceleration arrow shows how the velocity is changing.
    - Speed readout increases/decreases depending on the motion.

    Good Motion Test Cases:
    - Circle (constant-ish speed):
    Motion: Ellipse/Circle
    a=3, b=3, omega=1, h=0, k=0

    - Ellipse (speed changes):
    Motion: Ellipse/Circle
    a=5, b=2, omega=1

    - Faster motion:
    Same as above but omega=2.5

    - Parabola-like motion:
    Motion: Parabola-like
    p=0.25, speed=1.0

    Tips:
    - If arrows look too small: increase v_scale or a_scale.
    - If the curve goes off-screen: adjust parameters or change the plot range in the Transform tab.

    --------------------------------------------------------------------
    Notes / Limits
    --------------------------------------------------------------------
    - This tool is made to support Unit 2 topics (curve graphs, transformations, and parametric motion).
    - It focuses on visual understanding, not perfect physical modeling.
    """

        text.insert("1.0", help_text.strip())
        text.config(state="disabled")  # read-only

    
    def __init__(self):
        super().__init__()
        self.title("SDL 2 — Curved Motion Visualizer (Unit 2)")
        self.geometry("1200x720")

        self._build_ui()

        # Animation state
        self.anim_running = False
        self.t_anim = 0.0
        self.after_id = None

    # ---------- UI ----------
    def _build_ui(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_transform = ttk.Frame(self.notebook, padding=10)
        self.tab_motion = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab_transform, text="1) Transform Curves")
        self.notebook.add(self.tab_motion, text="2) Parametric Motion")

        self.tab_help = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_help, text="Help")
        self._build_help_tab()

        self._build_transform_tab()
        self._build_motion_tab()

    def _make_figure(self, parent):
        fig = Figure(figsize=(7.6, 6.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.grid(True)
        ax.set_aspect("equal", adjustable="box")
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, parent)
        toolbar.update()

        return fig, ax, canvas

    # ---------- Tab 1: Transformations ----------
    def _build_transform_tab(self):
        left = ttk.Frame(self.tab_transform)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        right = ttk.Frame(self.tab_transform)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Plot
        self.fig1, self.ax1, self.canvas1 = self._make_figure(right)
        self.ax1.set_title("Curve Transformations (Translation + Stretching)")

        # Controls
        ttk.Label(left, text="Curve Type").pack(anchor="w")
        self.curve_type = tk.StringVar(value="Ellipse")
        curve_box = ttk.Combobox(left, textvariable=self.curve_type, values=["Parabola", "Ellipse", "Hyperbola"], state="readonly")
        curve_box.pack(anchor="w", fill=tk.X, pady=(0, 10))
        curve_box.bind("<<ComboboxSelected>>", lambda e: self.render_transform())

        ttk.Label(left, text="Translation (h horizontal, k vertical) shift").pack(anchor="w", pady=(0, 2))
        self.h_var = tk.DoubleVar(value=0.0)
        self.k_var = tk.DoubleVar(value=0.0)
        self._slider(left, "h", self.h_var, -5, 5, self.render_transform)
        self._slider(left, "k", self.k_var, -5, 5, self.render_transform)

        ttk.Label(left, text="Stretching / Parameters").pack(anchor="w", pady=(10, 2))

        # Parameters that depend on curve
        self.a_var = tk.DoubleVar(value=3.0)  # ellipse a, hyperbola a, parabola "a"
        self.b_var = tk.DoubleVar(value=2.0)  # ellipse b, hyperbola b
        self.p_var = tk.DoubleVar(value=1.0)  # parabola coefficient alias (uses a_var)
        self.branch_var = tk.IntVar(value=1)

        self.a_slider = self._slider(left, "a", self.a_var, 0.5, 6, self.render_transform)
        self.b_slider = self._slider(left, "b", self.b_var, 0.5, 6, self.render_transform)

        ttk.Label(left, text="Hyperbola Branch").pack(anchor="w", pady=(10, 2))
        branch_row = ttk.Frame(left)
        branch_row.pack(anchor="w", pady=(0, 10), fill=tk.X)
        ttk.Radiobutton(branch_row, text="Right (+)", variable=self.branch_var, value=1, command=self.render_transform).pack(side=tk.LEFT)
        ttk.Radiobutton(branch_row, text="Left (-)", variable=self.branch_var, value=-1, command=self.render_transform).pack(side=tk.LEFT)

        ttk.Label(left, text="Plot Range").pack(anchor="w", pady=(5, 2))
        range_row = ttk.Frame(left)
        range_row.pack(anchor="w", pady=(0, 10))
        self.rmin1 = tk.DoubleVar(value=-6)
        self.rmax1 = tk.DoubleVar(value=6)
        ttk.Entry(range_row, textvariable=self.rmin1, width=6).pack(side=tk.LEFT)
        ttk.Label(range_row, text=" to ").pack(side=tk.LEFT)
        ttk.Entry(range_row, textvariable=self.rmax1, width=6).pack(side=tk.LEFT)

        ttk.Button(left, text="Render", command=self.render_transform).pack(anchor="w", pady=(10, 0))

        self.status1 = tk.StringVar(value="Ready.")
        ttk.Label(left, textvariable=self.status1, foreground="#005").pack(anchor="w", pady=(10, 0))

        # First render
        self.render_transform()

    def _slider(self, parent, label, var, vmin, vmax, cmd):
        row = ttk.Frame(parent)
        row.pack(anchor="w", fill=tk.X, pady=(0, 6))
        ttk.Label(row, text=f"{label}:").pack(side=tk.LEFT)
        entry = ttk.Entry(row, textvariable=var, width=6)
        entry.pack(side=tk.LEFT, padx=(4, 6))

        s = ttk.Scale(row, variable=var, from_=vmin, to=vmax, command=lambda _x: cmd())
        s.pack(side=tk.LEFT, fill=tk.X, expand=True)
        return s

    def render_transform(self):
        try:
            self.ax1.clear()
            self.ax1.grid(True)
            self.ax1.set_aspect("equal", adjustable="box")
            self.ax1.set_title("Curve Transformations (Translation + Stretching)")

            ctype = self.curve_type.get()
            h, k = float(self.h_var.get()), float(self.k_var.get())
            a = float(self.a_var.get())
            b = float(self.b_var.get())
            rmin, rmax = float(self.rmin1.get()), float(self.rmax1.get())
            if rmin >= rmax:
                raise ValueError("Range min must be less than range max.")

            # Plot original (centered) + transformed (shifted)
            # Use light styling differences (no custom colors needed)
            if ctype == "Parabola":
                t = np.linspace(rmin, rmax, 600)
                # Original y = a x^2
                x0 = t
                y0 = a * (t ** 2)
                # Transformed y = a(x-h)^2 + k
                x1, y1 = parabola_xy(t, a=a, h=h, k=k)

                self.ax1.plot(x0, y0, linestyle="--", linewidth=1, label="original (centered)")
                self.ax1.plot(x1, y1, linewidth=2, label="transformed")

            elif ctype == "Ellipse":
                th = np.linspace(0, 2*np.pi, 600)
                # Original centered ellipse
                x0, y0 = ellipse_xy(th, a=a, b=b, h=0.0, k=0.0)
                # Transformed
                x1, y1 = ellipse_xy(th, a=a, b=b, h=h, k=k)

                self.ax1.plot(x0, y0, linestyle="--", linewidth=1, label="original (centered)")
                self.ax1.plot(x1, y1, linewidth=2, label="transformed")

            else:  # Hyperbola
                tt = np.linspace(0, 2.2, 500)  # cosh grows fast
                branch = int(self.branch_var.get())

                # Original centered branch
                x0, y0 = hyperbola_xy(tt, a=a, b=b, h=0.0, k=0.0, branch=branch)
                # Transformed
                x1, y1 = hyperbola_xy(tt, a=a, b=b, h=h, k=k, branch=branch)

                self.ax1.plot(x0, y0, linestyle="--", linewidth=1, label="original (centered)")
                self.ax1.plot(x1, y1, linewidth=2, label="transformed")

            self.ax1.set_xlim(rmin, rmax)
            self.ax1.set_ylim(rmin, rmax)
            self.ax1.set_xlabel("x")
            self.ax1.set_ylabel("y")
            self.ax1.legend(loc="upper right")

            self.canvas1.draw()
            self.status1.set("Rendered.")
        except Exception as e:
            self.status1.set("Error.")
            messagebox.showerror("Transform Render Error", str(e))

    # ---------- Tab 2: Parametric Motion ----------
    def _build_motion_tab(self):
        left = ttk.Frame(self.tab_motion)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        right = ttk.Frame(self.tab_motion)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Plot
        self.fig2, self.ax2, self.canvas2 = self._make_figure(right)
        self.ax2.set_title("Parametric Motion (Position, Velocity, Acceleration)")

        # Controls
        ttk.Label(left, text="Motion Path").pack(anchor="w")
        self.motion_type = tk.StringVar(value="Ellipse/Circle")
        motion_box = ttk.Combobox(left, textvariable=self.motion_type, values=["Ellipse/Circle", "Parabola-like"], state="readonly")
        motion_box.pack(anchor="w", fill=tk.X, pady=(0, 10))
        motion_box.bind("<<ComboboxSelected>>", lambda e: self.render_motion_static())

        ttk.Label(left, text="Center (h, k)").pack(anchor="w", pady=(0, 2))
        self.mh_var = tk.DoubleVar(value=0.0)
        self.mk_var = tk.DoubleVar(value=0.0)
        self._slider(left, "h", self.mh_var, -5, 5, self.render_motion_static)
        self._slider(left, "k", self.mk_var, -5, 5, self.render_motion_static)

        ttk.Label(left, text="Parameters").pack(anchor="w", pady=(10, 2))

        # For ellipse/circle
        self.ma_var = tk.DoubleVar(value=3.0)      # a radius
        self.mb_var = tk.DoubleVar(value=2.0)      # b radius
        self.omega_var = tk.DoubleVar(value=1.0)   # angular speed

        self._slider(left, "a", self.ma_var, 0.5, 6, self.render_motion_static)
        self._slider(left, "b", self.mb_var, 0.5, 6, self.render_motion_static)
        self._slider(left, "omega", self.omega_var, 0.2, 5, self.render_motion_static)

        # For parabola-like
        ttk.Label(left, text="Parabola p & speed").pack(anchor="w", pady=(10, 2))
        self.p_motion_var = tk.DoubleVar(value=0.25)
        self.speed_motion_var = tk.DoubleVar(value=1.0)
        self._slider(left, "p", self.p_motion_var, 0.05, 2.0, self.render_motion_static)
        self._slider(left, "speed", self.speed_motion_var, 0.2, 3.0, self.render_motion_static)

        ttk.Separator(left).pack(fill=tk.X, pady=10)

        ttk.Label(left, text="Vector display scale").pack(anchor="w")
        self.v_scale = tk.DoubleVar(value=1.0)
        self.a_scale = tk.DoubleVar(value=0.3)
        self._slider(left, "v_scale", self.v_scale, 0.1, 5.0, self.render_motion_static)
        self._slider(left, "a_scale", self.a_scale, 0.05, 2.0, self.render_motion_static)

        ttk.Separator(left).pack(fill=tk.X, pady=10)

        # Animation controls
        btn_row = ttk.Frame(left)
        btn_row.pack(anchor="w", pady=(0, 8))
        ttk.Button(btn_row, text="Render Path", command=self.render_motion_static).pack(side=tk.LEFT)
        ttk.Button(btn_row, text="Start", command=self.start_animation).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_row, text="Stop", command=self.stop_animation).pack(side=tk.LEFT)

        self.dt_var = tk.DoubleVar(value=0.03)
        ttk.Label(left, text="Time step (dt)").pack(anchor="w")
        ttk.Entry(left, textvariable=self.dt_var, width=8).pack(anchor="w", pady=(0, 6))

        self.status2 = tk.StringVar(value="Ready.")
        ttk.Label(left, textvariable=self.status2, foreground="#005").pack(anchor="w", pady=(6, 0))

        self.readout = tk.StringVar(value="t=0.00   speed=0.00")
        ttk.Label(left, textvariable=self.readout).pack(anchor="w", pady=(6, 0))

        # Initial render
        self.render_motion_static()

    def render_motion_static(self):
        try:
            self.ax2.clear()
            self.ax2.grid(True)
            self.ax2.set_aspect("equal", adjustable="box")
            self.ax2.set_title("Parametric Motion (Position, Velocity, Acceleration)")

            mtype = self.motion_type.get()
            h, k = float(self.mh_var.get()), float(self.mk_var.get())
            rmin, rmax = -7, 7

            # Draw the path curve
            if mtype == "Ellipse/Circle":
                a = float(self.ma_var.get())
                b = float(self.mb_var.get())
                th = np.linspace(0, 2*np.pi, 800)
                x, y = ellipse_xy(th, a=a, b=b, h=h, k=k)
                self.ax2.plot(x, y, linewidth=2, label="path (ellipse)")

                # Draw a sample instantaneous vectors at current t_anim
                t0 = self.t_anim
                omega = float(self.omega_var.get())
                px, py = motion_ellipse(t0, a=a, b=b, omega=omega, h=h, k=k)
                vx, vy = motion_ellipse_v(t0, a=a, b=b, omega=omega)
                ax, ay = motion_ellipse_a(t0, a=a, b=b, omega=omega)

            else:
                p = float(self.p_motion_var.get())
                spd = float(self.speed_motion_var.get())
                t = np.linspace(-3, 3, 800)
                x, y = motion_parabola_param(t, p=p, speed=spd, h=h, k=k)
                self.ax2.plot(x, y, linewidth=2, label="path (parabola-like)")

                t0 = self.t_anim
                px, py = motion_parabola_param(t0, p=p, speed=spd, h=h, k=k)
                vx, vy = motion_parabola_v(t0, p=p, speed=spd)
                ax, ay = motion_parabola_a(t0, p=p, speed=spd)

            # Point + vectors
            self.ax2.scatter([px], [py], s=40, label="moving point")

            vs = float(self.v_scale.get())
            ac = float(self.a_scale.get())

            self.ax2.quiver(px, py, vs*vx, vs*vy, angles="xy", scale_units="xy", scale=1)
            self.ax2.quiver(px, py, ac*ax, ac*ay, angles="xy", scale_units="xy", scale=1)

            speed = float(np.sqrt(vx*vx + vy*vy))
            self.readout.set(f"t={self.t_anim:.2f}   speed={speed:.3f}")
            self.ax2.set_xlim(rmin, rmax)
            self.ax2.set_ylim(rmin, rmax)
            self.ax2.set_xlabel("x")
            self.ax2.set_ylabel("y")
            self.ax2.legend(loc="upper right")

            self.canvas2.draw()
            self.status2.set("Rendered.")
        except Exception as e:
            self.status2.set("Error.")
            messagebox.showerror("Motion Render Error", str(e))

    def start_animation(self):
        if self.anim_running:
            return
        self.anim_running = True
        self.status2.set("Animating...")
        self._tick()

    def stop_animation(self):
        self.anim_running = False
        self.status2.set("Stopped.")
        if self.after_id is not None:
            try:
                self.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None

    def _tick(self):
        if not self.anim_running:
            return

        try:
            dt = float(self.dt_var.get())
            if dt <= 0:
                dt = 0.03
        except Exception:
            dt = 0.03

        # Advance time
        self.t_anim += dt

        # Keep time from growing forever (wrap)
        if self.motion_type.get() == "Ellipse/Circle":
            # Wrap by 2π/omega (period)
            omega = float(self.omega_var.get())
            period = (2*np.pi / omega) if omega != 0 else 2*np.pi
            if self.t_anim > period:
                self.t_anim -= period
        else:
            # Keep parabola time bounded for display
            if self.t_anim > 3:
                self.t_anim = -3

        self.render_motion_static()
        self.after_id = self.after(int(1000 * dt), self._tick)


if __name__ == "__main__":
    app = SDL2CurvedMotionApp()
    app.mainloop()
 