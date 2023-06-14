from typing import Any
from abc import ABC, abstractmethod

import os


class Module(ABC):
    def __init__(self) -> None:
        if not os.path.exists("agent/modules"):
            os.mkdir("agent/modules")

    @abstractmethod
    def process(self) -> Any:
        pass
