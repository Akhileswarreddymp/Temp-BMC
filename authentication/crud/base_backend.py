from pydantic import BaseModel
from sqlmodel import Session


class BaseBackend:
    def __init__(self, session: Session, concrete_type: type[BaseModel]) -> None:
        self.session = session
        self.concrete_type = concrete_type
