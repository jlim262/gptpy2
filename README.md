# gptpy2
gptpy2 is a straightforward socket server, designed to work with python2. It enables the sending of messages to [gpt clients](https://github.com/jlim262/gptpy3) that are connected to it.

## Prerequisites
Before beginning, ensure that you have Python 2.7 installed on your system.

## Installing gptpy2
To install gptpy2, clone the GitHub repository and install it using the setup script:
```
git clone git@github.com:jlim262/gptpy2.git
cd gptpy2
python setup.py install
```

## Usage Example
To use gptpy2, simply import the ChatServer class, create an instance with specified host and port, and then call the `start()` method. 
```python
from gptpy2.chat_server import ChatServer

server = ChatServer(host='localhost', port=7788)
server.start()
```

Here's a basic example demonstrating how to send messages to clients:

```python
import random
import time
from gptpy2.chat_server import ChatServer

server = ChatServer(host='localhost', port=7788)
server.start()

# Sending random math questions to clients
for _ in range(10):
    time.sleep(10)
    prompt = str(random.randint(1, 10000)) + ' * ' + str(random.randint(1, 10000)) + ' = ?'
    print('>> ' + prompt)
    server.send(prompt)

server.join()
```
In this example, the server sends out random multiplication questions to clients every 10 seconds.
