from typing import List

from langchain_core.pydantic_v1 import BaseModel,Field


class Reflection(BaseModel):
    missing:str=Field(description="Critique de ce qui a été oublié")
    superflous:str=Field(description="Critique de ce qui est superflux")

class AnswerQuestion(BaseModel):
    """Réponse aux questions"""
    asnwer:str=Field(description="~300 mots détaillé de la réponse à la question")
    reflection: Reflection=Field(description="Ta reflexion par rapport à la reponse initial")
    search_queries:List[str]=Field(
description="1-4 requête de recherche pour améliorer face au critique de ta réponse actuelle"
    )

class ReviseAnswer(AnswerQuestion):
    """Revise ta réponse """
    references:List[str]=Field(
        description="Citation qui ont motivé le changement de la réponse"
    )