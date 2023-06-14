from agent.module import Module


class RewriterModule(Module):
    def __init__(self) -> None:
        ...

    def process(self, response: str) -> str:
        return response
