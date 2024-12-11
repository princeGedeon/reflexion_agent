from typing import List

from pydantic import BaseModel, Field


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