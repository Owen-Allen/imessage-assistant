# iMessage-GPT

A python script that responds to iMessages using OpenAI Assistants. Run the program followed by the phone number of the person you want to respond to, and let the assistant take it away. 

```
$ src.main 6133054948
```

## REQUIREMENTS
- MacOS for iMessage DB
- OpenAI Key
- imessage-ruby

## SETUP
- git clone the repo and cd into project root
```
git clone git@github.com:Owen-Allen/imessage-assistant.git
cd imessage-assistant
```
- Create a virtual environment
```
python -m venv venv
```
- activate virtual environment
```
source venv/bin/activate
```
- Install requirements.txt
```
pip install -r requirements.txt
```
- Create a .env file with your Open AI API key, and the path to your chat.db file
    - To find the path to your chat.db file, you can run this command    
```
find /Users -name chat.db 2>/dev/null
```

- Install imessage ruby
```
brew install imessage-ruby
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

Bug:
- Since the messages are selected by phone number, get_messages_since() will sometimes get messages from the correct person but in a different conversation, if they sent a message to you after the program began. To fix, when initiating a Conversation, pull the chat.guid from the chat_handle_join table and add an extra WHERE clause to the sql query
