"""LangGraph meal planning agent with tool integration."""

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
    """Configurable parameters for the agent."""
    model_name: str
    temperature: float
    max_tokens: int

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

    # 🔧 Get configuration
    configuration = config.get("configurable", {})
    model_name = configuration.get("model_name", "gpt-4o-mini")
    temperature = configuration.get("temperature", 0.7)
    max_tokens = configuration.get("max_tokens", 1000)

    print(f"🔧 Using model: {model_name}")
    print(f"🔧 Temperature: {temperature}")
    print(f"🔧 Max tokens: {max_tokens}")

    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens
    )

    llm_with_tools = llm.bind_tools(
        ALL_TOOLS, 
        tool_choice="auto"
    )

    ### Add system prompt if not there
    messages = state["messages"]
    has_system_prompt = any(isinstance(msg, SystemMessage) for msg in messages)

    if not has_system_prompt:
        messages = [SystemMessage(content=MEAL_PLANNER_SYSTEM_PROMPT)] + messages

    response = await llm_with_tools.ainvoke(state["messages"])

    return {
        "messages": [response]
    }

tool_node = ToolNode(ALL_TOOLS)

graph_builder = StateGraph(State, config_schema=Configuration)

graph_builder.add_node("call_model", call_model)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "call_model")

graph_builder.add_conditional_edges(
    "call_model",
    tools_condition, 
)

graph_builder.add_edge("tools", "call_model")

graph = graph_builder.compile(name="Meal Planner Agent")
