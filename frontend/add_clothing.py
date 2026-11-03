
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

from backend.clothing_manager import add_clothing

BG = "#F7F4EF"
WHITE = "#FFFFFF"
TEXT = "#332B27"
MUTED = "#8B8178"
ACCENT = "#B77B62"
BORDER = "#EAE3DA"


class AddClothingFrame(ctk.CTkFrame):

    def __init__(self, master, navigate_callback=None):

        super().__init__(master, fg_color=BG)

        self.navigate_callback = navigate_callback
        self.selected_image = None
        self.preview_image = None

        self.create_form()

    def create_form(self):

        # Page heading
        ctk.CTkLabel(
            self,
            text="Add new clothing",
            font=("Arial", 28, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=35, pady=(30, 5))

        ctk.CTkLabel(
            self,
            text="Add a new piece to your digital wardrobe.",
            font=("Arial", 13),
            text_color=MUTED
        ).pack(anchor="w", padx=35, pady=(0, 20))

        # Scrollable form
        self.form = ctk.CTkScrollableFrame(
            self,
            fg_color=WHITE,
            corner_radius=15,
            border_width=1,
            border_color=BORDER
        )

        self.form.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 25)
        )

        # Image upload section
        ctk.CTkLabel(
            self.form,
            text="Clothing photograph",
            font=("Arial", 17, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=25, pady=(20, 10))

        self.image_preview = ctk.CTkLabel(
            self.form,
            text="No image selected\n\nUpload a clothing photo",
            width=250,
            height=190,
            fg_color=BG,
            corner_radius=12,
            text_color=MUTED
        )

        self.image_preview.pack(anchor="w", padx=25, pady=5)

        ctk.CTkButton(
            self.form,
            text="Choose photograph",
            fg_color=ACCENT,
            hover_color="#96624F",
            command=self.choose_image
        ).pack(anchor="w", padx=25, pady=10)

        # Input fields
        ctk.CTkLabel(
            self.form,
            text="Clothing details",
            font=("Arial", 17, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=25, pady=(20, 10))

        self.name_entry = self.create_input(
            "Clothing name",
            "Example: White oversized shirt"
        )

        self.category_menu = self.create_dropdown(
            "Category",
            ["Top", "Bottom", "Dress", "Outerwear",
             "Shoes", "Accessories", "Other"]
        )

        self.colour_menu = self.create_dropdown(
            "Colour",
            ["White", "Black", "Brown", "Beige",
             "Blue", "Pink", "Red", "Green",
             "Yellow", "Grey", "Purple", "Other"]
        )

        self.occasion_menu = self.create_dropdown(
            "Occasion",
            ["Casual", "College", "Office",
             "Party", "Formal", "Traditional",
             "Sports", "Other"]
        )

        self.season_menu = self.create_dropdown(
            "Season",
            ["Summer", "Winter", "Monsoon",
             "Spring", "Autumn", "All seasons"]
        )

        # Save button
        ctk.CTkButton(
            self.form,
            text="Save clothing item",
            height=45,
            width=220,
            corner_radius=10,
            fg_color=ACCENT,
            hover_color="#96624F",
            font=("Arial", 14, "bold"),
            command=self.save_clothing
        ).pack(anchor="w", padx=25, pady=30)

    def create_input(self, label, placeholder):

        ctk.CTkLabel(
            self.form,
            text=label,
            font=("Arial", 12, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=25, pady=(12, 5))

        entry = ctk.CTkEntry(
            self.form,
            width=400,
            height=40,
            placeholder_text=placeholder,
            fg_color=BG,
            border_color=BORDER,
            text_color=TEXT
        )

        entry.pack(anchor="w", padx=25)

        return entry

    def create_dropdown(self, label, options):

        ctk.CTkLabel(
            self.form,
            text=label,
            font=("Arial", 12, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=25, pady=(12, 5))

        menu = ctk.CTkOptionMenu(
            self.form,
            values=options,
            width=400,
            height=40,
            fg_color=ACCENT,
            button_color="#96624F",
            button_hover_color="#80503F",
            dropdown_fg_color=WHITE,
            text_color=WHITE
        )

        menu.pack(anchor="w", padx=25)

        return menu

    def choose_image(self):

        path = filedialog.askopenfilename(
            title="Choose clothing photograph",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.webp")
            ]
        )

        if not path:
            return

        self.selected_image = path

        try:
            image = Image.open(path).convert("RGB")
            image.thumbnail((250, 190))

            self.preview_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=image.size
            )

            self.image_preview.configure(
                image=self.preview_image,
                text=""
            )

        except Exception as error:
            messagebox.showerror("Image error", str(error))

    def save_clothing(self):

        name = self.name_entry.get()

        try:

            add_clothing(
                name=name,
                category=self.category_menu.get(),
                colour=self.colour_menu.get(),
                occasion=self.occasion_menu.get(),
                season=self.season_menu.get(),
                image_path=self.selected_image
            )

            messagebox.showinfo(
                "Success",
                "Clothing item added successfully!"
            )

            if self.navigate_callback:
                self.navigate_callback("Dashboard")

        except Exception as error:

            messagebox.showerror(
                "Unable to save clothing",
                str(error)
            )
