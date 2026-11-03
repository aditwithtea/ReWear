```python
import customtkinter as ctk
from tkinter import messagebox

# Backend imports
from backend.database import initialize_database

# Frontend imports
from frontend.dashboard import DashboardFrame
from frontend.add_clothing import AddClothingFrame
from frontend.wardrobe import WardrobeFrame


# ==========================================
# REWEAR QUIET LUXURY COLOUR PALETTE
# ==========================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG = "#F7F4EF"          # Warm ivory
SIDEBAR = "#EEE8DE"     # Soft cream
CARD = "#FFFFFF"        # White
TAUPE = "#B6A797"       # Taupe
MOCHA = "#806C5B"       # Mocha
TEXT = "#382F2A"        # Deep espresso
MUTED = "#8B8178"       # Muted brown
SAGE = "#A7AA96"        # Muted sage
BORDER = "#E5DED4"      # Soft border

# Button colours
PRIMARY = "#382F2A"
PRIMARY_HOVER = "#806C5B"
ACTIVE_BG = "#F7F4EF"


# ==========================================
# MAIN APPLICATION CLASS
# ==========================================

class ReWearApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # Initialize database
        initialize_database()

        # Window settings
        self.title("ReWear | Your Digital Closet")
        self.geometry("1440x900")
        self.minsize(1100, 700)
        self.configure(fg_color=BG)

        self.current_page = "Dashboard"

        # Build application layout
        self.create_sidebar()
        self.create_main_content()

        # Open dashboard initially
        self.navigate("Dashboard")

    # ======================================
    # SIDEBAR
    # ======================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=225,
            corner_radius=0,
            fg_color=SIDEBAR,
            border_width=0
        )

        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Application logo
        ctk.CTkLabel(
            self.sidebar,
            text="reWear.",
            font=("Cormorant Garamond", 38, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=28, pady=(30, 0))

        # Brand subtitle
        ctk.CTkLabel(
            self.sidebar,
            text="Y O U R   D I G I T A L   C L O S E T",
            font=("DM Sans", 8),
            text_color=MOCHA
        ).pack(anchor="w", padx=30, pady=(0, 45))

        # Navigation buttons
        self.nav_buttons = {}

        navigation = [
            ("Dashboard", "⌂"),
            ("My Wardrobe", "▣"),
            ("Add Clothing", "+"),
            ("Outfit Planner", "✧"),
            ("Recommendations", "♡"),
            ("Analytics", "▥")
        ]

        for name, symbol in navigation:

            button = ctk.CTkButton(
                self.sidebar,
                text=f"   {symbol}    {name}",
                height=44,
                corner_radius=8,
                anchor="w",
                font=("DM Sans", 13),
                fg_color="transparent",
                hover_color="#E5DED4",
                text_color=TEXT,
                command=lambda p=name: self.navigate(p),
                border_width=0
            )

            button.pack(fill="x", padx=12, pady=4)

            self.nav_buttons[name] = button

        # Sidebar footer
        ctk.CTkLabel(
            self.sidebar,
            text="Dress better.\nWear smarter.",
            font=("Cormorant Garamond", 18, "italic"),
            text_color=MOCHA,
            justify="left"
        ).pack(side="bottom", anchor="w", padx=28, pady=30)

    # ======================================
    # MAIN CONTENT AREA
    # ======================================

    def create_main_content(self):

        self.content = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0,
            border_width=0
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

    # ======================================
    # CLEAR CURRENT PAGE
    # ======================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # ======================================
    # PAGE NAVIGATION
    # ======================================

    def navigate(self, page):

        self.current_page = page

        # Highlight active sidebar button
        for name, button in self.nav_buttons.items():

            is_active = name == page

            button.configure(
                fg_color=ACTIVE_BG if is_active else "transparent",
                text_color=TEXT,
                hover_color="#E5DED4"
            )

        # Clear previous screen
        self.clear_content()

        try:

            if page == "Dashboard":

                self.show_dashboard()

            elif page == "Add Clothing":

                self.show_add_clothing()

            elif page == "My Wardrobe":

                self.show_wardrobe()

            elif page in [
                "Outfit Planner",
                "Recommendations",
                "Analytics"
            ]:

                self.show_placeholder(page)

        except Exception as error:

            messagebox.showerror(
                "Page loading error",
                f"Unable to open {page}.\n\n{error}"
            )

    # ======================================
    # DASHBOARD SCREEN
    # ======================================

    def show_dashboard(self):

        dashboard = DashboardFrame(
            self.content,
            navigate_callback=self.navigate
        )

        dashboard.pack(
            fill="both",
            expand=True
        )

    # ======================================
    # ADD CLOTHING SCREEN
    # ======================================

    def show_add_clothing(self):

        screen = AddClothingFrame(
            self.content,
            navigate_callback=self.navigate
        )

        screen.pack(
            fill="both",
            expand=True
        )

    # ======================================
    # MY WARDROBE SCREEN
    # ======================================

    def show_wardrobe(self):

        screen = WardrobeFrame(
            self.content,
            navigate_callback=self.navigate
        )

        screen.pack(
            fill="both",
            expand=True
        )

    # ======================================
    # TEMPORARY SCREENS
    # ======================================

    def show_placeholder(self, page):

        ctk.CTkLabel(
            self.content,
            text=page,
            font=("Cormorant Garamond", 34),
            text_color=TEXT
        ).pack(pady=(150, 15))

        ctk.CTkLabel(
            self.content,
            text="This section is under development.",
            font=("DM Sans", 13),
            text_color=MUTED
        ).pack()

    # ======================================
    # CLOSE APPLICATION
    # ======================================

    def on_close(self):

        self.destroy()


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    try:

        app = ReWearApp()

        app.protocol(
            "WM_DELETE_WINDOW",
            app.on_close
        )

        app.mainloop()

    except Exception as error:

        print("ReWear startup error:", error)
        raise
```
