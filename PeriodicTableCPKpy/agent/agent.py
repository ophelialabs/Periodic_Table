"""
This is the main entry point for the agent.
It defines the workflow graph, state, tools, nodes and edges.
Integrated with quantum research and periodic table element analysis.
"""

from typing import Any, List, Dict
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
    Agent state for periodic table research
    
    Includes:
    - Messages: conversation history
    - Research data: element analysis and quantum simulations
    - Element history: user's selected elements
    """
    element_history: List[str] = []
    research_data: Dict[str, Any] = {}
    tools: List[Any]

@tool
def analyze_element(element_symbol: str):
    """
    Analyze properties of a periodic table element.
    Provides atomic number, electron configuration, ionization energy, etc.
    
    Args:
        element_symbol: Chemical symbol (e.g., 'H', 'He', 'C', 'Fe', 'Au')
    
    Returns:
        Dictionary with element properties and analysis
    """
    elements_db = {
        "H": {
            "name": "Hydrogen",
            "atomic_number": 1,
            "electron_config": "1s¹",
            "ionization_energy_ev": 13.6,
            "electronegativity": 2.2,
            "atomic_radius_pm": 53,
            "category": "nonmetal"
        },
        "He": {
            "name": "Helium",
            "atomic_number": 2,
            "electron_config": "1s²",
            "ionization_energy_ev": 24.6,
            "electronegativity": 0,
            "atomic_radius_pm": 31,
            "category": "noble gas"
        },
        "C": {
            "name": "Carbon",
            "atomic_number": 6,
            "electron_config": "[He]2s²2p²",
            "ionization_energy_ev": 11.26,
            "electronegativity": 2.55,
            "atomic_radius_pm": 77,
            "category": "nonmetal"
        },
        "O": {
            "name": "Oxygen",
            "atomic_number": 8,
            "electron_config": "[He]2s²2p⁴",
            "ionization_energy_ev": 13.62,
            "electronegativity": 3.44,
            "atomic_radius_pm": 66,
            "category": "nonmetal"
        },
        "Fe": {
            "name": "Iron",
            "atomic_number": 26,
            "electron_config": "[Ar]3d⁶4s²",
            "ionization_energy_ev": 7.87,
            "electronegativity": 1.83,
            "atomic_radius_pm": 140,
            "category": "transition metal"
        },
        "Au": {
            "name": "Gold",
            "atomic_number": 79,
            "electron_config": "[Xe]4f¹⁴5d¹⁰6s¹",
            "ionization_energy_ev": 9.23,
            "electronegativity": 2.54,
            "atomic_radius_pm": 144,
            "category": "transition metal"
        },
    }
    
    if element_symbol not in elements_db:
        return {"error": f"Element {element_symbol} not found in database"}
    
    return elements_db[element_symbol]

@tool
def simulate_quantum_orbital(element_symbol: str, grid_size: int = 16):
    """
    Run quantum simulation to generate 3D electron orbital visualization.
    Simulates the probability distribution of electrons in an atom.
    
    Args:
        element_symbol: Chemical symbol (e.g., 'H', 'C', 'Fe')
        grid_size: Resolution of probability grid (default: 16)
    
    Returns:
        Simulation results with orbital data and visualization parameters
    """
    element_data = analyze_element(element_symbol)
    
    if "error" in element_data:
        return element_data
    
    atomic_number = element_data["atomic_number"]
    
    # Mock quantum simulation result
    ground_state_energy = -13.6 * (atomic_number ** 2) / (1 ** 2)  # Rydberg formula
    bohr_radius = 0.529 / atomic_number  # Angstroms
    
    return {
        "element": element_symbol,
        "atomic_number": atomic_number,
        "grid_size": grid_size,
        "ground_state_energy_ev": round(ground_state_energy, 2),
        "bohr_radius_angstroms": round(bohr_radius, 3),
        "orbital_type": "1s (ground state)",
        "probability_distribution": "Gaussian-like spherical distribution",
        "simulation_status": "completed",
        "data_points": grid_size ** 3,
    }

@tool
def research_element_properties(element_symbol: str):
    """
    Comprehensive research on element properties for R&D and materials science.
    Analyzes atomic structure, reactivity, and potential applications.
    
    Args:
        element_symbol: Chemical symbol
    
    Returns:
        Detailed research analysis
    """
    element_data = analyze_element(element_symbol)
    
    if "error" in element_data:
        return element_data
    
    orbital_data = simulate_quantum_orbital(element_symbol)
    
    return {
        "element": element_symbol,
        "name": element_data["name"],
        "atomic_properties": element_data,
        "quantum_simulation": orbital_data,
        "research_notes": f"""
