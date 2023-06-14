from agent.module import Module

import os
import json
import math


MOODS = {
    "depressed": {
        "happiness": -5.0,
        "energy": -5.0,
    },
    "tired": {
        "happiness": 0.0,
        "energy": -5.0,
    },
    "chill": {
        "happiness": 5.0,
        "energy": -5.0,
    },
    "sad": {
        "happiness": -5.0,
        "energy": 0.0,
    },
    "neutral": {
        "happiness": 0.0,
        "energy": 0.0,
    },
    "happy": {
        "happiness": 5.0,
        "energy": 0.0,
    },
    "anxious": {
        "happiness": -5.0,
        "energy": 5.0,
    },
    "focused": {
        "happiness": 0.0,
        "energy": 5.0,
    },
    "excited": {
        "happiness": 5.0,
        "energy": 5.0,
    },
}


class EmotionModule(Module):
    def __init__(self) -> None:
        super().__init__()

        if not os.path.exists("agent/modules/emotion"):
            info = {
                "current": {
                    "happiness": 0.0,
                    "energy": 0.0,
                },
                "dynamics": {
                    "default": {
                        "happiness": 0.0,
                        "energy": -5.0,
                    },
                    "movement_speed": 0.2,
                },
            }

            os.mkdir("agent/modules/emotion")
            with open("agent/modules/emotion/state.json", "w+") as f:
                json.dump(info, f, indent=4)

    def __get_default_state(self) -> dict[str, float]:
        with open("agent/modules/emotion/state.json", "r") as f:
            info = json.load(f)
        return info["dynamics"]["default"]

    def get_current_state(self) -> dict[str, float]:
        with open("agent/modules/emotion/state.json", "r") as f:
            info = json.load(f)
        return info["current"]

    def __get_value(self, name: str) -> float:
        with open("agent/modules/emotion/state.json", "r") as f:
            info = json.load(f)
        return info["dynamics"][name]

    def __save_state(self, state: dict[str, float]) -> None:
        with open("agent/modules/emotion/state.json", "r") as f:
            info = json.load(f)
        info["current"] = state

        with open("agent/modules/emotion/state.json", "w") as f:
            json.dump(info, f, indent=4)

    def __distance(self, a: tuple[float, ...], b: tuple[float, ...]) -> float:
        return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(len(a))))

    def get_mood_name(self) -> str:
        state_values = tuple(self.get_current_state().values())
        moods_distances = {mood_name: self.__distance(state_values, list(mood.values())) for mood_name, mood in MOODS.items()}

        return min(moods_distances, key=lambda name: moods_distances[name])

    def update_state(
        self,
        new_mood: str,
        mean_memory_state: dict[str, float],
    ) -> None:
        default_state = self.__get_default_state()
        current_state = self.get_current_state()
        new_mood_state = MOODS[new_mood]
        movement_speed = self.__get_value("movement_speed")

        for key in current_state:
            current_state[key] += (default_state[key] - current_state[key]) * movement_speed
            current_state[key] += (new_mood_state[key] - current_state[key]) * movement_speed
            if mean_memory_state is not None:
                current_state[key] += (mean_memory_state[key] - current_state[key]) * movement_speed
        self.__save_state(current_state)

    def process(self) -> None:
        pass
