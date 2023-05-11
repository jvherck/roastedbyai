# RoastedByAI
This is an *unofficial* Python package that uses Selenium to communicate with 
https://roastedby.ai as the website doesn't have an official API.


---


## How to install
Run `pip install roastbyai` \
If that doesn't work, try `py -m pip install roastedbyai`


---


## Usage
Important note: the package uses Selenium, which means a browser will be 
opened!
```python
from roastedbyai import Conversation
from time import sleep

convo = Conversation()

user_input = input("Start by roasting the AI:\n>>> ")

response1 = convo.send(user_input)
while response1 is None:
    sleep(1)

print(response1)
sleep(5)

user_input = input("Roast the AI again:\n>>> ")

response2 = convo.send(user_input)
while response2 is None:
    sleep(1)

print(response2)

convo.quit()
# This step isn't necessary, the moment you don't use the `convo` object 
# anymore, python will automatically handle it
```