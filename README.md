# RoastedByAI
This is an *unofficial* Python package for https://roastedby.ai to roast and get roasted by AI.


---


## How to install
Install the package using one of these pip commands (they both 
install the same package, the first command just does not always 
work properly on all devices, the second one should always work)

```shell
pip install roastedbyai
```
Windows:
```shell
python -m pip install roastedbyai
```
Linux:
```shell
python3 -m pip install roastedbyai
```


---


## Usage

```python
from roastedbyai import Conversation, Style

convo = Conversation(Style.valley_girl)

user_input = input("Start by roasting the AI:\n>>> ")
response1 = convo.send(user_input)
print(response1)

user_input = input("\nRoast the AI again:\n>>> ")
response2 = convo.send(user_input)
print(response2)

convo.kill()
# This step isn't necessary, the moment you don't use the `convo` object
# anymore, python will automatically handle it

print("\n---\nHistory:\n")
for msg in convo.history:
    print(msg["role"], msg["content"], sep=": ")
```


---


## Contributing
Feel free to open Pull Requests with new features, improvements or fixes.


---


## Disclaimer/Credits
I am not affiliated with https://roastedby.ai, all credits for the AI go to them.
