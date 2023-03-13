import flet as ft
import os


# set Flet path to an empty string to serve at the root URL (e.g., https://lizards.ai/)
# or a folder/path to serve beneath the root (e.g., https://lizards.ai/ui/path
DEFAULT_FLET_PATH = ''  # or 'ui/path'
DEFAULT_FLET_PORT = 8502


def main(page: ft.Page):
    page.title = "You Enjoy Mychatbot"
    page.add(ft.Text("Reba put a stopper in the bottom of the tub"))


if __name__ == "__main__":
    print("Starting Flet")
    flet_path = os.getenv("FLET_PATH", DEFAULT_FLET_PATH)
    flet_port = int(os.getenv("FLET_PORT", DEFAULT_FLET_PORT))
    ft.app(name=flet_path, target=main, view=ft.WEB_BROWSER, port=flet_port)