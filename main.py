from typing import Sequence, List

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.constants import END
from langgraph.graph import MessageGraph

from chains import generation_chain, reflect_chain

load_dotenv()

## Définissons des clés
REFLECT="reflect"
GENERATE="generate"


## Fonction associé à chaque nodes
def generation_node(state:Sequence[BaseMessage]):
    return generation_chain.invoke({"messages":state})

def reflection_node(messages:Sequence[BaseMessage]) -> List[BaseMessage]:
    res =reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]

### Retournos au graphe
builder= MessageGraph()
builder.add_node(GENERATE,generation_node)
builder.add_node(REFLECT,reflection_node)
builder.set_entry_point(GENERATE)

def should_continue(state:List[BaseMessage]):
    if len(state) > 6:
        return END
    return REFLECT

builder.add_conditional_edges(GENERATE,should_continue)

builder.add_edge(REFLECT,GENERATE)

graph=builder.compile()

#graph.get_graph().print_ascii()

### Tester now
input=HumanMessage(content="""
Make this tweet better: "
I'm happy to share that I’ve obtained a new certification: "Data processing with R" from Google! Previously, I was doing everything with Pandas in Python, but learning R has given me a new perspective. It offers a more advanced approach to statistical analysis, and I’ve discovered the power of RMarkdown for reporting and documentation. This new way of working helps me implement statistics more effectively, providing a deeper understanding and new methods that complement my previous experience with Python.

"
""")
response=graph.invoke(input)

print(response)