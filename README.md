# iMessage Assistant

A python script that responds to iMessages using OpenAI Assistants. Run the program followed by the phone number of the person you want to respond to, and let the assistant take it away. 

```
$ python3 -m src.main 6133054948 
```
 

## Prerequisites
- MacOS (required for iMessage DB access)
- Python 3.7.1 or greater

## SETUP
- git clone the repo and cd into project root
```
$ git clone git@github.com:Owen-Allen/imessage-assistant.git
$ cd imessage-assistant
```
$ - Create a virtual environment
```
$ python -m venv venv
```
$ - activate virtual environment
```
$ source venv/bin/activate
```
$ - Install requirements.txt
```
$ pip install -r requirements.txt
```
$ - Create a .env file with your Open AI API key, and the path to your chat.db file
    - To find the path to your chat.db file, you can run this command    
```
$ find /Users -name chat.db 2>/dev/null
```
 

- Install imessage ruby
```
$ brew install imessage-ruby
```
 

- Give terminal access to chat.db
    - Open System Preferences
    - Go to Security and Privacy
    - Click lock to make changes
    - Select Full Disk Access
    - Give Terminal.app full disk access
    - (Note: If running within an IDE like VSCode, you may also need to grant it Full Disk Access)

- To have the Assistant pretend to be you, create a file called "instructions" and add details about your self you want it to know

## TODO:
- [x] Process user input through cli
- [x] Fetch recent message data from chat.db
- [x] Generate response
- [x] Send response text message via iMessage
- [ ] Add check for api_key. Try using env var and env file
- [ ] Add conversation id so that get_messages_since does not fetch messages from the wrong conversation. (chat_handle_join)
- [ ] Check if imessage-ruby can send messages to group chats
- [ ] Create a User class by seperating responsibilies from the Conversation

Known Bug:
- Messages are selected by phone number, so get_messages_since() may fetch messages from different conversations if the same person has sent a message in another chat after the program started. Future fix, use the chat_handle_join table to pull the chat.guid when initiating a Conversation and add an extra WHERE clause to the SQL query.
