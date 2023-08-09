import reflex as rx
from . import BasePage
from ..state import State


class PageHome(BasePage):
    def private_content(self) -> rx.Component:
        return rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading("Tom Spycher", size="4xl"),
                    rx.heading(State.my_age, " years old", size="2xl"),
                    rx.container(
                        rx.text(
                            "Father of two kids, private pilot, Enthusiastic about cars and planes"
                            ),
                        font_size="2em"
                    ),
                ),
                rx.image(
                    src="https://live.staticflickr.com/2904/33900477071_e0eb372192_b.jpg",
                    width="300px",
                    height="500px",
                    border_radius="10px 30px",
                    border="2px solid #555",
                    object_fit="cover",
                    object_position="10% 0"
                )
            ),
            rx.container(
                rx.text(
                    "Proud Father of two Kids (", State.ben_age, " and ", State.leia_age, " years old), Married. Retired Crossfiter (now fat again). ",
                    "I like my Coffee like my Metal, black. Enthusiastic about Cars and Airplanes. ",
                    "Where my World is about digital engeneering i'm very facinated by mechanical engineering in the form of Cars and Planes. ",
                    "Flying Taildraggers for leisure (still bad at landing them). I love beer and food. I hate boardgames! Star Wars is Awesome!",
                    "I need two matches to light up a bonfire... what does this tell you about me?",
                    "I like my car dirt smudged. Not that i don't care, it just feels so 'adventurous'. Talking about cars, I like the rocking of solid axels in the front and back and changing gears is and will allways be prefered manual.",
                ),
                font_size="1.25em",
                text_align="left",
            ),
            width="100%",

            spacing="1.5em",
        )

    def professional_content(self) -> rx.Component:
        def skill_slider(name:str, value:int):
            return rx.vstack(
                rx.heading(name),
                rx.slider(value=value, is_read_only=True, min_=1, max_=10),
                width="100%",
            )

        return rx.vstack(
            rx.hstack(
                rx.image(
                    src="https://live.staticflickr.com/2904/33900477071_e0eb372192_b.jpg",
                    width="300px",
                    height="500px",
                    border_radius="10px 30px",
                    border="2px solid #555",
                    object_fit="cover",
                    object_position="10% 0"
                ),
                rx.vstack(
                    rx.heading("Thomas Spycher", size="4xl"),
                    rx.container(
                        rx.text(
                            "Not not an Architect, not not a Programmer, not not a Scrum Master, not not a Product Owner and certainly not not a CTO but not purely theoretical and certainly not lazy"),
                        font_size="2em"
                    ),
                ),
            ),
            rx.container(
                rx.text(
                    "Been working for and in Startups, in several postions as CTO. Part of mergers worked a couple of times for bigass corporates.",
                    "Bold and getting shit done mentality.",
                    "Introvert by heart, trained extrovert",
                ),
                rx.grid(
                    rx.grid_item(skill_slider("Kubernetes", 7)),
                    rx.grid_item(skill_slider("Kubernetes", 7)),
                    rx.grid_item(skill_slider("Kubernetes", 7)),
                    rx.grid_item(skill_slider("Kubernetes", 7)),
                    rx.grid_item(skill_slider("Kubernetes", 7)),
                    template_columns="repeat(3, 1fr)",
                    h="10em",
                    width="100%",
                    gap=4,
                ),
                font_size="1.25em",
                text_align="left",
            ),
            width="100%",
            spacing="1.5em",
        )

    def body_content(self) -> rx.Component:
        def _wrap_body(content):
            return rx.container(
                content,
                #center_content=True,
                padding="2em",
                width="100%",
                bg="lightblue",
                border_radius="25px"
            )

        return rx.container(
            rx.tabs(
                items=[
                    ("Professional", _wrap_body(self.professional_content())),
                    ("Private", _wrap_body(self.private_content())),
                ],
                variant="soft-rounded",
                align="center",
                is_fitted=True,
                is_lazy=True,
            ),
            width="100%",
            height="80vh",
        )
