"""LangGraph meal planning agent with tool integration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Annotated
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from agent.tools import ALL_TOOLS
from agent.prompts import MEAL_PLANNER_SYSTEM_PROMPT

class Configuration(TypedDict):
    """Configurable parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    See: https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/
    """

    model_name: str


@dataclass
class State(TypedDict):
    """Input state for the agent.

    Defines the initial structure of incoming data.
    See: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
    """

    messages: Annotated[list, add_messages]


async def call_model(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Process input and returns output.

    Can use runtime configuration to alter behavior.
    """
    configuration = config.get("configurable", {})
    model_name = configuration.get("model_name", "gpt-3.5-turbo")

    llm = ChatOpenAI(model=model_name, temperature=0.7)
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    ### Add system prompt if not there
    messages = state["messages"]
    has_system_prompt = any(isinstance(msg, SystemMessage) for msg in messages)

    if not has_system_prompt:
        messages= [SystemMessage(content=MEAL_PLANNER_SYSTEM_PROMPT)] + messages

    response = await llm.ainvoke(messages)

    return {
        "messages": [response]
    }



# Define the graph
graph = (
    StateGraph(State, config_schema=Configuration)
    .add_node(call_model)
    .add_edge("__start__", "call_model")
    .compile(name="New Graph")
)
