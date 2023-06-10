from typing import Any
from module import Module
from load_openai import openai

import os
import json
import time
import numpy as np


class MemoryModule(Module):
    def __init__(self) -> None:
        super().__init__()

        if not os.path.exists("modules/memory"):
            os.mkdir("modules/memory")

    def __get_embedding(self, text: str) -> list[float]:
        text = text.encode(encoding="ascii", errors="ignore").decode()
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002",
        )
        embedding = response["data"][0]["embedding"]

        return embedding

    def __cos_similarity(self, a: list[float], b: list[float]) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def process(
        self,
        text: str,
        num_results: int = 5,
    ) -> list[dict[str, Any]]:
        text_embedding = self.__get_embedding(text)
        if num_results != 0:
            memories = []
            for name in os.listdir("modules/memory"):
                with open(f"modules/memory/{name}", "r") as f:
                    memory = json.load(f)
                memories.append(memory)
            memories = sorted(
                memories,
                key=lambda memory: self.__cos_similarity(
                    memory["embedding"],
                    text_embedding,
                ),
            )
            memories = memories[:num_results]

        next_index = len(os.listdir("modules/memory"))
        with open(f"modules/memory/{next_index}.json", "w+") as f:
            json.dump({
                "content": text,
                "timestamp": time.time(),
                "embedding": text_embedding,
            }, f, indent=4)
        return memories if num_results else []
