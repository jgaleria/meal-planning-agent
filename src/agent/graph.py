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

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

llm_with_tools = llm.bind_tools(ALL_TOOLS, tool_choice="auto")

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

async def call_model(state: State):
# async def call_model(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Process input and returns output.

    Can use runtime configuration to alter behavior.
    """
    # configuration = config.get("configurable", {})
    # model_name = configuration.get("model_name", "gpt-4o-mini")

    print("🔍 Available tools:")
    for tool in ALL_TOOLS:
        print(f"  - Name: {tool.name}")
        print(f"  - Description: {tool.description}")
        print(f"  - Schema: {tool.args}")

    # llm_with_tools = llm.bind_tools(
    #     ALL_TOOLS,
    #     tool_choice="auto"
    # )

    # 🔍 DEBUG: Check what the bound LLM looks like
    print(f"🔍 LLM bound tools: {llm_with_tools.kwargs.get('tools', 'None')}")

    ### Add system prompt if not there
    # messages = state["messages"]
    # has_system_prompt = any(isinstance(msg, SystemMessage) for msg in messages)

    # if not has_system_prompt:
    #     messages= [SystemMessage(content=MEAL_PLANNER_SYSTEM_PROMPT)] + messages

    # 🔍 DEBUG: Print exact messages being sent
    # print("🔍 Messages being sent to LLM:")
    # for i, msg in enumerate(messages):
    #     print(f"  {i}: {type(msg).__name__}: {str(msg.content)[:100]}...")

    response = await llm_with_tools.ainvoke(state["messages"])

    # response = await llm.ainvoke(messages)

    # Enhanced debugging
    # print(f"🔍 Model used: {model_name}")
    print(f"🔍 Response content: {response.content[:100]}...")
    print(f"🔍 Response type: {type(response).__name__}")
    print(f"🔍 Has tool_calls: {hasattr(response, 'tool_calls')}")
    
    if hasattr(response, 'tool_calls'):
        tool_calls = response.tool_calls
        print(f"🔍 Tool calls type: {type(tool_calls)}")
        print(f"🔍 Tool calls: {tool_calls}")
        print(f"🔍 Number of tool calls: {len(tool_calls) if tool_calls else 0}")
        
        if tool_calls:
            for i, call in enumerate(tool_calls):
                print(f"   Tool {i+1}: {call}")

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
    tools_condition, # No explicit END needed
)

graph_builder.add_edge("tools", "call_model")

graph = graph_builder.compile(name="Meal Planner Agent")
