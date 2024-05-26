import logging
import re
import openai 
import os

open_ai_key = os.getenv("OPENAI_KEY")
OPENAI_MODEL = "gpt-3.5-turbo-16k"
from .persistence import Persistence

class Chatbot:
    default_type_name: str = "Coach"
    default_type_role: str = "You are Dota 2 coach. You are here to help the user with their Dota 2 related questions. You analyze the user's recent games and provide feedback."
    default_instance_context: str = "The user is a Dota 2 player who wants to improve their gameplay. The user has provided their recent games for analysis."
    default_instance_starter: str = "Ask for the user's game ID to get their recent games."

    def __init__(
        self,
        database_file: str,
        type_id: str,
        user_id: str,
        type_name: str = None,
        type_role: str = None,
        instance_context: str = None,
        instance_starter: str = None,
    ):
        if database_file is None:
            raise RuntimeError("a database file path must be provided")
        if type_id is None:
            raise RuntimeError(
                "a type_id must be provided - either refer to an existing type or for a new type to be created"
            )
        if user_id is None:
            raise RuntimeError(
                "a user_id must be provided - either refer to an existing user or for a instance to be created"
            )

        if (type_name is not None or type_role is not None) and (
            type_name is None or type_role is None
        ):
            raise RuntimeError(
                "if any of type configuration is provided, then all of type configurations must be provided"
            )
        if (type_name is not None or type_role is not None) and (
            instance_context is None or instance_starter is None
        ):
            raise RuntimeError(
                "if a type is created, then one instance must be created along with it"
            )
        if (instance_context is not None or instance_starter is not None) and (
            instance_context is None or instance_starter is None
        ):
            raise RuntimeError(
                "if any of instance configuration is provided, then all of instance configurations must be provided"
            )

        self._persistence: Persistence = Persistence(
            database=database_file,
            type_id=type_id,
            user_id=user_id,
            type_name=type_name,
            type_role=type_role,
            instance_context=instance_context,
            instance_starter=instance_starter,
        )

    def _append_assistant(self, content: str) -> None:
        self._persistence.message_save(
            Persistence._assistant_label, content, cleanup=False
        )

    def _append_user(self, content: str) -> None:
        self._persistence.message_save(Persistence._user_label, content)

    def _openai(self) -> str:
        chat = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=self._persistence.messages_retrieve(with_system=True),
        )
        response: str = chat.choices[0].message.content
        logging.info(response)
        return response

    def _split_assistant_says(self, assistant_says: str) -> list[str]:
        # Regular expression to match <p>, <ul>, and <ol> elements
        pattern = re.compile(r"<p>.*?</p>|<ul>.*?</ul>|<ol>.*?</ol>")

        # Find all matches
        matches = pattern.findall(assistant_says)

        # If no matches, return the original string inside a list
        if not matches:
            return [assistant_says]

        
        parts = pattern.split(assistant_says)

        
        result = []
        for a, b in zip(parts, matches):
            if a:  
                result.append(a)
            result.append(b)  

        if len(parts) > len(matches):
            result.append(parts[-1])

        # Filter out any empty strings
        result = [r for r in result if r.strip()]

        return result

    def info_retrieve(self) -> dict[str, str]:
        return self._persistence.info_retrieve()

    def conversation_retrieve(self, with_system: bool = False) -> list[dict[str, str]]:
        return self._persistence.messages_retrieve(with_system)

    def start(self) -> str:
        self._persistence.starter_save()
        assistant_says: str = self._openai()
        assistant_says_list: list[str] = self._split_assistant_says(assistant_says)
        for assistant_says_list_entry in assistant_says_list:
            self._append_assistant(assistant_says_list_entry)
        return assistant_says_list

    def respond(self, user_says: str) -> list[str]:
        if user_says is None:
            raise RuntimeError("user_says must not be None")
        self._append_user(user_says)
        assistant_says: str = self._openai()
        assistant_says_list: list[str] = self._split_assistant_says(assistant_says)
        for assistant_says_list_entry in assistant_says_list:
            self._append_assistant(assistant_says_list_entry)
        return assistant_says_list

    def reset(self) -> None:
        self._persistence.reset()

    def resetDb(self) -> None:
        self._persistence.resetDb()

    def type_instances(self):
        return self._persistence.type_instances()    