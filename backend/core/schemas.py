from typing_extensions import Literal
from typing import Union, List
from pydantic import BaseModel


class SchedulepresenceSubscribe(BaseModel):
    event: Literal["schedule_presence"]
    team_id: int


class Subscribe(BaseModel):
    type: Literal["subscribe"]
    data: SchedulepresenceSubscribe


class SchedulepresenceUser(BaseModel):
    id: int
    avatar_url: str
    email: str


class PublishSchedulepresence(BaseModel):
    event: Literal["schedule_presence"]
    team_id: int
    users: List[SchedulepresenceUser]


class Publish(BaseModel):
    type: Literal["publish"]
    data: PublishSchedulepresence


class PubSub(BaseModel):
    message: Union[Subscribe, Publish]
