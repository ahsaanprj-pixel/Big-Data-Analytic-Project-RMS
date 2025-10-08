"""
Main application window for Restaurant Management System.
Week 1: Basic UI window setup + database connection test.
Later weeks will enable menus and additional windows.
"""

import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from sqlite3 import Error

# ====== Original imports (keep for later weeks) ======
# from BASE.Components.printorders import PrintOrders
# from BASE.Components.configwindow import ConfigWindow
# from BASE.Components.kitchenwindow import KitchenWindow
# from BASE.Components.createorders import CreateOrders
# from BASE.Components.aboutwindow import AboutWindow
# =====================================================

from BASE.Components.Database import Database


class MainWindow(tk.Tk):
    """Main Tkinter window of the Restaurant Management System."""

    def __init__(self):
        super().__init__()  # Initialize parent Tkinter window

        # ====== Window Setup ======
        self.win_width = 900      # Window width (increased for better layout)
        self.win_height = 600     # Window height (increased for better layout)

        # Get screen size for centering the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position to center the window
        self.center_x = int(screen_width / 2 - self.win_width / 2)
        self.center_y = int(screen_height / 2 - self.win_height / 2)

        # Set the geometry (size and position)
        self.geometry(f"{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}")

        # Disable resizing (fixed window)
        self.resizable(False, False)

        # Window title
        self.title("🍽️ Restaurant Management System")

        # ====== Frame (Container) ======
        self.m_frame = ttk.Frame(self, width=self.win_width, height=self.win_height)
        self.m_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.m_frame.grid_propagate(False)  # Prevent frame auto-resizing

        # ====== Icon Setup ======
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets", "icon_m.png"
        )

        # Try to load and set the window icon
        if os.path.exists(icon_path):
            self.icon_image = Image.open(icon_path)
            self.python_image = ImageTk.PhotoImage(self.icon_image)
            self.iconphoto(True, self.python_image)
        else:
            print("⚠️ icon_m.png not found — skipping window icon")

        # ====== Menu Bar Setup ======
        self.menubar = tk.Menu(self.m_frame)
        self.filebar = tk.Menu(self.menubar, tearoff=0)

        # Original menu commands (commented out for future weeks)
        # self.filebar.add_cascade(label="Print Receipts", command=self.print_win, state=tk.DISABLED)
        # self.filebar.add_cascade(label="Kitchen", command=self.kitchen_win, state=tk.DISABLED)
        # self.filebar.add_cascade(label="Create Orders", command=self.customer_win, state=tk.DISABLED)
        # self.filebar.add_cascade(label="Configure Facility/Menu", command=self.config_window)

        # Week 1 simplified (disabled options)
        self.filebar.add_command(label="🧾 Print Receipts", state=tk.DISABLED)
        self.filebar.add_command(label="👨‍🍳 Kitchen", state=tk.DISABLED)
        self.filebar.add_command(label="🛎️ Create Orders", state=tk.DISABLED)
        self.filebar.add_command(label="⚙️ Configure Facility/Menu", state=tk.DISABLED)

        self.filebar.add_separator()  # Visual separator
        self.filebar.add_command(label="❌ Exit", command=self.quit)  # Exit button
        self.menubar.add_cascade(label="File", menu=self.filebar)

        # Help menu (About section)
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        # self.helpmenu.add_command(label="About...", command=self.about_win)
        self.helpmenu.add_command(label="ℹ️ About...", state=tk.DISABLED)
        self.menubar.add_cascade(label="About", menu=self.helpmenu)

        # Attach menubar to window
        self.config(menu=self.menubar)

        # ====== Logo / Image Section ======
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets", "res.jpg"
        )

        # If image exists, display it
        if os.path.exists(img_path):
            self.img = Image.open(img_path)
            self.img = self.img.resize((300, 300), Image.Resampling.LANCZOS)  # Resize image
            self.img = ImageTk.PhotoImage(self.img)
            self.panel = tk.Label(
                self.m_frame,
                image=self.img,
                text="Restaurant Management System",
                compound="top",
                font=("Helvetica", 20, "bold"),
                bg="#F5F5F5",
                pady=10
            )
            self.panel.image = self.img  # Keep a reference to avoid garbage collection
            self.panel.place(relx=0.5, rely=0.45, anchor="center")  # Center image and text
        else:
            print("⚠️ restaurant.jpg not found — showing text only")
            self.panel = tk.Label(
                self.m_frame,
                text="🍽️ Restaurant Management System",
                font=("Helvetica", 22, "bold"),
                bg="#F5F5F5"
            )
            self.panel.place(relx=0.5, rely=0.4, anchor="center")

        # ====== Version Label (Bottom Left) ======
        self.vers = tk.Label(
            self.m_frame,
            text="v0.1.2, N.A",
            font=("Helvetica", 8),
            bg="#F5F5F5",
            fg="#555"
        )
        self.vers.place(relx=0.01, rely=0.96, anchor="sw")  # Bottom-left corner

        # ====== Run Database Test ======
        self.check_databases()

    # ==========================================================
    # DATABASE TEST SECTION
    # ==========================================================
    def check_databases(self):
        """Connect to the database and print confirmation in terminal."""
        try:
            self.fac_db = Database("restaurant.db")  # Connect or create db
            load_query = """SELECT * FROM gen_config"""
            res = self.fac_db.read_val(load_query)  # Read data
            print("✅ Database connected successfully:", res)
        except Error as e:
            print("❌ Database error:", e)

    # ==========================================================
    # Original window launchers (kept commented for next weeks)
    # ==========================================================
    # def config_window(self):
    #     config_window = ConfigWindow(self, self.check_databases)
    #     config_window.grab_set()

    # def kitchen_win(self):
    #     kitchen_win = KitchenWindow(self, self.check_databases)
    #     kitchen_win.grab_set()

    # def customer_win(self):
    #     customer_win = CreateOrders(self, self.check_databases)
    #     customer_win.grab_set()

    # def about_win(self):
    #     about_win = AboutWindow(self)
    #     about_win.grab_set()

    # def print_win(self):
    #     print_win = PrintOrders(self)
    #     print_win.grab_set()
    # ==========================================================
