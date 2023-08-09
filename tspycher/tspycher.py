import reflex as rx
from . import State
from .api import api_airfield, api_status, api_teltonika_gps
from .pages import PageHome, PageLandingpage


page_home = PageHome()
page_landing = PageLandingpage()

app = rx.App(
    state=State,
)
app.add_page(page_landing.body, route="/", title="Tom Spycher", description="Welcome on my over-engineered website", on_load=rx.toggle_color_mode)
app.add_page(page_home.body, route="/home/", title="Tom Spycher", description="Welcome on my over-engineered website", on_load=rx.toggle_color_mode)

app.api.add_api_route("/", api_status)
app.api.add_api_route("/teltonika", api_teltonika_gps, methods=["POST"])
app.api.add_api_route("/airfield/{name}", api_airfield)

app.compile()
