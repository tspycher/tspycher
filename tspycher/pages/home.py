import pynecone as pc
from . import BasePage
from ..state import State


class PageHome(BasePage):
    def private_content(self) -> pc.Component:
        return pc.vstack(
            pc.hstack(
                pc.vstack(
                    pc.heading("Tom Spycher", size="4xl"),
                    pc.heading(State.my_age, " years old", size="2xl"),
                    pc.container(
                        pc.text(
                            "Father of two kids, private pilot, Enthusiastic about cars and planes"
                            ),
                        font_size="2em"
                    ),
                ),
                pc.image(
                    src="https://live.staticflickr.com/2904/33900477071_e0eb372192_b.jpg",
                    width="300px",
                    height="500px",
                    border_radius="10px 30px",
                    border="2px solid #555",
                    object_fit="cover",
                    object_position="10% 0"
                )
            ),
            pc.container(
                pc.text(
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

    def professional_content(self) -> pc.Component:
        def skill_slider(name:str, value:int):
            return pc.vstack(
                pc.heading(name),
                pc.slider(value=value, is_read_only=True, min_=1, max_=10),
                width="100%",
            )

        return pc.vstack(
            pc.hstack(
                pc.image(
                    src="https://live.staticflickr.com/2904/33900477071_e0eb372192_b.jpg",
                    width="300px",
                    height="500px",
                    border_radius="10px 30px",
                    border="2px solid #555",
                    object_fit="cover",
                    object_position="10% 0"
                ),
                pc.vstack(
                    pc.heading("Thomas Spycher", size="4xl"),
                    pc.container(
                        pc.text(
                            "Not not an Architect, not not a Programmer, not not a Scrum Master, not not a Product Owner and certainly not not a CTO but not purely theoretical and certainly not lazy"),
                        font_size="2em"
                    ),
                ),
            ),
            pc.container(
                pc.text(
                    "Been working for and in Startups, in several postions as CTO. Part of mergers worked a couple of times for bigass corporates.",
                    "Bold and getting shit done mentality.",
                    "Introvert by heart, trained extrovert",
                ),
                pc.grid(
                    pc.grid_item(skill_slider("Kubernetes", 7)),
                    pc.grid_item(skill_slider("Kubernetes", 7)),
                    pc.grid_item(skill_slider("Kubernetes", 7)),
                    pc.grid_item(skill_slider("Kubernetes", 7)),
                    pc.grid_item(skill_slider("Kubernetes", 7)),
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

    def body_content(self) -> pc.Component:
        def _wrap_body(content):
            return pc.container(
                content,
                #center_content=True,
                padding="2em",
                width="100%",
                bg="lightblue",
                border_radius="25px"
            )

        return pc.container(
            pc.tabs(
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
