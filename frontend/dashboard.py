import customtkinter as ctk
from pathlib import Path
from PIL import Image

# ==========================================
# REWEAR QUIET LUXURY THEME
# ==========================================

BG = "#F7F4EF"
SIDEBAR = "#EEE8DE"
WHITE = "#FFFFFF"
TEXT = "#382F2A"
MUTED = "#806C5B"
TAUPE = "#B6A797"
MOCHA = "#806C5B"
SAGE = "#A7AA96"
BORDER = "#EAE3DA"
HIGHLIGHT = "#DDC8B6"

HEADING_FONT = "Cormorant Garamond"
BODY_FONT = "DM Sans"

BASE_DIR = Path(__file__).resolve().parent.parent


class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master, navigate_callback=None):

        super().__init__(
            master,
            fg_color=BG,
            corner_radius=0
        )

        self.navigate_callback = navigate_callback
        self.images = []

        # Main dashboard layout
        self.create_layout()

    # ======================================
    # MAIN LAYOUT
    # ======================================

    def create_layout(self):

        self.wrapper = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.wrapper.pack(
            fill="both",
            expand=True,
            padx=34,
            pady=24
        )

        self.wrapper.grid_columnconfigure(0, weight=1)
        self.wrapper.grid_columnconfigure(1, weight=0)
        self.wrapper.grid_rowconfigure(1, weight=1)

        # Main content
        self.main_area = ctk.CTkFrame(
            self.wrapper,
            fg_color="transparent"
        )

        self.main_area.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="nsew",
            padx=(0, 22)
        )

        self.main_area.grid_columnconfigure(0, weight=1)

        # Right sidebar
        self.right_panel = ctk.CTkFrame(
            self.wrapper,
            fg_color="transparent",
            width=210
        )

        self.right_panel.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky="nsew"
        )

        self.right_panel.grid_propagate(False)

        self.create_header()
        self.create_statistics()
        self.create_inspiration_banner()
        self.create_recent_section()

        self.create_quick_actions()
        self.create_top_picks()
        self.create_style_card()

    # ======================================
    # HEADER
    # ======================================

    def create_header(self):

        header = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            pady=(0, 20)
        )

        ctk.CTkLabel(
            header,
            text="Good evening, Adi.",
            font=(HEADING_FONT, 32, "italic"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="A little inspiration for your wardrobe today.",
            font=(BODY_FONT, 12),
            text_color=MOCHA
        ).pack(anchor="w", pady=(3, 0))

    # ======================================
    # STATISTICS
    # ======================================

    def create_statistics(self):

        from backend.database import get_dashboard_stats

        stats = get_dashboard_stats()

        data = [
            ("WARDROBE PIECES", stats["total_clothes"], "♧"),
            ("SAVED OUTFITS", stats["total_outfits"], "▱"),
            ("TIMES WORN", stats["total_worn"], "+")
        ]

        section = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        section.pack(
            fill="x",
            pady=(0, 16)
        )

        for title, value, symbol in data:

            card = ctk.CTkFrame(
                section,
                fg_color=WHITE,
                corner_radius=9,
                border_width=1,
                border_color=BORDER,
                height=78
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(0, 10)
            )

            card.pack_propagate(False)

            content = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            content.pack(
                fill="both",
                expand=True,
                padx=12,
                pady=10
            )

            ctk.CTkLabel(
                content,
                text=symbol,
                font=(BODY_FONT, 20),
                text_color=MOCHA
            ).pack(side="left", padx=(0, 12))

            details = ctk.CTkFrame(
                content,
                fg_color="transparent"
            )

            details.pack(side="left", fill="y")

            ctk.CTkLabel(
                details,
                text=title,
                font=(BODY_FONT, 9, "bold"),
                text_color=MOCHA
            ).pack(anchor="w")

            ctk.CTkLabel(
                details,
                text=str(value),
                font=(HEADING_FONT, 21),
                text_color=TEXT
            ).pack(anchor="w")

    # ======================================
    # INSPIRATION BANNER
    # ======================================

    def create_inspiration_banner(self):

        banner = ctk.CTkFrame(
            self.main_area,
            fg_color="#EEE4D9",
            corner_radius=14,
            height=205
        )

        banner.pack(
            fill="x",
            pady=(0, 20)
        )

        banner.pack_propagate(False)

        banner.grid_columnconfigure(0, weight=1)
        banner.grid_columnconfigure(1, weight=1)
        banner.grid_rowconfigure(0, weight=1)

        # Text section
        text_area = ctk.CTkFrame(
            banner,
            fg_color="transparent"
        )

        text_area.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=22,
            pady=18
        )

        ctk.CTkLabel(
            text_area,
            text="YOUR DAILY INSPIRATION",
            font=(BODY_FONT, 9, "bold"),
            text_color=MOCHA
        ).pack(anchor="w", pady=(5, 10))

        ctk.CTkLabel(
            text_area,
            text="Less, but better.",
            font=(HEADING_FONT, 27, "italic"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_area,
            text="Discover new combinations using\npieces you already own.",
            font=(BODY_FONT, 11),
            text_color=TEXT,
            justify="left"
        ).pack(anchor="w", pady=(7, 12))

        ctk.CTkButton(
            text_area,
            text="Explore outfits  →",
            height=32,
            width=135,
            corner_radius=3,
            fg_color=TEXT,
            hover_color=MOCHA,
            text_color=WHITE,
            font=(BODY_FONT, 10, "bold"),
            command=lambda: self.navigate("Recommendations")
            if self.navigate_callback else None
        ).pack(anchor="w")

        # Image section
        self.banner_image_area = ctk.CTkFrame(
            banner,
            fg_color="#D8C9B9",
            corner_radius=0
        )

        self.banner_image_area.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.load_banner_image()

    def load_banner_image(self):

        # Optional local inspiration image.
        # Add your own image at assets/inspiration.jpg

        image_path = BASE_DIR / "assets" / "inspiration.jpg"

        if image_path.exists():

            try:

                img = Image.open(image_path).convert("RGB")

                photo = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(300, 205)
                )

                self.images.append(photo)

                ctk.CTkLabel(
                    self.banner_image_area,
                    text="",
                    image=photo
                ).pack(fill="both", expand=True)

                return

            except Exception:
                pass

        ctk.CTkLabel(
            self.banner_image_area,
            text="Your wardrobe,\nyour inspiration.",
            font=(HEADING_FONT, 20, "italic"),
            text_color=TEXT
        ).pack(expand=True)

    # ======================================
    # RECENTLY ADDED SECTION
    # ======================================

    def create_recent_section(self):

        from backend.database import get_recent_clothes

        heading = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        heading.pack(fill="x", pady=(0, 8))

        title_area = ctk.CTkFrame(
            heading,
            fg_color="transparent"
        )

        title_area.pack(side="left")

        ctk.CTkLabel(
            title_area,
            text="Recently added",
            font=(HEADING_FONT, 22),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_area,
            text="Fresh additions to your collection.",
            font=(BODY_FONT, 10),
            text_color=MOCHA
        ).pack(anchor="w")

        ctk.CTkButton(
            heading,
            text="See all  →",
            width=80,
            height=28,
            fg_color="transparent",
            hover_color="#EDE4DA",
            text_color=MOCHA,
            font=(BODY_FONT, 10),
            command=lambda: self.navigate("My Wardrobe")
            if self.navigate_callback else None
        ).pack(side="right", pady=5)

        clothes = get_recent_clothes(4)

        gallery = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        gallery.pack(fill="x")

        for item in clothes:

            self.create_clothing_card(gallery, item)

        if not clothes:

            empty = ctk.CTkFrame(
                gallery,
                fg_color=WHITE,
                corner_radius=10,
                border_width=1,
                border_color=BORDER
            )

            empty.pack(fill="x", pady=5)

            ctk.CTkLabel(
                empty,
                text="Your wardrobe starts here.",
                font=(HEADING_FONT, 20),
                text_color=TEXT
            ).pack(pady=(18, 4))

            ctk.CTkLabel(
                empty,
                text="Add your first clothing item to begin.",
                font=(BODY_FONT, 11),
                text_color=MUTED
            ).pack(pady=(0, 10))

            ctk.CTkButton(
                empty,
                text="+ Add clothing",
                fg_color=TEXT,
                hover_color=MOCHA,
                text_color=WHITE,
                command=lambda: self.navigate("Add Clothing")
                if self.navigate_callback else None
            ).pack(pady=(0, 18))

    # ======================================
    # INDIVIDUAL CLOTHING CARD
    # ======================================

    def create_clothing_card(self, parent, item):

        card = ctk.CTkFrame(
            parent,
            fg_color=WHITE,
            corner_radius=10,
            border_width=1,
            border_color=BORDER,
            width=145,
            height=165
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 9)
        )

        card.pack_propagate(False)

        image_path = item.get("image_path")

        image_box = ctk.CTkFrame(
            card,
            fg_color="#EEE8DE",
            corner_radius=5,
            height=108
        )

        image_box.pack(
            fill="x",
            padx=5,
            pady=(5, 4)
        )

        image_box.pack_propagate(False)

        loaded = False

        if image_path:

            path = Path(image_path)

            if not path.is_absolute():
                path = BASE_DIR / path

            if path.exists():

                try:

                    img = Image.open(path).convert("RGB")

                    photo = ctk.CTkImage(
                        light_image=img,
                        dark_image=img,
                        size=(125, 108)
                    )

                    self.images.append(photo)

                    ctk.CTkLabel(
                        image_box,
                        text="",
                        image=photo
                    ).pack(fill="both", expand=True)

                    loaded = True

                except Exception:
                    pass

        if not loaded:

            ctk.CTkLabel(
                image_box,
                text="No image",
                font=(BODY_FONT, 10),
                text_color=MUTED
            ).pack(expand=True)

        ctk.CTkLabel(
            card,
            text=item.get("name", "Clothing item"),
            font=(BODY_FONT, 11, "bold"),
            text_color=TEXT,
            anchor="w"
        ).pack(
            fill="x",
            padx=8,
            pady=(1, 0)
        )

        ctk.CTkLabel(
            card,
            text=item.get("category", ""),
            font=(BODY_FONT, 9),
            text_color=MOCHA,
            anchor="w"
        ).pack(
            fill="x",
            padx=8,
            pady=(0, 5)
        )

    # ======================================
    # RIGHT PANEL - QUICK ACTIONS
    # ======================================

    def create_quick_actions(self):

        card = ctk.CTkFrame(
            self.right_panel,
            fg_color=WHITE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        card.pack(fill="x", pady=(82, 14))

        ctk.CTkLabel(
            card,
            text="Quick actions",
            font=(HEADING_FONT, 18),
            text_color=TEXT
        ).pack(pady=(12, 8))

        actions = [
            ("＋", "Add clothing", "Add Clothing"),
            ("✧", "Get looks", "Recommendations"),
            ("▦", "Plan outfit", "Outfit Planner")
        ]

        row = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        row.pack(fill="x", padx=8, pady=(0, 12))

        for symbol, label, page in actions:

            action = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )

            action.pack(
                side="left",
                expand=True,
                fill="x"
            )

            ctk.CTkButton(
                action,
                text=symbol,
                width=43,
                height=40,
                corner_radius=5,
                fg_color=SIDEBAR,
                hover_color="#E5DED4",
                text_color=MOCHA,
                font=(BODY_FONT, 17),
                command=lambda p=page: self.navigate(p)
                if self.navigate_callback else None
            ).pack()

            ctk.CTkLabel(
                action,
                text=label,
                font=(BODY_FONT, 9),
                text_color=TEXT
            ).pack(pady=(4, 0))

    # ======================================
    # RIGHT PANEL - TOP PICKS
    # ======================================

    def create_top_picks(self):

        card = ctk.CTkFrame(
            self.right_panel,
            fg_color=WHITE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        card.pack(fill="x", pady=(0, 14))

        ctk.CTkLabel(
            card,
            text="Top picks for you",
            font=(HEADING_FONT, 18),
            text_color=TEXT
        ).pack(pady=(12, 7))

        preview = ctk.CTkFrame(
            card,
            fg_color=SIDEBAR,
            height=112,
            corner_radius=5
        )

        preview.pack(
            fill="x",
            padx=12,
            pady=(0, 7)
        )

        preview.pack_propagate(False)

        ctk.CTkLabel(
            preview,
            text="Your wardrobe favourites",
            font=(HEADING_FONT, 15, "italic"),
            text_color=MOCHA
        ).pack(expand=True)

        ctk.CTkLabel(
            card,
            text="Discover your personal style.",
            font=(BODY_FONT, 9),
            text_color=MOCHA
        ).pack(pady=(0, 12))

        ctk.CTkButton(
            card,
            text="Explore looks  →",
            height=29,
            fg_color="transparent",
            hover_color=SIDEBAR,
            text_color=MOCHA,
            font=(BODY_FONT, 10),
            command=lambda: self.navigate("Recommendations")
            if self.navigate_callback else None
        ).pack(pady=(0, 7))

    # ======================================
    # RIGHT PANEL - TRACK YOUR STYLE
    # ======================================

    def create_style_card(self):

        card = ctk.CTkFrame(
            self.right_panel,
            fg_color=HIGHLIGHT,
            corner_radius=12
        )

        card.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            card,
            text="Track your style",
            font=(HEADING_FONT, 19),
            text_color=TEXT
        ).pack(anchor="w", padx=16, pady=(14, 8))

        ctk.CTkLabel(
            card,
            text="See what you wear most\nand find new favourites.",
            font=(BODY_FONT, 10),
            text_color=TEXT,
            justify="left"
        ).pack(anchor="w", padx=16)

        ctk.CTkButton(
            card,
            text="View analytics  →",
            height=32,
            corner_radius=3,
            fg_color=TEXT,
            hover_color=MOCHA,
            text_color=WHITE,
            font=(BODY_FONT, 10, "bold"),
            command=lambda: self.navigate("Analytics")
            if self.navigate_callback else None
        ).pack(
            anchor="w",
            padx=16,
            pady=14
        )
