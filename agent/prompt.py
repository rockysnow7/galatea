from typing import Any
from agent.module import Module

import os
import json


class PromptModule(Module):
    def __init__(self) -> None:
        super().__init__()

    def __get_intro(self, bot_name: str, user_name: str) -> str:
        with open("agent/modules/prompt/intro.txt", "r") as f:
            text = f.read()
        text = text.format(
            bot_name=bot_name,
            user_name=user_name,
        )

        return text

    def __get_example_chat(
        self,
        bot_name: str,
        user_name: str,
        mood_name: str,
    ) -> str:
        with open(f"agent/modules/prompt/example-chats/{mood_name}.txt", "r") as f:
            text = f.read()
        text = text.format(
            bot_name=bot_name,
            user_name=user_name,
        )

        return text

    def __get_example_json(
        self,
        bot_name: str,
        user_name: str,
        mood_name: str,
    ) -> str:
        # TODO: add all moods

        #with open(f"modules/prompt/example-json/{mood_name}.txt", "r") as f:
        #    text = f.read()

        with open(f"agent/modules/prompt/example-json/neutral.txt", "r") as f:
            text = f.read()
        text = text.format(
            bot_name=bot_name,
            user_name=user_name,
        )

        return text

    def __get_mood(self, bot_name: str, mood_name: str) -> str:
        with open(f"agent/modules/prompt/mood/{mood_name}.txt", "r") as f:
            text = f.read()
        text = text.format(bot_name=bot_name)

        return text

    def __get_memories(
        self,
        bot_name: str,
        memories: list[dict[str, Any]],
    ) -> str:
        memories_formatted = ""
        for memory in memories:
            memories_formatted += f"- {memory['content']}\n"
        memories_formatted = memories_formatted.strip()

        with open(f"agent/modules/prompt/memories.txt", "r") as f:
            text = f.read()
        text = text.format(
            bot_name=bot_name,
            memories=memories_formatted,
        )

        return text

    def __get_messages(
        self,
        bot_name: str,
        user_name: str,
        messages: list[dict[str, Any]],
    ) -> str:
        messages_formatted = ""
        for message in messages:
            messages_formatted += f"{message['sender']}: {message['content']}\n"
        messages_formatted = messages_formatted.strip()

        with open(f"agent/modules/prompt/messages.txt", "r") as f:
            text = f.read()
        text = text.format(
            bot_name=bot_name,
            user_name=user_name,
            messages=messages_formatted,
        )

        return text

    def __get_respond(self, bot_name: str) -> str:
        with open(f"agent/modules/prompt/respond.txt", "r") as f:
            text = f.read()
        text = text.format(bot_name=bot_name)

        return text

    def process(
        self,
        bot_name: str,
        user_name: str,
        mood_name: str,
        memories_list: list[dict[str, Any]],
        messages_list: list[dict[str, Any]],
    ) -> str:
        intro = self.__get_intro(bot_name, user_name)
        example_chat = self.__get_example_chat(bot_name, user_name, mood_name)
        example_json = self.__get_example_json(bot_name, user_name, mood_name)
        mood = self.__get_mood(bot_name, mood_name)
        memories = self.__get_memories(bot_name, memories_list)
        messages = self.__get_messages(bot_name, user_name, messages_list)
        respond = self.__get_respond(bot_name)

        with open("agent/modules/prompt/prompt.txt", "r") as f:
            text = f.read()
        text = text.format(
            intro=intro,
            example_chat=example_chat,
            example_json=example_json,
            mood=mood,
            memories=memories or "<none>",
            messages=messages or "<none>",
            respond=respond,
        )

        return text
