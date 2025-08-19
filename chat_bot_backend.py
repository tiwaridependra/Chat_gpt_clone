from langchain_openai import ChatOpenAI
from typing import TypedDict,Literal,Annotated,List
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver


model = ChatOpenAI(model='gpt-3.5-turbo',openai_api_key=API_KEY)
# result=model.invoke("what is the capital of india")
# print(result.content)

class Chats(TypedDict):
    messages:Annotated[List[BaseMessage],add_messages]

def chat_messages(state:Chats):
    input_data=state["messages"]
    response=model.invoke(input_data)
    return {"messages":[response]}
graph=StateGraph(Chats)
graph.add_node('chat_message',chat_messages)

graph.add_edge(START,'chat_message')
graph.add_edge('chat_message',END)
checkpoint=InMemorySaver()
chatbot=graph.compile(checkpointer=checkpoint)


