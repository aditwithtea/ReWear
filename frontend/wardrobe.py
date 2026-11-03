
import customtkinter as ctk
from pathlib import Path
from PIL import Image
from tkinter import messagebox

from backend.clothing_manager import (
    get_all_clothing,
    delete_clothing
)

BG = "#F7F4EF"
WHITE = "#FFFFFF"
TEXT = "#332B27"
MUTED = "#8B8178"
ACCENT = "#B77B62"
BORDER = "#EAE3DA"

BASE_DIR = Path(__file__).resolve().parent.parent


class WardrobeFrame(ctk.CTkFrame):

    def __init__(self, master, navigate_callback=None):

        super().__init__(master, fg_color=BG)

        self.navigate_callback = navigate_callback
        self.image_references = []

        self.create_header()
        self.create_filters()
        self.create_gallery()

        self.load_clothes()

    # -----------------------------
    # HEADER
    # -----------------------------

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.pack(fill="x", padx=35, pady=(30, 10))

        ctk.CTkLabel(
            header,
            text="My Wardrobe",
            font=("Arial", 28, "bold"),
            text_color=TEXT
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="+ Add Clothing",
            fg_color=ACCENT,
            hover_color="#96624F",
            command=self.open_add_clothing
        ).pack(side="right")

        self.count_label = ctk.CTkLabel(
            self,
            text="Your personal clothing collection",
            font=("Arial", 12),
            text_color=MUTED
        )

        self.count_label.pack(anchor="w", padx=37, pady=(0, 15))

    # -----------------------------
    # FILTERS
    # -----------------------------

    def create_filters(self):

        filters = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        filters.pack(fill="x", padx=35, pady=10)

        self.search_entry = ctk.CTkEntry(
            filters,
            placeholder_text="Search clothing...",
            width=260,
            height=40,
            fg_color=WHITE,
            border_color=BORDER,
            text_color=TEXT
        )
        self.search_entry.pack(side="left", padx=(0, 12))

        self.category_filter = ctk.CTkOptionMenu(
            filters,
            values=[
                "All", "Top", "Bottom", "Dress",
                "Outerwear", "Shoes", "Accessories", "Other"
            ],
            fg_color=ACCENT,
            button_color="#96624F",
            button_hover_color="#80503F",
            command=lambda value: self.load_clothes()
        )
        self.category_filter.pack(side="left", padx=8)

        self.colour_filter = ctk.CTkOptionMenu(
            filters,
            values=[
                "All", "White", "Black", "Brown",
                "Beige", "Blue", "Pink", "Red",
                "Green", "Yellow", "Grey", "Purple", "Other"
            ],
            fg_color=ACCENT,
            button_color="#96624F",
            button_hover_color="#80503F",
            command=lambda value: self.load_clothes()
        )
        self.colour_filter.pack(side="left", padx=8)

        ctk.CTkButton(
            filters,
            text="Search",
            width=85,
            fg_color=TEXT,
            hover_color="#51423B",
            command=self.load_clothes
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            filters,
            text="Reset",
            width=75,
            fg_color="transparent",
            text_color=ACCENT,
            hover_color="#EDE4DA",
            command=self.reset_filters
        ).pack(side="left", padx=3)

    # -----------------------------
    # GALLERY CONTAINER
    # -----------------------------

    def create_gallery(self):

        self.gallery = ctk.CTkScrollableFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )

        self.gallery.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

    # -----------------------------
    # LOAD CLOTHING
    # -----------------------------

    def load_clothes(self, value=None):

        for widget in self.gallery.winfo_children():
            widget.destroy()

        self.image_references.clear()

        clothes = get_all_clothing(
            search=self.search_entry.get(),
            category=self.category_filter.get(),
            colour=self.colour_filter.get()
        )

        self.count_label.configure(
            text=f"{len(clothes)} clothing items in your collection"
        )

        if not clothes:

            ctk.CTkLabel(
                self.gallery,
                text="Your wardrobe is waiting for its first outfit.",
                font=("Arial", 18, "bold"),
                text_color=TEXT
            ).pack(pady=(100, 10))

            ctk.CTkLabel(
                self.gallery,
                text="Try another search or add a clothing item.",
                font=("Arial", 12),
                text_color=MUTED
            ).pack(pady=5)

            return

        # Responsive number of columns
        columns = 3

        for index, item in enumerate(clothes):

            row = index // columns
            column = index % columns

            card = ctk.CTkFrame(
                self.gallery,
                fg_color=WHITE,
                corner_radius=15,
                border_width=1,
                border_color=BORDER
            )

            card.grid(
                row=row,
                column=column,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            self.gallery.grid_columnconfigure(
                column,
                weight=1,
                uniform="wardrobe"
            )

            self.create_clothing_card(card, item)

    # -----------------------------
    # CLOTHING CARD
    # -----------------------------

    def create_clothing_card(self, card, item):

        image_path = item.get("image_path")

        if image_path:

            path = Path(image_path)

            if not path.is_absolute():
                path = BASE_DIR / path

            if path.exists():

                try:
                    image = Image.open(path).convert("RGB")
                    image.thumbnail((220, 190))

                    photo = ctk.CTkImage(
                        light_image=image,
                        dark_image=image,
                        size=(190, 180)
                    )

                    self.image_references.append(photo)

                    ctk.CTkLabel(
                        card,
                        text="",
                        image=photo
                    ).pack(padx=10, pady=(12, 5))

                except Exception:
                    self.show_placeholder(card)

            else:
                self.show_placeholder(card)

        else:
            self.show_placeholder(card)

        ctk.CTkLabel(
            card,
            text=item["name"],
            font=("Arial", 15, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=15, pady=(8, 2))

        details = (
            f'{item["category"]}  •  '
            f'{item.get("colour") or "No colour"}'
        )

        ctk.CTkLabel(
            card,
            text=details,
            font=("Arial", 11),
            text_color=MUTED
        ).pack(anchor="w", padx=15)

        ctk.CTkLabel(
            card,
            text=f'Occasion: {item.get("occasion") or "Not specified"}',
            font=("Arial", 10),
            text_color=MUTED
        ).pack(anchor="w", padx=15, pady=3)

        ctk.CTkLabel(
            card,
            text=f'Worn {item["wear_count"]} times',
            font=("Arial", 10),
            text_color=MUTED
        ).pack(anchor="w", padx=15, pady=3)

        ctk.CTkButton(
            card,
            text="Delete item",
            height=32,
            fg_color="#F2E5E1",
            hover_color="#E6D0C9",
            text_color="#9B5144",
            command=lambda: self.remove_clothing(
                item["clothing_id"]
            )
        ).pack(fill="x", padx=15, pady=12)

    # -----------------------------
    # IMAGE PLACEHOLDER
    # -----------------------------

    def show_placeholder(self, parent):

        ctk.CTkLabel(
            parent,
            text="No image",
            width=190,
            height=180,
            fg_color=BG,
            corner_radius=10,
            text_color=MUTED
        ).pack(padx=10, pady=(12, 5))

    # -----------------------------
    # DELETE CLOTHING
    # -----------------------------

    def remove_clothing(self, clothing_id):

        confirm = messagebox.askyesno(
            "Delete clothing",
            "Are you sure you want to delete this item?"
        )

        if not confirm:
            return

        try:
            delete_clothing(clothing_id)
            self.load_clothes()

        except Exception as error:
            messagebox.showerror("Delete error", str(error))

    # -----------------------------
    # RESET FILTERS
    # -----------------------------

    def reset_filters(self):

        self.search_entry.delete(0, "end")
        self.category_filter.set("All")
        self.colour_filter.set("All")

        self.load_clothes()

    # -----------------------------
    # OPEN ADD CLOTHING
    # -----------------------------

    def open_add_clothing(self):

        if self.navigate_callback:
            self.navigate_callback("Add Clothing")
