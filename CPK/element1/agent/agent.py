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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import base64
from io import BytesIO

# Sample periodic table data
PERIODIC_TABLE_DATA = {
    "H": {"name": "Hydrogen", "atomic_number": 1, "atomic_mass": 1.008, "electronegativity": 2.1, "ionization_energy": 13.6, "atomic_radius": 37, "density": 0.08988, "melting_point": -259.16, "boiling_point": -252.87, "period": 1, "group": 1},
    "He": {"name": "Helium", "atomic_number": 2, "atomic_mass": 4.003, "electronegativity": 0, "ionization_energy": 24.6, "atomic_radius": 32, "density": 0.1785, "melting_point": -272.2, "boiling_point": -268.93, "period": 1, "group": 18},
    "Li": {"name": "Lithium", "atomic_number": 3, "atomic_mass": 6.941, "electronegativity": 0.98, "ionization_energy": 5.39, "atomic_radius": 152, "density": 0.534, "melting_point": 180.54, "boiling_point": 1342, "period": 2, "group": 1},
    "Be": {"name": "Beryllium", "atomic_number": 4, "atomic_mass": 9.012, "electronegativity": 1.57, "ionization_energy": 9.32, "atomic_radius": 112, "density": 1.85, "melting_point": 1287, "boiling_point": 2471, "period": 2, "group": 2},
    "C": {"name": "Carbon", "atomic_number": 6, "atomic_mass": 12.011, "electronegativity": 2.55, "ionization_energy": 11.26, "atomic_radius": 77, "density": 2.26, "melting_point": 3823, "boiling_point": 4098, "period": 2, "group": 14},
    "N": {"name": "Nitrogen", "atomic_number": 7, "atomic_mass": 14.007, "electronegativity": 3.04, "ionization_energy": 14.53, "atomic_radius": 71, "density": 1.251, "melting_point": -210.1, "boiling_point": -195.8, "period": 2, "group": 15},
    "O": {"name": "Oxygen", "atomic_number": 8, "atomic_mass": 15.999, "electronegativity": 3.44, "ionization_energy": 13.61, "atomic_radius": 66, "density": 1.429, "melting_point": -218.79, "boiling_point": -182.95, "period": 2, "group": 16},
    "F": {"name": "Fluorine", "atomic_number": 9, "atomic_mass": 18.998, "electronegativity": 3.98, "ionization_energy": 17.42, "atomic_radius": 64, "density": 1.696, "melting_point": -219.62, "boiling_point": -188.12, "period": 2, "group": 17},
    "Fe": {"name": "Iron", "atomic_number": 26, "atomic_mass": 55.845, "electronegativity": 1.83, "ionization_energy": 7.90, "atomic_radius": 124, "density": 7.874, "melting_point": 1538, "boiling_point": 2862, "period": 4, "group": 8},
    "Cu": {"name": "Copper", "atomic_number": 29, "atomic_mass": 63.546, "electronegativity": 1.90, "ionization_energy": 7.73, "atomic_radius": 132, "density": 8.96, "melting_point": 1084.62, "boiling_point": 2562, "period": 4, "group": 11},
    "Au": {"name": "Gold", "atomic_number": 79, "atomic_mass": 196.967, "electronegativity": 2.54, "ionization_energy": 9.23, "atomic_radius": 144, "density": 19.3, "melting_point": 1064.18, "boiling_point": 2856, "period": 6, "group": 11},
}

class AgentState(MessagesState):
    """
    Here we define the state of the agent
    """
    tools: List[Any]

