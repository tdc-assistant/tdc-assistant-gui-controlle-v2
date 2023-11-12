from typing import TypedDict, Union, Literal

Component = Union[Literal["public chat"], Literal["code editor"]]


class Message(TypedDict):
    content: str
    component: Component
