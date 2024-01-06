# iMessage-GPT

A python script that responds to iMessages using OpenAI Assistants

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
- Since the messages are selected by phone number, get_messages_since() will sometimes get messages from the correct person but in a different conversation (group chat). To fix, when initiating a Conversation, we should figure out the chat.guid from the chat_handle_join table
