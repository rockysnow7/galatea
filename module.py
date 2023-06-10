from typing import Any
from abc import ABC, abstractmethod

import os


class Module(ABC):
    def __init__(self) -> None:
        if not os.path.exists("modules"):
            os.mkdir("modules")

    @abstractmethod
    def process(self) -> Any:
        pass
