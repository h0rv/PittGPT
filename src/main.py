import grequests
from gevent import monkey
monkey.patch_all(thread=False, select=False)

###

import os
from typing import Iterable

import instructor
from openai import OpenAI
from PittAPI import (
    course,
    dining,
    lab,
    laundry,
    library,
    news,
    people,
    shuttle,
    textbook,
)

from functions import Function, functions_handler


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def main() -> None:
    clear_screen()

    # print(get_pitt_json_schema())

    if True:
        client = instructor.from_openai(
            OpenAI(
                # base_url="http://localhost:11434/v1",
                # api_key="ollama",  # required, but unused
            ),
            mode=instructor.Mode.JSON,
        )

        funcs = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # model = "llama3:8b"
            messages=[
                {
                    "role": "user",
                    "content": "How busy is the laundry in Towers?",
                }
            ],
            response_model=Iterable[Function],
        )
        functions_handler(funcs)


if __name__ == "__main__":
    main()
