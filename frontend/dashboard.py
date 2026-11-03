
import customtkinter as ctk
from pathlib import Path
from PIL import Image

BG = "#F7F4EF"
WHITE = "#FFFFFF"
TEXT = "#332B27"
MUTED = "#8B8178"
ACCENT = "#B77B62"
BORDER = "#EAE3DA"

BASE_DIR = Path(__file__).resolve().parent.parent


class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master, navigate_callback=None):

        super().__init__(master, fg_color=BG, corner_radius=0)

        self.navigate_callback = navigate_callback

        self.create_header()
        self.create_statistics()
        self.create_recent_section()

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.pack(fill="x", padx=35, pady=(30, 20))

        ctk.CTkLabel(
            header,
            text="Your wardrobe, reimagined.",
            font=("Arial", 28, "bold"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Welcome back! Let's make getting dressed easier.",
            font=("Arial", 13),
            text_color=MUTED
        ).pack(anchor="w", pady=(6, 0))

    def create_statistics(self):

        from backend.database import get_dashboard_stats

        stats = get_dashboard_stats()

        data = [
            ("TOTAL CLOTHES", stats["total_clothes"],
             "Pieces in your wardrobe"),

            ("OUTFITS CREATED", stats["total_outfits"],
             "Saved combinations"),

            ("TIMES WORN", stats["total_worn"],
             "Recorded wear events"),

            ("FAVOURITE CATEGORY", stats["favourite_category"],
             "Your largest category")
        ]

        section = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        section.pack(fill="x", padx=28, pady=10)

        for title, value, description in data:

            card = ctk.CTkFrame(
                section,
                fg_color=WHITE,
                corner_radius=15,
                height=135,
                border_width=1,
                border_color=BORDER
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=7
            )

            card.pack_propagate(False)

            ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 10, "bold"),
                text_color=MUTED
            ).pack(anchor="w", padx=15, pady=(18, 5))

            ctk.CTkLabel(
                card,
                text=str(value),
                font=("Arial", 25, "bold"),
                text_color=TEXT
            ).pack(anchor="w", padx=15)

            ctk.CTkLabel(
                card,
                text=description,
                font=("Arial", 10),
                text_color=MUTED
            ).pack(anchor="w", padx=15, pady=(5, 0))

    def create_recent_section(self):

        from backend.database import get_recent_clothes

        section = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        section.pack(fill="x", padx=35, pady=(30, 10))

        ctk.CTkLabel(
            section,
            text="Recently added",
            font=("Arial", 21, "bold"),
            text_color=TEXT
        ).pack(side="left")

        ctk.CTkButton(
            section,
            text="View all  →",
            width=105,
            fg_color="transparent",
            hover_color="#EDE4DA",
            text_color=ACCENT,
            command=lambda: self.navigate("My Wardrobe")
            if self.navigate_callback else None
        ).pack(side="right")

        clothes = get_recent_clothes(4)

        container = ctk.CTkFrame(
            self,
            fg_color=WHITE,
            corner_radius=15,
            border_width=1,
            border_color=BORDER
        )
        container.pack(fill="both", expand=True, padx=35, pady=10)

        if not clothes:

            ctk.CTkLabel(
                container,
                text="✧",
                font=("Arial", 42),
                text_color=ACCENT
            ).pack(pady=(35, 5))

            ctk.CTkLabel(
                container,
                text="Your wardrobe starts here.",
                font=("Arial", 19, "bold"),
                text_color=TEXT
            ).pack()

            ctk.CTkLabel(
                container,
                text="Add your first clothing item to begin.",
                font=("Arial", 12),
                text_color=MUTED
            ).pack(pady=7)

            ctk.CTkButton(
                container,
                text="+  Add clothing",
                fg_color=ACCENT,
                hover_color="#96624F",
                command=lambda: self.navigate("Add Clothing")
                if self.navigate_callback else None
            ).pack(pady=15)

        else:

            gallery = ctk.CTkFrame(
                container,
                fg_color="transparent"
            )
            gallery.pack(fill="both", expand=True, padx=15, pady=15)

            for item in clothes:

                card = ctk.CTkFrame(
                    gallery,
                    fg_color=BG,
                    corner_radius=12
                )
                card.pack(
                    side="left",
                    fill="both",
                    expand=True,
                    padx=6
                )

                image_path = item.get("image_path")

                if image_path:
                    path = Path(image_path)
                    if not path.is_absolute():
                        path = BASE_DIR / path

                    if path.exists():
                        try:
                            img = Image.open(path)
                            img.thumbnail((180, 150))
                            photo = ctk.CTkImage(
                                light_image=img,
                                dark_image=img,
                                size=(130, 130)
                            )

                            image_label = ctk.CTkLabel(
                                card,
                                text="",
                                image=photo
                            )
                            image_label.pack(pady=10)

                        except Exception:
                            self.show_image_placeholder(card)
                    else:
                        self.show_image_placeholder(card)
                else:
                    self.show_image_placeholder(card)

                ctk.CTkLabel(
                    card,
                    text=item["name"],
                    font=("Arial", 12, "bold"),
                    text_color=TEXT
                ).pack(pady=(5, 2))

                ctk.CTkLabel(
                    card,
                    text=item["category"],
                    font=("Arial", 10),
                    text_color=MUTED
                ).pack(pady=(0, 10))

    def show_image_placeholder(self, parent):

        ctk.CTkLabel(
            parent,
            text="No image",
            width=130,
            height=130,
            fg_color="#EAE3DA",
            corner_radius=10,
            text_color=MUTED
        ).pack(pady=10)
