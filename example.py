import random
import time

from gptpy2.chat_server import ChatServer

server = ChatServer(port=7788)
server.start()

for _ in range(10):
    time.sleep(10)
    prompt = str(random.randint(1, 10000)) + ' * ' + str(random.randint(1, 10000)) + ' = ?'
    print('>> ' + prompt)
    server.send(prompt)

server.join()