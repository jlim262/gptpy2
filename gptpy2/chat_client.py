import select
import socket
import sys
import signal
import argparse
from gptpy2.chatgpt import ChatGPT
from gptpy2.utils import *


class ChatClient:
    """A command line chat client using select"""

    def __init__(
        self,
        name,
        openai_key_path,
        host="localhost",
        port=7788,
    ):
        self.name = name
        self.connected = False
        self.host = host
        self.port = port

        # Initial prompt
        self.prompt = f"[{name}@{socket.gethostname()}]> "
        self.gpt = ChatGPT(secret_key_path=openai_key_path)

        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print(f"Now connected to chat server {self.host} port {self.port}")
            self.connected = True

            # Send my name...
            send(self.sock, "NAME: " + self.name)
            data = receive(self.sock)

            # Contains client address, set it
            addr = data.split("CLIENT: ")[1]
            self.prompt = "[" + "@".join((self.name, addr)) + "]> "
        except socket.error as e:
            print(
                f"Failed to connect to chat server {self.host} port {self.port} : {e}"
            )
            sys.exit(1)

    def cleanup(self):
        """Close the connection and wait for the thread to terminate."""
        self.sock.close()

    def run(self):
        """Chat client main loop"""
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                # Wait for input from stdin and socket
                readable, writeable, exceptional = select.select([0, self.sock], [], [])

                for sock in readable:
                    if sock == 0:
                        inp = sys.stdin.readline().strip()

                        # inp = input("Press Enter to test or input 'e' to exit >> ")
                        if inp == "e":
                            self.sr.listen()
                            data = self.sr.sr_openai_whisper("output")
                        else:
                            data = inp

                        # if data:
                        data = self.gpt.chat(data)
                        send(self.sock, data)
                    elif sock == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print("Client shutting down.")
                            self.connected = False
                            break
                        else:
                            data = self.gpt.chat(data)
                            send(self.sock, data)
                            sys.stdout.write(data + "\n")
                            sys.stdout.flush()

            except KeyboardInterrupt:
                print(" Client interrupted. " "")
                self.cleanup()
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", action="store", dest="name", required=True)
    parser.add_argument("--port", action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()

    port = given_args.port
    name = given_args.name

    # client = ChatClient(host="192.168.1.35", name=name, port=port)
    client = ChatClient(name=name, port=port)
    client.run()
