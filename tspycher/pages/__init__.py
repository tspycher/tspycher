import pynecone as pc



class BasePage(object):
    def _header(self) -> pc.Component:
        return pc.flex(
            pc.menu(
                pc.menu_button(pc.icon(tag="hamburger")),
                pc.menu_list(
                    pc.menu_item("Social Media", is_focusable=False, is_disabled=True),
                    pc.menu_item(pc.link("LinkedIn ", pc.icon(tag="external_link"), href="https://www.linkedin.com/in/tspycher84/", is_external=True)),
                    pc.menu_item(pc.link("Instagram ", pc.icon(tag="external_link"), href="https://www.instagram.com/tspycher/", is_external=True)),
                    pc.menu_divider(),
                    pc.menu_item("API's", is_focusable=False, is_disabled=True),
                    pc.menu_item(pc.link("LSZI API", href="http://localhost:8000/api/airfield/lszi", is_external=True)),
                ),
            ),
            pc.spacer(),
            pc.button(
                pc.icon(tag="sun"),
                on_click=pc.toggle_color_mode,
            ),
            width="100%",
            height="10vh",
            padding="1.0em"
        )

    def body(self) -> pc.Component:
        return pc.container(
            #self._header(),
            self.body_content(),
            self._footer(),
            center_content=True,
            justifyContent="center",
            maxWidth="auto",
            height="100vh",

        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
        )

    def body_content(self) -> pc.Component:
        raise NotImplementedError()

    def _footer(self) -> pc.Component:
        return pc.center(
            "Made by myself, build with ", pc.link(pc.button("pynecone", is_external=True), href="https://pynecone.io", button=True),
            " Framework, powered by ", pc.link(pc.button("FastAPI", is_external=True), href="https://fastapi.tiangolo.com", button=True),
            " and run with ", pc.link(pc.button("Google Cloud Run", is_external=True), href="https://cloud.google.com/run", button=True),
            " as a ", pc.link(pc.button("Docker", is_external=True), href="https://www.docker.com", button=True), " image",
            "... oh boy i love ", pc.link(pc.button("Python", is_external=True), href="https://www.python.orgm", button=True),
            width="100%",
            height="10vh",
            bottom=0,
            padding="2.0em",
            position="absolute"
        )


from .home import PageHome
from .landingpage import PageLandingpage