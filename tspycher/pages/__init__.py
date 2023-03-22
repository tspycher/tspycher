import pynecone as pc


class BasePage(object):
    def _header(self) -> pc.Component:
        # return pc.container(
        # pc.menu(
        #    pc.menu_button(pc.icon(tag="hamburger")),
        #    pc.menu_list(
        #        pc.menu_item("Social Media", is_focusable=False, is_disabled=True),
        #        pc.menu_item(pc.link("LinkedIn ", pc.icon(tag="external_link"), href="https://www.linkedin.com/in/tspycher84/", is_external=True)),
        #        pc.menu_item(pc.link("Instagram ", pc.icon(tag="external_link"), href="https://www.instagram.com/tspycher/", is_external=True)),
        #        pc.menu_divider(),
        #        pc.menu_item("API's", is_focusable=False, is_disabled=True),
        #        pc.menu_item(pc.link("LSZI API", href="http://localhost:8000/api/airfield/lszi", is_external=True)),
        #    ),
        # ),
        # pc.spacer(),
        # ,
        # width="100%",
        # height="10vh",
        # padding="1.0em"
        # )
        return pc.hstack(
            pc.box(
                width="33%",
                text_align="left",
            ),
            pc.box(
                width="33%",
                text_align="center",
            ),
            pc.box(
                pc.button(
                    pc.icon(tag="sun"),
                    on_click=pc.toggle_color_mode,
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

    def body(self) -> pc.Component:
        return pc.container(
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

    def body_content(self) -> pc.Component:
        raise NotImplementedError()

    def _footer(self) -> pc.Component:
        return pc.vstack(
            pc.desktop_only(
                pc.box(
                    "This landing-page is so over-engineered but i had fun building it.",
                    text_align="center",
                    white_space="normal"
                )
            ),
            pc.desktop_only(
                pc.box(
                    "It's made by myself, build with ",
                    pc.link(pc.button("pynecone"), href="https://pynecone.io", is_external=True, name="pynecone"),
                    " Framework, powered by ",
                    pc.link(pc.button("FastAPI"), href="https://fastapi.tiangolo.com", is_external=True,
                            name="fastapi"),
                    " and run with ",
                    pc.link(pc.button("Google Cloud Run"), href="https://cloud.google.com/run", is_external=True,
                            name="cloudrun"),
                    # " and run with ", pc.link(pc.button("AWS ECS"), href="https://aws.amazon.com/ecs/", is_external=True, name="ecs"),
                    " as a ",
                    pc.link(pc.button("Docker"), href="https://www.docker.com", is_external=True, name="docker"),
                    " image",
                    "... oh boy i love ",
                    pc.link(pc.button("Python"), href="https://www.python.org", is_external=True, name="python"),
                    text_align="center",
                    white_space="normal"
                )
            ),
            pc.mobile_and_tablet(
                pc.box(
                    "This landing-page is so over-engineered with",
                    pc.link(pc.button("Docker"), href="https://www.docker.com", is_external=True, name="docker"), ", ",
                    pc.link(pc.button("Google Cloud Run"), href="https://cloud.google.com/run", is_external=True,
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
