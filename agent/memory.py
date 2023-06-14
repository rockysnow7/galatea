from typing import Any
from agent.module import Module
from agent.load_openai import openai

import os
import json
import time
import numpy as np


class MemoryModule(Module):
    def __init__(self) -> None:
        super().__init__()

        if not os.path.exists("agent/modules/memory"):
            os.mkdir("agent/modules/memory")

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

    def save_memory(
        self,
        text: str,
        embedding: list[float],
        current_state: dict[str, float],
    ) -> None:
        next_index = len(os.listdir("agent/modules/memory"))
        with open(f"agent/modules/memory/{next_index}.json", "w+") as f:
            json.dump({
                "content": text,
                "timestamp": time.time(),
                "embedding": embedding,
                "state": current_state,
            }, f, indent=4)

    def process(
        self,
        text: str,
        current_state: dict[str, float],
        num_results: int = 5,
    ) -> tuple[list[dict[str, Any]], dict[str, float] | None]:
        text_embedding = self.__get_embedding(text)
        memories = []
        if num_results:
            for name in os.listdir("agent/modules/memory"):
                with open(f"agent/modules/memory/{name}", "r") as f:
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

        if num_results and memories:
            states = [memory["state"] for memory in memories]
            print(states)
            mean_state = {key: sum(state[key] for state in states) / len(states) for key in states[0]}
        else:
            mean_state = None

        self.save_memory(text, text_embedding, current_state)

        return memories, mean_state