@tool
def analyze_periodic_properties(property_name: str, elements: str = "all"):
    """
    Analyze and return statistical analysis of periodic table properties.
    Use this to get data for visualization and analysis.
    
    Args:
        property_name: The property to analyze (e.g., 'atomic_mass', 'electronegativity', 'density')
        elements: Comma-separated element symbols or 'all'
    
    Returns:
        JSON with property statistics and data points
    """
    try:
        if elements == "all":
            data_dict = PERIODIC_TABLE_DATA
        else:
            elem_list = [e.strip().capitalize() for e in elements.split(",")]
            data_dict = {k: v for k, v in PERIODIC_TABLE_DATA.items() if k in elem_list}
        
        values = [v.get(property_name, 0) for v in data_dict.values() if property_name in v]
        
        if not values:
            return json.dumps({"error": f"Property '{property_name}' not found or no data available"})
        
        stats_result = {
            "property": property_name,
            "count": len(values),
            "mean": float(np.mean(values)),
            "median": float(np.median(values)),
            "std_dev": float(np.std(values)),
            "min": float(np.min(values)),
            "max": float(np.max(values)),
            "data": {k: v.get(property_name, None) for k, v in data_dict.items()},
        }
        return json.dumps(stats_result)
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def generate_trend_analysis(property1: str, property2: str):
    """
    Generate correlation analysis between two periodic properties using scipy and numpy.
    
    Args:
        property1: First property to compare
        property2: Second property to compare
    
    Returns:
        JSON with correlation coefficient and analysis
    """
    try:
        data1 = []
        data2 = []
        
        for symbol, elem_data in PERIODIC_TABLE_DATA.items():
            if property1 in elem_data and property2 in elem_data:
                val1 = elem_data[property1]
                val2 = elem_data[property2]
                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    data1.append(val1)
                    data2.append(val2)
        
        if len(data1) < 2:
            return json.dumps({"error": "Not enough data for correlation analysis"})
        
        correlation, p_value = stats.pearsonr(data1, data2)
        
        analysis = {
            "property1": property1,
            "property2": property2,
            "pearson_correlation": float(correlation),
            "p_value": float(p_value),
            "significant": p_value < 0.05,
            "data_points": len(data1),
        }
        return json.dumps(analysis)
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def create_visualization_data(visualization_type: str, property_name: str):
    """
    Prepare data for visualizations using pandas and numpy.
    Returns base64 encoded image data.
    
    Args:
        visualization_type: 'bar', 'scatter', 'heatmap', 'boxplot'
        property_name: The property to visualize
    
    Returns:
        Base64 encoded image and metadata
    """
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
        
        if visualization_type == "bar":
            symbols = list(PERIODIC_TABLE_DATA.keys())[:10]
            values = [PERIODIC_TABLE_DATA[s].get(property_name, 0) for s in symbols]
            
            fig, ax = plt.subplots(figsize=(12, 6))
            bars = ax.bar(symbols, values, color='steelblue', edgecolor='navy', alpha=0.7)
            ax.set_ylabel(property_name.replace('_', ' ').title(), fontsize=12)
            ax.set_title(f'{property_name.replace("_", " ").title()} Comparison', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            
        elif visualization_type == "scatter":
            df_list = []
            for symbol, data in PERIODIC_TABLE_DATA.items():
                if 'atomic_number' in data and property_name in data:
                    df_list.append({'atomic_number': data['atomic_number'], property_name: data[property_name], 'symbol': symbol})
            
            df = pd.DataFrame(df_list)
            fig, ax = plt.subplots(figsize=(12, 6))
            scatter = ax.scatter(df['atomic_number'], df[property_name], s=100, alpha=0.6, c=df['atomic_number'], cmap='viridis')
            
            for idx, row in df.iterrows():
                ax.annotate(row['symbol'], (row['atomic_number'], row[property_name]), fontsize=9)
            
            ax.set_xlabel('Atomic Number', fontsize=12)
            ax.set_ylabel(property_name.replace('_', ' ').title(), fontsize=12)
            ax.set_title(f'{property_name.replace("_", " ").title()} vs Atomic Number', fontsize=14, fontweight='bold')
            plt.colorbar(scatter, ax=ax)
            
        elif visualization_type == "boxplot":
            periods = {}
            for symbol, data in PERIODIC_TABLE_DATA.items():
                period = data.get('period', 1)
                if period not in periods:
                    periods[period] = []
                if property_name in data:
                    periods[period].append(data[property_name])
            
            fig, ax = plt.subplots(figsize=(12, 6))
            bp = ax.boxplot(periods.values(), labels=[f'Period {p}' for p in sorted(periods.keys())], patch_artist=True)
            
            for patch in bp['boxes']:
                patch.set_facecolor('lightblue')
            
            ax.set_ylabel(property_name.replace('_', ' ').title(), fontsize=12)
            ax.set_title(f'{property_name.replace("_", " ").title()} Distribution by Period', fontsize=14, fontweight='bold')
            
        else:
            return json.dumps({"error": f"Visualization type '{visualization_type}' not supported"})
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return json.dumps({
            "success": True,
            "visualization_type": visualization_type,
            "property": property_name,
            "image_base64": image_base64,
            "message": f"Generated {visualization_type} visualization for {property_name}"
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

backend_tools = [
    analyze_periodic_properties,
    generate_trend_analysis,
    create_visualization_data,
]

# Extract tool names from backend_tools for comparison
backend_tool_names = [tool.name for tool in backend_tools]


async def chat_node(state: AgentState, config: RunnableConfig) -> Command[Literal["tool_node", "__end__"]]:
    """
    Standard chat node based on the ReAct design pattern for chemistry analysis.
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
        content="""You are an expert chemistry AI assistant specializing in the Periodic Table of Elements.
        
Your capabilities include:
1. **Element Information**: Provide detailed properties of any element from the periodic table
2. **Data Analysis**: Analyze trends in elemental properties using statistical tools
3. **Visualizations**: Generate charts and graphs using matplotlib and seaborn
4. **Correlations**: Find relationships between different elemental properties
5. **Frontend Integration**: Trigger UI updates through frontend actions (selectElement, filterByCategory, highlightProperty, searchElement, changeVisualization)

When analyzing data:
- Use analyze_periodic_properties for statistics on element properties
- Use generate_trend_analysis to find correlations between properties using scipy
- Use create_visualization_data to generate charts (bar, scatter, boxplot)

Always provide clear explanations of findings and suggest related visualizations or analyses the user might be interested in.
When appropriate, suggest using frontend actions to update the UI display."""
    )

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
