
import sys
from pathlib import Path

import flet as ft

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.clothing_manager import (
    get_all_clothing,
    add_clothing,
    delete_clothing,
)

BG = "#F7F4EF"
BROWN = "#332B27"
ACCENT = "#B77B62"
MUTED = "#8B8178"
WHITE = "#FFFFFF"


def show_wardrobe(page: ft.Page):

    selected_image = {"path": None}

    # File picker service for Flet 1.0
    file_picker = ft.FilePicker()

    # Search
    search_field = ft.TextField(
        hint_text="Search your wardrobe...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=15,
        bgcolor=WHITE,
        color=BROWN,
    )

    # Category filter
    category_dropdown = ft.Dropdown(
        label="Category",
        value="All",
        options=[
            ft.dropdown.Option("All"),
            ft.dropdown.Option("Top"),
            ft.dropdown.Option("Bottom"),
            ft.dropdown.Option("Dress"),
            ft.dropdown.Option("Shoes"),
            ft.dropdown.Option("Accessories"),
        ],
        border=ft.OutlineInputBorder(border_radius=12),
    )

    count_text = ft.Text(color=MUTED, size=14)

    clothing_grid = ft.ResponsiveRow(
        columns=12,
        spacing=12,
        run_spacing=12,
    )

    # Add clothing form fields
    name_field = ft.TextField(
        label="Clothing name",
        border_radius=12,
    )

    category_field = ft.Dropdown(
        label="Category",
        options=[
            ft.dropdown.Option("Top"),
            ft.dropdown.Option("Bottom"),
            ft.dropdown.Option("Dress"),
            ft.dropdown.Option("Shoes"),
            ft.dropdown.Option("Accessories"),
        ],
        border=ft.OutlineInputBorder(border_radius=12),
    )

    colour_field = ft.TextField(
        label="Colour",
        border_radius=12,
    )

    occasion_field = ft.Dropdown(
        label="Occasion",
        options=[
            ft.dropdown.Option("Casual"),
            ft.dropdown.Option("Formal"),
            ft.dropdown.Option("Party"),
            ft.dropdown.Option("Sports"),
            ft.dropdown.Option("Everyday"),
        ],
        border=ft.OutlineInputBorder(border_radius=12),
    )

    season_field = ft.Dropdown(
        label="Season",
        options=[
            ft.dropdown.Option("Summer"),
            ft.dropdown.Option("Winter"),
            ft.dropdown.Option("Monsoon"),
            ft.dropdown.Option("All Season"),
        ],
        border=ft.OutlineInputBorder(border_radius=12),
    )

    image_status = ft.Text(
        "No photo selected",
        color=MUTED,
        size=13,
    )

    form_status = ft.Text(color=ACCENT, size=13)

    # Image picker
    async def pick_image(e):
        files = await file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png", "webp"],
        )

        if files:
            selected_image["path"] = files[0].path
            image_status.value = files[0].name
            page.update()

    # Refresh gallery
    def refresh_grid(e=None):

        clothing_grid.controls.clear()

        items = get_all_clothing(
            search=search_field.value or "",
            category=category_dropdown.value or "All",
        )

        count_text.value = f"{len(items)} clothing items"

        if not items:
            clothing_grid.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No clothing found. Add something to your wardrobe!",
                        color=MUTED,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=30,
                    bgcolor=WHITE,
                    border_radius=18,
                    col={"xs": 12},
                )
            )

        for item in items:

            image_path = item.get("image_path")

            image_widget = ft.Container(
                content=ft.Text("👗", size=45),
                height=160,
                alignment=ft.Alignment.CENTER,
                bgcolor="#F0E9E2",
                border_radius=12,
            )

            if image_path:
                full_path = PROJECT_ROOT / image_path

                if full_path.exists():
                    image_widget = ft.Image(
                        src=str(full_path),
                        height=160,
                        width=float("inf"),
                        fit=ft.BoxFit.COVER,
                        border_radius=12,
                    )

            def remove_item(clothing_id):
                def handler(e):
                    delete_clothing(clothing_id)
                    refresh_grid()
                    page.update()
                return handler

            card = ft.Container(
                content=ft.Column(
                    [
                        image_widget,
                        ft.Text(
                            item["name"],
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=BROWN,
                        ),
                        ft.Text(
                            item.get("category") or "Uncategorised",
                            color=MUTED,
                        ),
                        ft.Text(
                            f"Colour: {item.get('colour') or 'Not specified'}",
                            size=12,
                            color=MUTED,
                        ),
                        ft.TextButton(
                            "Delete",
                            icon=ft.Icons.DELETE_OUTLINE,
                            on_click=remove_item(item["clothing_id"]),
                        ),
                    ],
                    spacing=8,
                ),
                bgcolor=WHITE,
                padding=12,
                border_radius=16,
                col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
            )

            clothing_grid.controls.append(card)

        page.update()

    # Save clothing
    def save_clothing(e):

        if not name_field.value or not name_field.value.strip():
            form_status.value = "Please enter a clothing name."
            page.update()
            return

        if not category_field.value:
            form_status.value = "Please select a category."
            page.update()
            return

        try:
            add_clothing(
                name=name_field.value,
                category=category_field.value,
                colour=colour_field.value or "",
                occasion=occasion_field.value or "",
                season=season_field.value or "",
                image_path=selected_image["path"],
            )

            name_field.value = ""
            category_field.value = None
            colour_field.value = ""
            occasion_field.value = None
            season_field.value = None

            selected_image["path"] = None
            image_status.value = "No photo selected"

            form_status.value = "Clothing saved successfully!"

            refresh_grid()
            page.update()

        except Exception as error:
            form_status.value = f"Could not save: {error}"
            page.update()

    # Form container
    add_form = ft.Container(
        visible=False,
        content=ft.Column(
            [
                ft.Text(
                    "Add a Clothing Item",
                    size=21,
                    weight=ft.FontWeight.BOLD,
                    color=BROWN,
                ),
                name_field,
                category_field,
                colour_field,
                occasion_field,
                season_field,
                ft.Button(
                    content="Choose Photo",
                    icon=ft.Icons.ADD_A_PHOTO,
                    on_click=pick_image,
                ),
                image_status,
                ft.Button(
                    content="Save to Wardrobe",
                    bgcolor=ACCENT,
                    color=WHITE,
                    on_click=save_clothing,
                ),
                form_status,
            ],
            spacing=12,
        ),
        bgcolor=WHITE,
        padding=20,
        border_radius=18,
    )

    def toggle_form(e):
        add_form.visible = not add_form.visible
        page.update()

    add_button = ft.Button(
        content="+ Add Clothing",
        bgcolor=ACCENT,
        color=WHITE,
        on_click=toggle_form,
    )

    search_field.on_change = refresh_grid
    category_dropdown.on_change = refresh_grid

    refresh_grid()

    return ft.Column(
        [
            ft.Text(
                "My Wardrobe",
                size=30,
                weight=ft.FontWeight.BOLD,
                color=BROWN,
            ),
            ft.Text(
                "All your favourite pieces, in one place.",
                color=MUTED,
            ),
            add_button,
            add_form,
            search_field,
            category_dropdown,
            count_text,
            clothing_grid,
        ],
        spacing=14,
        scroll=ft.ScrollMode.AUTO,
    )
