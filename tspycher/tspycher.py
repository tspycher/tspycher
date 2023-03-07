import pynecone as pc
from .state import State
from .api import api_airfield
from .pages import PageHome, PageLandingpage


#page_home = PageHome()
page_landing = PageLandingpage()

app = pc.App(
    state=State,
)
app.add_page(page_landing.body, route="/")
app.api.add_api_route("/airfield/{name}", api_airfield)
app.compile()
