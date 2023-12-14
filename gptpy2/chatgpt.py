# import subprocess
# cmd = ["pip", "install", "openai"]
# subprocess.call(cmd)

import numpy as np
import random
import openai
import ast
import os

from aiohttp import ClientSession
from tqdm import tqdm
import time


from openai import OpenAI


from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


class ChatGPT(object):
    def __init__(
        self,
        secret_key_path,
        robot_name="Assistant Robot",
        instruction="",
        model="gpt-4-1106-preview",
        temperature=0.4,
    ):
        api_key = self.read_secret_key(secret_key_path)
        self.client = OpenAI(
            api_key=api_key,
        )

        # openai.aiosession.set(ClientSession())
        self.model = model
        self.temperature = temperature
        self.chat_history = []
        self.delay_in_seconds = 0.1
        self.robot_name = robot_name
        # self.set_instruction(instruction)
        self.instruction = instruction

        self.assistant = self.client.beta.assistants.create(
            name="Robot Assistant",
            instructions="You are a versatile robotic assistant designed for various tasks in the University of Auckland. Deliver a concise response in a single sentence.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview",
        )

    # Function to read the secret key from the file
    def read_secret_key(self, file_path):
        try:
            # Open the file in read mode
            with open(file_path, "r") as file:
                # Read the secret key
                secret_key = file.read().strip()
                return secret_key
        except FileNotFoundError:
            return "File not found. Please check the file path."
        except Exception as e:
            return f"An error occurred: {e}"

    def set_instruction(self, instruction):
        msg = {"role": "system", "content": instruction}
        self.chat_history.append(msg)

    def append_reply(self, content):
        msg = {"role": "assistant", "content": f"{self.robot_name}: {content}"}
        self.chat_history.append(msg)

    def chat(self, content):
        context = "Chat History: "
        for s in self.chat_history:
            context += s
            context += "\n"

        thread = self.client.beta.threads.create()

        msg = f"""
{context}
---
{content}    
        """

        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=msg,
        )
        self.chat_history.append(content)

        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id,
            instructions=self.instruction,
        )

        while True:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )

            if run.status == "completed":
                messages = self.client.beta.threads.messages.list(thread_id=thread.id)
                received_msg = messages.data[0].content[0].text.value
                self.chat_history.append(received_msg)
                return received_msg
            elif run.status == "queued" or run.status == "in_progress":
                time.sleep(self.delay_in_seconds)
            else:
                break

        return "error"

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def get_completion_from_messages(self, messages, temperature):
        # max number of concurrent requests
        # async with request_semaphore: Sleep for the delay
        time.sleep(self.delay_in_seconds)
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=temperature,  # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]


if __name__ == "__main__":
    gpt = ChatGPT(secret_key_path="secret_key.txt")
    while True:
        msg = input("msg: ")
        if msg == "q":
            break
        # elif msg == "l":
        #     print(gpt.messages)
        else:
            received_msg = gpt.chat(msg)
            print(received_msg)
