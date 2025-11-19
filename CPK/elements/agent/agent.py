"""
This is the main entry point for the agent.
It defines the workflow graph, state, tools, nodes and edges.
"""

from typing import Any, List
from typing_extensions import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.types import Command
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
import json

class AgentState(MessagesState):
    """
    State for the Periodic Table Agent with visualization capabilities.
    """
    proverbs: List[str] = []
    selected_elements: List[str] = []
    visualization_type: str = "scatter"
    visualization_property: str = "atomicMass"
    tools: List[Any]

@tool
def get_weather(location: str):
    """
    Get the weather for a given location.
    """
    return f"The weather for {location} is 70 degrees."

@tool
def select_elements_by_category(category: str) -> str:
    """
    Select elements by their category (e.g., 'Transition Metal', 'Nonmetal', 'Halogen').
    Returns a list of element symbols in that category.
    """
    categories_map = {
        "nonmetal": ["H", "C", "N", "O", "P", "S", "Se"],
        "reactive nonmetal": ["F", "Cl", "Br"],
        "noble gas": ["He", "Ne", "Ar", "Kr"],
        "alkali metal": ["Li", "Na", "K"],
        "alkaline earth metal": ["Be", "Mg", "Ca"],
        "metalloid": ["B", "Si", "Ge", "As"],
        "transition metal": ["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn"],
        "post-transition metal": ["Al", "Ga"],
        "halogen": ["F", "Cl", "Br"],
        "lanthanide": [],
        "actinide": [],
    }
    
    cat_lower = category.lower()
    elements = categories_map.get(cat_lower, [])
    return json.dumps({
        "category": category,
        "elements": elements,
        "count": len(elements)
    })

@tool
def create_visualization(
    visualization_type: str,
    property_name: str,
    elements: List[str] = None
) -> str:
    """
    Create a data visualization. 
    visualization_type: 'scatter', 'histogram', or 'heatmap'
    property_name: 'atomicMass', 'electronegativity', 'ionizationEnergy', or 'density'
    elements: optional list of element symbols to visualize
    """
    return json.dumps({
        "visualization_type": visualization_type,
        "property": property_name,
        "elements": elements or "all",
        "status": "created"
    })

@tool
def get_element_properties(element_symbol: str) -> str:
    """
    Get detailed properties of an element by its symbol.
    """
    properties = {
        "H": {"name": "Hydrogen", "atomicNumber": 1, "atomicMass": 1.008, "category": "Nonmetal"},
        "He": {"name": "Helium", "atomicNumber": 2, "atomicMass": 4.003, "category": "Noble Gas"},
        "C": {"name": "Carbon", "atomicNumber": 6, "atomicMass": 12.011, "category": "Nonmetal"},
        "N": {"name": "Nitrogen", "atomicNumber": 7, "atomicMass": 14.007, "category": "Nonmetal"},
        "O": {"name": "Oxygen", "atomicNumber": 8, "atomicMass": 15.999, "category": "Nonmetal"},
        "Fe": {"name": "Iron", "atomicNumber": 26, "atomicMass": 55.845, "category": "Transition Metal"},
        "Cu": {"name": "Copper", "atomicNumber": 29, "atomicMass": 63.546, "category": "Transition Metal"},
        "Au": {"name": "Gold", "atomicNumber": 79, "atomicMass": 196.967, "category": "Transition Metal"},
    }
    
    element = properties.get(element_symbol, {})
    if element:
        return json.dumps(element)
    return json.dumps({"error": f"Element {element_symbol} not found"})

backend_tools = [
    get_weather,
    select_elements_by_category,
    create_visualization,
    get_element_properties,
]

# Extract tool names from backend_tools for comparison
backend_tool_names = [tool.name for tool in backend_tools]


async def chat_node(state: AgentState, config: RunnableConfig) -> Command[Literal["tool_node", "__end__"]]:
    """
    Chat node with ReAct pattern for the Periodic Table agent.
    """

    # 1. Define the model
    model = ChatOpenAI(model="gpt-4o")

    # 2. Bind the tools to the model
    model_with_tools = model.bind_tools(
        [
            *state.get("tools", []),
            *backend_tools,
        ],
        parallel_tool_calls=False,
    )

    # 3. Define the system message
    system_message = SystemMessage(
        content=f"""You are an expert chemistry assistant with deep knowledge of the periodic table.
You have access to tools to visualize element data and explore element properties.
Help users understand the periodic table, compare elements, and create data visualizations.
The current selected elements are: {state.get('selected_elements', [])}
Current visualization type: {state.get('visualization_type', 'scatter')}
Current visualization property: {state.get('visualization_property', 'atomicMass')}"""
    )

    # 4. Run the model
    response = await model_with_tools.ainvoke([
        system_message,
        *state["messages"],
    ], config)

    # Route to tool node if necessary
    if route_to_tool_node(response):
        print("routing to tool node")
        return Command(
            goto="tool_node",
            update={
                "messages": [response],
            }
        )

    # End the graph
    return Command(
        goto=END,
        update={
            "messages": [response],
        }
    )

def route_to_tool_node(response: BaseMessage):
    """
    Route to tool node if any tool call in the response matches a backend tool name.
    """
    tool_calls = getattr(response, "tool_calls", None)
    if not tool_calls:
        return False

    for tool_call in tool_calls:
        if tool_call.get("name") in backend_tool_names:
            return True
    return False

# Define the workflow graph
workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.add_node("tool_node", ToolNode(tools=backend_tools))
workflow.add_edge("tool_node", "chat_node")
workflow.set_entry_point("chat_node")

graph = workflow.compile()
