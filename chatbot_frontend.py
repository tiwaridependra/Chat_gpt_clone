import streamlit as st
from langchain_core.messages import HumanMessage,SystemMessage,BaseMessage,AIMessage
from chat_bot_backend import chatbot
import uuid
from chat_bot_backend import model
#******************

def generate_thread():
  thread_id=uuid.uuid4()
  return thread_id

#********************
if 'thread_list' not in st.session_state:
  st.session_state['thread_list']=[]
if 'message_history' not in st.session_state:
  st.session_state['message_history']=[]
if 'thread_id' not in st.session_state:
  st.session_state['thread_id']=generate_thread()
  st.session_state['thread_list'].append(st.session_state['thread_id'])
  st.session_state['message_history']=[]
  st.session_state['thread_map']={st.session_state['thread_id']:'New chat'}
config = {"configurable": {"thread_id": st.session_state['thread_id']}}



st.title("CHATGPT CLONE maugaGPT")

st.sidebar.title('Chatbot')

if st.sidebar.button('Add New Chat'):
  st.session_state['thread_id']=generate_thread()
  st.session_state['thread_list'].append(st.session_state['thread_id'])
  st.session_state['thread_map'][st.session_state['thread_id']]='New chat'
  st.session_state['message_history']=[]
  config = {"configurable": {"thread_id": st.session_state['thread_id']}}

st.sidebar.title('All Recent Chats')
  
for thread in st.session_state['thread_list']:
  if st.sidebar.button(str(st.session_state['thread_map'][thread])):
      st.session_state['thread_id']=thread
      config = {"configurable": {"thread_id": st.session_state['thread_id']}}
      state = chatbot.get_state(config={'configurable': {'thread_id': thread}})
      messages = state.values.get("messages", [])
      temp_messages=[]
      for msg in messages:
        if isinstance(msg,HumanMessage):
          temp_messages.append({'role':'user','content':msg.content})
        else:
          temp_messages.append({'role':'AI','content':msg.content})
      st.session_state['message_history']=temp_messages
          


for message in st.session_state['message_history']:
  with st.chat_message(message['role']):
    st.text(message['content'])
input_data=st.chat_input('Type here')

if input_data:
    st.session_state['message_history'].append({'role':'user','content':input_data})
     
    with st.chat_message('user'):
     st.text(input_data)
    with st.chat_message('AI'):
     result = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=input_data)]},
                config= {'configurable': {'thread_id': st.session_state['thread_id']}},
                stream_mode= 'messages'
            )
        )
     
     st.session_state['message_history'].append({'role': 'assistant', 'content': result})
    #  message1=st.session_state['message_history']
    #  summary=""
    #  for msg in message1:
    #    summary+=(msg['content'])
    #  prompt=f"Based on the summary of the conversation generate a title for the conversation in 2 to 3 words {summary}.Do not Assume any thing if the history is inconclusive simply keept it as New Chat"
    #  response=model.invoke(prompt)
     st.session_state['thread_map'][st.session_state['thread_id']]=input_data[0:25]
     
    #  st.text(result)
       
