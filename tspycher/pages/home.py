import reflex as rx
from . import BasePage
from tspycher.state import State


class PageHome(BasePage):

    def __wrapper(self, picture_url: str, text: rx.components):
        return rx.hstack(
            rx.image(
                src=picture_url,  # "https://live.staticflickr.com/2904/33900477071_e0eb372192_b.jpg",
                width="200px",
                height="300px",
                border_radius="10px 30px",
                border="2px solid #555",
                object_fit="cover",
                object_position="10% 0"
            ),
            rx.container(
                text,
                text_align="left",

            )
        )

    def _private_content(self) -> rx.Component:
        return self.__wrapper("https://live.staticflickr.com/2904/33900477071_e0eb372192_b.jpg",
                              rx.text(
                                  f"Proud Father of a Son an Daughter, " + State.my_age + " years old, happily married, enthusiastic about cars and planes, IT geek, retired crossfitter (now fat again), beer",
                                  size="4xl")
                              )

    def _business_content(self) -> rx.Component:
        return self.__wrapper("https://live.staticflickr.com/2904/33900477071_e0eb372192_b.jpg",
                              rx.container(
                                  rx.text(
                                      "Not not an Architect, not not a Programmer, not not a Scrum Master, not not a Product Owner and certainly not not a CTO but not purely theoretical and certainly not lazy", font_size="2em"),
                                  rx.text(
                                      "Been working for and in Startups, in several postions as CTO. Part of mergers worked a couple of times for bigass corporates.",
                                      "Bold and getting shit done mentality.",
                                      "Introvert by heart, trained extrovert",
                                  ),
                                  text_align="left",
                                  #font_size="2em"

                              )
                              )

    def body_content(self) -> rx.Component:
        return rx.container(
            rx.tabs(
                items=[
                    ("Professional", self._business_content()),
                    ("Private", self._private_content())
                ],
                variant="soft-rounded",
                align="center",
                is_fitted=True,
                is_lazy=True,
                height="100%",
                width="100%"
            ),
            width="80vw",
            height="50vh",
            center_content=True,
            padding="40px",
            borderRadius="15px",
            #boxShadow="0px 0px 200px #0d0f15"
        )

        """
        return rx.container(
            rx.vstack(
                rx.heading("Tom Spycherr", size="4xl"),
                self._private_content(),
            ),
            center_content=True,
            padding="100px",
            borderRadius="15px",
            boxShadow="0px 0px 200px #0d0f15"
        )"""
