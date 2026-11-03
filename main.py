
import customtkinter as ctk
from tkinter import messagebox

# Backend imports
from backend.database import initialize_database

# Frontend imports
from frontend.dashboard import DashboardFrame
from frontend.add_clothing import AddClothingFrame
from frontend.wardrobe import WardrobeFrame


# ==========================================
# REWEAR APPLICATION THEME
# ==========================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG = "#F7F4EF"
SIDEBAR = "#332B27"
ACCENT = "#B77B62"
WHITE = "#FFFFFF"
TEXT = "#332B27"
MUTED = "#8B8178"


# ==========================================
# MAIN APPLICATION CLASS
# ==========================================

class ReWearApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # Initialize database
        initialize_database()

        # Window settings
        self.title("ReWear | Smart Digital Wardrobe")
        self.geometry("1300x800")
        self.minsize(1050, 650)
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
            width=235,
            corner_radius=0,
            fg_color=SIDEBAR
        )

        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Application logo
        ctk.CTkLabel(
            self.sidebar,
            text="reWear.",
            font=("Arial", 32, "bold"),
            text_color=WHITE
        ).pack(anchor="w", padx=28, pady=(35, 3))

        # Subtitle
        ctk.CTkLabel(
            self.sidebar,
            text="YOUR DIGITAL WARDROBE",
            font=("Arial", 9),
            text_color="#C2B5AA"
        ).pack(anchor="w", padx=30, pady=(0, 40))

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
                height=48,
                corner_radius=10,
                anchor="w",
                font=("Arial", 14),
                fg_color="transparent",
                hover_color="#51423B",
                text_color=WHITE,
                command=lambda p=name: self.navigate(p)
            )

            button.pack(fill="x", padx=15, pady=5)

            self.nav_buttons[name] = button

        # Sidebar footer
        ctk.CTkLabel(
            self.sidebar,
            text="Dress better.\nWear smarter.",
            font=("Arial", 12, "italic"),
            text_color="#C2B5AA"
        ).pack(side="bottom", pady=30)

    # ======================================
    # MAIN CONTENT AREA
    # ======================================

    def create_main_content(self):

        self.content = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
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

            button.configure(
                fg_color=ACCENT if name == page else "transparent"
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
            font=("Arial", 30, "bold"),
            text_color=TEXT
        ).pack(pady=(150, 15))

        ctk.CTkLabel(
            self.content,
            text="This section is under development.",
            font=("Arial", 14),
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
