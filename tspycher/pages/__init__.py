import reflex as rx


class BasePage(object):
    def _header(self) -> rx.Component:
        # return rx.container(
        # rx.menu(
        #    rx.menu_button(rx.icon(tag="hamburger")),
        #    rx.menu_list(
        #        rx.menu_item("Social Media", is_focusable=False, is_disabled=True),
        #        rx.menu_item(rx.link("LinkedIn ", rx.icon(tag="external_link"), href="https://www.linkedin.com/in/tspycher84/", is_external=True)),
        #        rx.menu_item(rx.link("Instagram ", rx.icon(tag="external_link"), href="https://www.instagram.com/tspycher/", is_external=True)),
        #        rx.menu_divider(),
        #        rx.menu_item("API's", is_focusable=False, is_disabled=True),
        #        rx.menu_item(rx.link("LSZI API", href="http://localhost:8000/api/airfield/lszi", is_external=True)),
        #    ),
        # ),
        # rx.spacer(),
        # ,
        # width="100%",
        # height="10vh",
        # padding="1.0em"
        # )
        return rx.hstack(
            rx.box(
                width="33%",
                text_align="left",
            ),
            rx.box(
                width="33%",
                text_align="center",
            ),
            rx.box(
                rx.button(
                    rx.icon(tag="sun"),
                    on_click=rx.toggle_color_mode,
                    name="themechange"
                ),
                width="33%",
                text_align="right",
            ),
            center_content=True,
            width="100%",
            top=0,
            padding="2.0em",
            position="absolute"
        )

    def body(self) -> rx.Component:
        return rx.container(
            self._header(),
            self.body_content(),
            self._footer(),
            center_content=True,
            justifyContent="center",
            maxWidth="100vw",
            height="100vh",
            width="100vw",
            background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
        )

    def body_content(self) -> rx.Component:
        raise NotImplementedError()

    def _footer(self) -> rx.Component:
        return rx.vstack(
            rx.desktop_only(
                rx.box(
                    "This landing-page is so over-engineered but i had fun building it.",
                    text_align="center",
                    white_space="normal"
                )
            ),
            rx.desktop_only(
                rx.box(
                    "It's made by myself, build with ",
                    rx.link(rx.button("Reflex"), href="https://reflex.dev", is_external=True, name="reflex"),
                    " Framework, powered by ",
                    rx.link(rx.button("FastAPI"), href="https://fastapi.tiangolo.com", is_external=True,
                            name="fastapi"),
                    " and run with ",
                    rx.link(rx.button("Google Cloud Run"), href="https://cloud.google.com/run", is_external=True,
                            name="cloudrun"),
                    # " and run with ", rx.link(rx.button("AWS ECS"), href="https://aws.amazon.com/ecs/", is_external=True, name="ecs"),
                    " as a ",
                    rx.link(rx.button("Docker"), href="https://www.docker.com", is_external=True, name="docker"),
                    " image",
                    "... oh boy i love ",
                    rx.link(rx.button("Python"), href="https://www.python.org", is_external=True, name="python"),
                    text_align="center",
                    white_space="normal"
                )
            ),
            rx.mobile_and_tablet(
                rx.box(
                    "This landing-page is so over-engineered with",
                    rx.link(rx.button("Docker"), href="https://www.docker.com", is_external=True, name="docker"), ", ",
                    rx.link(rx.button("Google Cloud Run"), href="https://cloud.google.com/run", is_external=True,
                            name="cloudrun"), " and many more stuff. But i had fun building it.",
                    text_align="center",
                    white_space="normal"
                )
            ),

            center_content=True,
            width="100%",
            bottom=0,
            padding="2.0em",
            position="absolute",
            white_space="normal",
            display="flex",
            color="DimGrey"
        )


from .home import PageHome
from .landingpage import PageLandingpage
