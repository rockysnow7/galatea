from emotion import EmotionModule
from memory import MemoryModule
from prompt import PromptModule
from message import MessageModule


class Agent:
    def __init__(self, bot_name: str, user_name: str) -> None:
        self.__bot_name = bot_name
        self.__user_name = user_name
        self.__emotion = EmotionModule()
        self.__memory = MemoryModule()
        self.__prompt = PromptModule()
        self.__message = MessageModule()

    def __respond(self, text: str) -> str:
        mood_name = self.__emotion.get_mood_name()
        print(self.__emotion.get_current_state())
        print(mood_name)

        related_memories = self.__memory.process(text)
        self.__message.save_message(text, self.__user_name)
        recent_messages = self.__message.get_recent_messages(5)

        prompt = self.__prompt.process(
            self.__bot_name,
            self.__user_name,
            mood_name,
            related_memories,
            recent_messages,
        )
        #print(prompt)
        response = self.__message.process(
            self.__bot_name,
            self.__user_name,
            prompt,
        )
        print(response)

        self.__message.save_message(response["response"], self.__bot_name)
        for note in response["notes"]:
            self.__memory.process(note, 0)
        self.__emotion.update_state(response["new mood"])

        return response["response"]

    def converse(self) -> None:
        while True:
            user_input = input(f"{self.__user_name}: ")
            if not user_input:
                break

            response = self.__respond(user_input)
            print(f"\n{self.__bot_name}: {response}\n")
