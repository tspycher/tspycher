import reflex as rx
from . import BasePage
from tspycher.state import State


class PageLandingpage(BasePage):
    def body_content(self) -> rx.Component:
        return rx.container(
            rx.vstack(
                rx.heading("Tom Spycher", size="4xl"),
                rx.text(f"Proud Father of a Son an Daughter, " + State.my_age + " years old, happily married, enthusiastic about cars and planes, IT geek, retired crossfitter (now fat again), beer", size="4xl"),
            ),
            center_content=True,
            padding="100px",
            borderRadius="15px",
            boxShadow="0px 0px 200px #0d0f15"
        )
