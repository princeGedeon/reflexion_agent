from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

reflection_prompt=ChatPromptTemplate.from_messages(
    [
    (
        "system",
        "You are a virtual Twitter influencer agent. Generate critique and recommendations for a user's tweet"+
        "Always provide detailed recommendations with requests for length, virality, style, etc."
    ),
    MessagesPlaceholder(variable_name="messages")
        ]
)


generation_prompt=ChatPromptTemplate.from_messages(
    [
    (
        "system",
        "You are a twitter influencer assistant tasked with writing excellent twitter posts"+
        "Generate the best twitter post possible for the user's request"+
        "if the user provides critique, respond with a revised version of your previous attemps "
    ),
    MessagesPlaceholder(variable_name="messages")
 ]
)

llm=ChatOpenAI()
generation_chain= generation_prompt | llm
reflect_chain=reflection_prompt | llm