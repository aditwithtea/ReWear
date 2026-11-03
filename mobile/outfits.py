
import sys
from pathlib import Path

import flet as ft

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.database import get_connection
from backend.clothing_manager import get_all_clothing

BG = "#F7F4EF"
BROWN = "#332B27"
ACCENT = "#B77B62"
MUTED = "#8B8178"
WHITE = "#FFFFFF"


def show_outfits(page: ft.Page):

    clothes = get_all_clothing()

    outfit_name = ft.TextField(
        label="Outfit name",
        hint_text="e.g. Casual Sunday Look",
        border_radius=12,
    )

    occasion = ft.Dropdown(
        label="Occasion",
        value="Casual",
        options=[
            ft.dropdown.Option(x)
            for x in [
                "Casual", "Formal", "Party",
                "College", "Work", "Sports"
            ]
        ],
    )

    selection_area = ft.Column(spacing=10)
    preview_area = ft.ResponsiveRow(spacing=10, run_spacing=10)
    saved_area = ft.Column(spacing=14)
    status = ft.Text(color=ACCENT, size=14)

    item_selection = {}

    def get_image(item):

        image_path = item.get("image_path")

        if image_path:
            full_path = PROJECT_ROOT / image_path

            if full_path.exists():
                return ft.Image(
                    src=str(full_path),
                    width=105,
                    height=110,
                    fit=ft.BoxFit.COVER,
                    border_radius=12,
                )

        return ft.Container(
            content=ft.Text("👗", size=35),
            width=105,
            height=110,
            alignment=ft.Alignment.CENTER,
            bgcolor="#F0E9E2",
            border_radius=12,
        )

    def get_selected_items():

        selected_ids = [
            clothing_id
            for clothing_id, checkbox in item_selection.items()
            if checkbox.value
        ]

        return [
            item for item in clothes
            if item["clothing_id"] in selected_ids
        ]

    def refresh_preview(e=None):

        preview_area.controls.clear()

        selected = get_selected_items()

        for item in selected:

            preview_area.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            get_image(item),
                            ft.Text(
                                item["name"],
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=BROWN,
                            ),
                        ],
                        spacing=5,
                    ),
                    col={"xs": 6, "sm": 4, "md": 3},
                )
            )

        if not selected:
            preview_area.controls.append(
                ft.Text(
                    "Select clothing to preview your outfit.",
                    color=MUTED,
                )
            )

        page.update()

    def build_item_selection():

        item_selection.clear()
        selection_area.controls.clear()

        if not clothes:
            selection_area.controls.append(
                ft.Text(
                    "Your wardrobe is empty. Add clothing first!",
                    color=MUTED,
                )
            )
            return

        for item in clothes:

            checkbox = ft.Checkbox(
                label=(
                    f"{item['name']} • "
                    f"{item['category']} • "
                    f"{item.get('colour') or 'No colour'}"
                ),
                value=False,
                on_change=refresh_preview,
            )

            item_selection[item["clothing_id"]] = checkbox

            selection_area.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            get_image(item),
                            ft.Column(
                                [
                                    ft.Text(
                                        item["name"],
                                        weight=ft.FontWeight.BOLD,
                                        color=BROWN,
                                    ),
                                    ft.Text(
                                        item["category"],
                                        color=MUTED,
                                        size=12,
                                    ),
                                    checkbox,
                                ],
                                spacing=5,
                                expand=True,
                            ),
                        ],
                        spacing=12,
                    ),
                    bgcolor=WHITE,
                    padding=10,
                    border_radius=14,
                )
            )

    def load_saved_outfits():

        saved_area.controls.clear()

        with get_connection() as conn:
            rows = conn.execute("""
                SELECT
                    o.outfit_id,
                    o.outfit_name,
                    o.occasion,
                    c.clothing_id,
                    c.name,
                    c.category,
                    c.image_path
                FROM outfits o
                LEFT JOIN outfit_items oi
                    ON o.outfit_id = oi.outfit_id
                LEFT JOIN clothing c
                    ON oi.clothing_id = c.clothing_id
                ORDER BY o.created_at DESC, o.outfit_id DESC
            """).fetchall()

        outfits = {}

        for row in rows:

            outfit_id = row["outfit_id"]

            if outfit_id not in outfits:
                outfits[outfit_id] = {
                    "name": row["outfit_name"],
                    "occasion": row["occasion"],
                    "items": [],
                }

            if row["clothing_id"] is not None:
                outfits[outfit_id]["items"].append({
                    "clothing_id": row["clothing_id"],
                    "name": row["name"],
                    "category": row["category"],
                    "image_path": row["image_path"],
                })

        if not outfits:
            saved_area.controls.append(
                ft.Text(
                    "No saved outfits yet. Create your first look!",
                    color=MUTED,
                )
            )

        for outfit_id, outfit in outfits.items():

            photo_row = ft.Row(
                controls=[
                    get_image(item)
                    for item in outfit["items"]
                ],
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
            )

            def delete_outfit(oid):
                def handler(e):

                    with get_connection() as conn:
                        conn.execute(
                            "DELETE FROM outfits WHERE outfit_id = ?",
                            (oid,),
                        )

                    load_saved_outfits()
                    page.update()

                return handler

            def wear_outfit(oid):
                def handler(e):

                    try:
                        with get_connection() as conn:

                            item_rows = conn.execute("""
                                SELECT clothing_id
                                FROM outfit_items
                                WHERE outfit_id = ?
                            """, (oid,)).fetchall()

                            if not item_rows:
                                status.value = "This outfit has no clothing items."
                                page.update()
                                return

                            for item_row in item_rows:

                                clothing_id = item_row["clothing_id"]

                                conn.execute("""
                                    INSERT INTO wear_history
                                    (outfit_id, clothing_id)
                                    VALUES (?, ?)
                                """, (oid, clothing_id))

                                conn.execute("""
                                    UPDATE clothing
                                    SET wear_count = wear_count + 1
                                    WHERE clothing_id = ?
                                """, (clothing_id,))

                        status.value = "Outfit marked as worn! 🤎"

                    except Exception as error:
                        status.value = f"Could not record outfit: {error}"

                    page.update()

                return handler

            saved_area.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                outfit["name"],
                                size=19,
                                weight=ft.FontWeight.BOLD,
                                color=BROWN,
                            ),
                            ft.Text(
                                f"Occasion: {outfit['occasion'] or 'Not specified'}",
                                size=13,
                                color=MUTED,
                            ),
                            photo_row,
                            ft.Text(
                                f"{len(outfit['items'])} clothing pieces",
                                size=12,
                                color=MUTED,
                            ),
                            ft.Row(
                                [
                                    ft.Button(
                                        content="Wear Outfit",
                                        bgcolor=ACCENT,
                                        color=WHITE,
                                        on_click=wear_outfit(outfit_id),
                                    ),
                                    ft.TextButton(
                                        "Delete",
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        on_click=delete_outfit(outfit_id),
                                    ),
                                ],
                                wrap=True,
                            ),
                        ],
                        spacing=10,
                    ),
                    bgcolor=WHITE,
                    padding=16,
                    border_radius=18,
                )
            )

    def save_outfit(e):

        name = (outfit_name.value or "").strip()

        if not name:
            status.value = "Please enter an outfit name."
            page.update()
            return

        selected = get_selected_items()

        if len(selected) < 2:
            status.value = "Select at least two clothing items."
            page.update()
            return

        try:
            with get_connection() as conn:

                cursor = conn.execute("""
                    INSERT INTO outfits (outfit_name, occasion)
                    VALUES (?, ?)
                """, (name, occasion.value or "Casual"))

                outfit_id = cursor.lastrowid

                conn.executemany("""
                    INSERT INTO outfit_items (outfit_id, clothing_id)
                    VALUES (?, ?)
                """, [
                    (outfit_id, item["clothing_id"])
                    for item in selected
                ])

            outfit_name.value = ""

            for checkbox in item_selection.values():
                checkbox.value = False

            refresh_preview()

            status.value = "Outfit saved successfully! 🤎"

            load_saved_outfits()
            page.update()

        except Exception as error:
            status.value = f"Could not save outfit: {error}"
            page.update()

    build_item_selection()
    load_saved_outfits()

    return ft.Column(
        [
            ft.Text(
                "Outfit Planner",
                size=30,
                weight=ft.FontWeight.BOLD,
                color=BROWN,
            ),
            ft.Text(
                "Create looks using your own wardrobe.",
                color=MUTED,
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Create an Outfit",
                            size=21,
                            weight=ft.FontWeight.BOLD,
                            color=BROWN,
                        ),
                        outfit_name,
                        occasion,
                        ft.Text(
                            "SELECT YOUR CLOTHING",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=MUTED,
                        ),
                        selection_area,
                        ft.Divider(color="#E8DFD7"),
                        ft.Text(
                            "YOUR OUTFIT PREVIEW",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=MUTED,
                        ),
                        preview_area,
                        ft.Button(
                            content="Save Outfit",
                            bgcolor=ACCENT,
                            color=WHITE,
                            on_click=save_outfit,
                        ),
                        status,
                    ],
                    spacing=12,
                ),
                bgcolor="#F0E9E2",
                padding=18,
                border_radius=18,
            ),
            ft.Text(
                "My Saved Outfits",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=BROWN,
            ),
            saved_area,
        ],
        spacing=14,
        scroll=ft.ScrollMode.AUTO,
    )
