from typing import Any
from agent.module import Module
from agent.rewriter import RewriterModule
from agent.load_openai import openai

import os
import json
import time


class MessageModule(Module):
    def __init__(self, rewriter: RewriterModule = RewriterModule()) -> None:
        super().__init__()
        self.__rewriter = rewriter

        if not os.path.exists("agent/modules/messages"):
            os.mkdir("agent/modules/messages")

    def save_message(self, text: str, sender: str) -> None:
        next_index = len(os.listdir("agent/modules/messages"))
        with open(f"agent/modules/messages/{next_index}.json", "w+") as f:
            json.dump({
                "content": text,
                "sender": sender,
                "timestamp": time.time(),
            }, f, indent=4)

    def get_recent_messages(self, num_messages: int) -> list[dict[str, Any]]:
        names = os.listdir("agent/modules/messages")
        names = sorted(names, key=lambda name: int(name.split(".")[0]))
        names = names[-num_messages:]

        messages = []
        for name in names:
            with open(f"agent/modules/messages/{name}", "r") as f:
                messages.append(json.load(f))
        return messages

    def process(
        self,
        bot_name: str,
        user_name: str,
        prompt: str,
    ) -> dict[str, str | list[str]]:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=1.0,
            stop=[f"{bot_name}:", f"{user_name}:"],
            max_tokens=1000,
        )
        response = response["choices"][0]["text"].strip()
        response_dict = json.loads(response)
        response_dict["response"] = self.__rewriter.process(response_dict["response"])

        return response_dict
