
import flet as ft

from wardrobe import show_wardrobe
from outfits import show_outfits
from analytics import show_analytics


BG = "#F7F4EF"
BROWN = "#332B27"
ACCENT = "#B77B62"
MUTED = "#8B8178"
WHITE = "#FFFFFF"


def main(page: ft.Page):

    page.title = "ReWear"
    page.bgcolor = BG
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    content = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    def show_home(e=None):

        content.controls.clear()

        content.controls.extend([
            ft.Text(
                "reWear.",
                size=34,
                weight=ft.FontWeight.BOLD,
                color=BROWN,
            ),
            ft.Text(
                "YOUR PERSONAL WARDROBE",
                size=10,
                color=MUTED,
            ),
            ft.Container(height=20),
            ft.Text(
                "Your style, your space.",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=BROWN,
            ),
            ft.Text(
                "Everything in your wardrobe, all in one place.",
                color=MUTED,
            ),
            ft.Container(height=20),

            ft.Container(
                content=ft.Column([
                    ft.Text("👗", size=28),
                    ft.Text(
                        "My Wardrobe",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=BROWN,
                    ),
                    ft.Text(
                        "Browse all your clothing pieces.",
                        color=MUTED,
                    ),
                    ft.Button(
                        "View Wardrobe →",
                        bgcolor=ACCENT,
                        color=WHITE,
                        on_click=show_wardrobe_page,
                    ),
                ], spacing=12),
                bgcolor=WHITE,
                padding=22,
                border_radius=18,
            ),

            ft.Container(
                content=ft.Column([
                    ft.Text("✨", size=28),
                    ft.Text(
                        "Outfit Planner",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=BROWN,
                    ),
                    ft.Text(
                        "Create new looks with your clothes.",
                        color=MUTED,
                    ),
                    ft.Button(
                        "Plan an Outfit →",
                        bgcolor=ACCENT,
                        color=WHITE,
                        on_click=show_outfits_page,
                    ),
                ], spacing=12),
                bgcolor=WHITE,
                padding=22,
                border_radius=18,
            ),

            ft.Container(
                content=ft.Column([
                    ft.Text("📊", size=28),
                    ft.Text(
                        "Wardrobe Insights",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=BROWN,
                    ),
                    ft.Text(
                        "See your wardrobe statistics and habits.",
                        color=MUTED,
                    ),
                    ft.Button(
                        "View Analytics →",
                        bgcolor=ACCENT,
                        color=WHITE,
                        on_click=show_analytics_page,
                    ),
                ], spacing=12),
                bgcolor=WHITE,
                padding=22,
                border_radius=18,
            ),
        ])

        page.update()

    def show_wardrobe_page(e=None):

        content.controls.clear()
        content.controls.append(show_wardrobe(page))
        page.update()

    def show_outfits_page(e=None):

        content.controls.clear()
        content.controls.append(show_outfits(page))
        page.update()

    def show_analytics_page(e=None):

        content.controls.clear()
        content.controls.append(show_analytics(page))
        page.update()

    navigation = ft.Row(
        controls=[
            ft.TextButton("⌂ Home", on_click=show_home),
            ft.TextButton("👗 Wardrobe", on_click=show_wardrobe_page),
            ft.TextButton("✨ Outfits", on_click=show_outfits_page),
            ft.TextButton("📊 Insights", on_click=show_analytics_page),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        wrap=True,
    )

    page.add(
        content,
        ft.Divider(color="#E8DFD7"),
        navigation,
    )

    show_home()


ft.run(main)
