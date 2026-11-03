
import sys
from pathlib import Path

import flet as ft

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.database import get_connection

BG = "#F7F4EF"
BROWN = "#332B27"
ACCENT = "#B77B62"
MUTED = "#8B8178"
WHITE = "#FFFFFF"


def show_analytics(page: ft.Page):

    with get_connection() as conn:

        total_clothes = conn.execute(
            "SELECT COUNT(*) FROM clothing"
        ).fetchone()[0]

        total_outfits = conn.execute(
            "SELECT COUNT(*) FROM outfits"
        ).fetchone()[0]

        total_worn = conn.execute(
            "SELECT COUNT(*) FROM wear_history"
        ).fetchone()[0]

        most_worn = conn.execute("""
            SELECT name, wear_count
            FROM clothing
            ORDER BY wear_count DESC, name ASC
            LIMIT 1
        """).fetchone()

        least_worn = conn.execute("""
            SELECT name, wear_count
            FROM clothing
            ORDER BY wear_count ASC, name ASC
            LIMIT 1
        """).fetchone()

        categories = conn.execute("""
            SELECT category, COUNT(*) AS total
            FROM clothing
            GROUP BY category
            ORDER BY total DESC
        """).fetchall()

        history = conn.execute("""
            SELECT worn_date, COUNT(*) AS total
            FROM wear_history
            GROUP BY DATE(worn_date)
            ORDER BY DATE(worn_date) DESC
            LIMIT 7
        """).fetchall()

    def stat_card(number, label, emoji):

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(emoji, size=25),
                    ft.Text(
                        str(number),
                        size=27,
                        weight=ft.FontWeight.BOLD,
                        color=BROWN,
                    ),
                    ft.Text(label, size=13, color=MUTED),
                ],
                spacing=7,
            ),
            bgcolor=WHITE,
            padding=18,
            border_radius=18,
            col={"xs": 6, "md": 3},
        )

    category_cards = []

    for category in categories:

        category_cards.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            category["category"] or "Other",
                            weight=ft.FontWeight.BOLD,
                            color=BROWN,
                        ),
                        ft.Text(
                            str(category["total"]),
                            color=ACCENT,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                bgcolor=WHITE,
                padding=15,
                border_radius=12,
                col={"xs": 12, "sm": 6},
            )
        )

    history_cards = []

    for record in history:

        history_cards.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            str(record["worn_date"]),
                            color=BROWN,
                        ),
                        ft.Text(
                            f"{record['total']} wears",
                            color=ACCENT,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                bgcolor=WHITE,
                padding=14,
                border_radius=12,
            )
        )

    return ft.Column(
        [
            ft.Text(
                "Wardrobe Insights",
                size=30,
                weight=ft.FontWeight.BOLD,
                color=BROWN,
            ),
            ft.Text(
                "Get to know your wardrobe better.",
                color=MUTED,
            ),

            ft.Container(height=10),

            ft.ResponsiveRow(
                [
                    stat_card(total_clothes, "Clothing items", "👗"),
                    stat_card(total_outfits, "Saved outfits", "✨"),
                    stat_card(total_worn, "Wear records", "📅"),
                ],
                spacing=12,
                run_spacing=12,
            ),

            ft.Container(height=20),

            ft.Text(
                "CLOTHING INSIGHTS",
                size=12,
                weight=ft.FontWeight.BOLD,
                color=MUTED,
            ),

            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Most worn item", color=MUTED),
                        ft.Text(
                            (
                                f"{most_worn['name']} "
                                f"({most_worn['wear_count']} wears)"
                            ) if most_worn else "No clothing added yet",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=BROWN,
                        ),
                        ft.Divider(color="#E8DFD7"),
                        ft.Text("Least worn item", color=MUTED),
                        ft.Text(
                            (
                                f"{least_worn['name']} "
                                f"({least_worn['wear_count']} wears)"
                            ) if least_worn else "No clothing added yet",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=BROWN,
                        ),
                    ],
                    spacing=10,
                ),
                bgcolor=WHITE,
                padding=18,
                border_radius=18,
            ),

            ft.Container(height=15),

            ft.Text(
                "CATEGORY BREAKDOWN",
                size=12,
                weight=ft.FontWeight.BOLD,
                color=MUTED,
            ),

            ft.ResponsiveRow(
                category_cards,
                spacing=10,
                run_spacing=10,
            ),

            ft.Container(height=15),

            ft.Text(
                "RECENT WEAR HISTORY",
                size=12,
                weight=ft.FontWeight.BOLD,
                color=MUTED,
            ),

            *history_cards,

            ft.Container(
                content=ft.Text(
                    "Your wardrobe data updates as you add clothing "
                    "and record outfits you've worn.",
                    color=MUTED,
                    size=12,
                ),
                padding=15,
            ),
        ],
        spacing=14,
        scroll=ft.ScrollMode.AUTO,
    )
