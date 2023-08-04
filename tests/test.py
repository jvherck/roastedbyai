from roastedbyai import Conversation

convo = Conversation()

user_input = input("Start by roasting the AI:\n>>> ")
response1 = convo.send(user_input)
print(response1)

user_input = input("\nRoast the AI again:\n>>> ")
response2 = convo.send(user_input)
print(response2)

convo.kill()
# This step isn't necessary, the moment you don't use the `convo` object
# anymore, python will automatically handle it

print("\n---\n")
for msg in convo.history:
    print(msg["role"], msg["content"], sep=": ")