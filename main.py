from typing import Sequence, List

from dotenv import load_dotenv

from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser,PydanticToolsParser
from langchain_core.messages import HumanMessage, BaseMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from  langchain_openai import ChatOpenAI
from langgraph.graph import END, MessageGraph

from chains import first_responder, revisor
from tool_executer import execute_tools

load_dotenv()

MAX_ITERATIONS = 2

builder=MessageGraph()
builder.add_node("draft",first_responder)
builder.add_node("execute_tools",execute_tools)

builder.add_node("revise",revisor)

builder.add_edge("draft","execute_tools")
builder.add_edge("execute_tools","revise")


def event_loop(state:List[BaseMessage])->str:
    count_tool_vists=sum(isinstance(item,ToolMessage) for item in state)
    num_iterations=count_tool_vists
    if num_iterations>MAX_ITERATIONS:
        return END
    return "execute_tools"

builder.add_conditional_edges("revise",event_loop)

builder.set_entry_point("draft")
graph=builder.compile()
#print(graph.get_graph().draw_ascii())
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
if __name__ == "__main__":
    res=graph.invoke(
        "Parle moi histoire derrière la vision par ordinateur, ainsi que des faits marquants, cite des entreprises en France qui s'investit dans cette branche de l'IA, leur réalisation dans ce domaine"

    )


    print(res)