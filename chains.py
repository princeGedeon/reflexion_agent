from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

reflection_prompt=ChatPromptTemplate.from_messages(
    (
        "system",
        "You are a virtual Twitter influencer agent. Generate critique and recommendations for a user's tweet",
        "Always provide detailed recommendations with requests for length, virality, style, etc."
    ),
    MessagesPlaceholder(variable_name="messages")
)


generation_prompt=ChatPromptTemplate.from_messages(
    (
        "system",
        "You are a twitter influencer assistant tasked with writing excellent twitter posts",
        "Generate the best twitter post possible for the user's request"
    ),
    MessagesPlaceholder(variable_name="messages")
)