Research Analysis for {element_data['name']}:

1. Electronic Structure:
   - Configuration: {element_data['electron_config']}
   - Ionization Energy: {element_data['ionization_energy_ev']} eV
   - Electronegativity: {element_data['electronegativity']}

2. Quantum Properties:
   - Ground State Energy: {orbital_data['ground_state_energy_ev']} eV
   - Effective Bohr Radius: {orbital_data['bohr_radius_angstroms']} Å
   - Atomic Radius: {element_data['atomic_radius_pm']} pm

3. Reactivity:
   - Category: {element_data['category']}
   - Likely to form bonds with complementary electronegativity elements
   - Suitable for molecular and materials science applications

4. Applications:
   - Use in quantum computing research
   - Potential for nanotechnology applications
   - Reference element for periodic table studies
        """
    }

@tool
def get_weather(location: str):
    """
    Get the weather for a given location.
    """
    return f"The weather for {location} is 70 degrees."

backend_tools = [
    analyze_element,
    simulate_quantum_orbital,
    research_element_properties,
    get_weather
]

# Extract tool names from backend_tools for comparison
backend_tool_names = [tool.name for tool in backend_tools]


async def chat_node(state: AgentState, config: RunnableConfig) -> Command[Literal["tool_node", "__end__"]]:
    """
    Standard chat node based on the ReAct design pattern. It handles:
    - The model to use (and binds in CopilotKit actions and the tools defined above)
    - The system prompt
    - Getting a response from the model
    - Handling tool calls

    For more about the ReAct design pattern, see:
    https://www.perplexity.ai/search/react-agents-NcXLQhreS0WDzpVaS4m9Cg
    """

    # 1. Define the model
    model = ChatOpenAI(model="gpt-4o")

    # 2. Bind the tools to the model
    model_with_tools = model.bind_tools(
        [
            *state.get("tools", []), # bind tools defined by ag-ui
            *backend_tools,
        ],

        # 2.1 Disable parallel tool calls to avoid race conditions,
        #     enable this for faster performance if you want to manage
        #     the complexity of running tool calls in parallel.
        parallel_tool_calls=False,
    )

    # 3. Define the system message by which the chat model will be run
    system_prompt = """You are an expert research assistant specializing in chemistry and quantum physics.
    
Your capabilities include:
- Analyzing periodic table elements and their properties
- Running quantum simulations for electron orbital visualization
- Providing detailed research on element applications in materials science
- Explaining quantum mechanics concepts and their practical applications

When users ask about elements:
1. Analyze the element's properties
2. Run quantum orbital simulations if interested in visual data
3. Provide comprehensive research insights
4. Suggest related elements or applications

Be detailed, scientific, and engaging in your responses."""

    system_message = SystemMessage(content=system_prompt)

    # 4. Run the model to generate a response
    response = await model_with_tools.ainvoke([
        system_message,
        *state["messages"],
    ], config)

    # only route to tool node if tool is not in the tools list
    if route_to_tool_node(response):
        print("routing to tool node")
        return Command(
            goto="tool_node",
            update={
                "messages": [response],
            }
        )

    # 5. We've handled all tool calls, so we can end the graph.
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
