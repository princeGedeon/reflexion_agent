import datetime

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputToolsParser, PydanticToolsParser
from langchain_core.output_parsers.openai_functions import PydanticOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from schema import AnswerQuestion

load_dotenv()

actor_prompt_template=ChatPromptTemplate.from_messages(
    [
    (
        "system",
        """Tu es un chercheur export
        Heure actuelle : {time}
        
        1. {first_instruction}
        2. Réfléchis et critique ta réponse.Sois sévère pour améliorer la qualité
        3. Recommande des requêtes de recherches pour améliorer l'information et ta réponse.
        """
    ),
    MessagesPlaceholder(variable_name="messages")
        ]
).partial(
    time=lambda: datetime.datetime.now()
)

llm=ChatOpenAI()
parser=JsonOutputToolsParser(return_id=True)
parser_pydantic=PydanticToolsParser(tools=[AnswerQuestion])
actor_chain= actor_prompt_template | llm

first_reponder_prompt_template=actor_prompt_template.partial(
    first_instruction="Fournir une réponse détaillé de ~300 mots"
)

first_responder=first_reponder_prompt_template | llm.bind_tools(
    tools=[AnswerQuestion],tool_choice="AnswerQuestion"
)

if __name__=="__main__":
    human_message=HumanMessage(
        content="Ecris à propos de l'écologie et du Génie de l'environnement"
        "Liste les entreprises en France quui sont dans ce domaine "
    )

    chain= (
        first_reponder_prompt_template |
        llm.bind_tools(tools=[AnswerQuestion],tool_choice="AnswerQuestion") |
        parser_pydantic
    )

    res=chain.invoke(input={"messages": [human_message]})
    print(res)
