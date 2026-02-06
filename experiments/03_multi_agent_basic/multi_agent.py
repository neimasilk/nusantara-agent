import os
import json
from typing import Annotated, TypedDict, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Define the state of the conversation
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    national_context: str
    adat_context: str
    final_synthesis: str

# Initialize LLM
llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat"
)

# 1. Agen Nasional
def national_agent(state: AgentState):
    query = state['messages'][0].content
    prompt = f"Kamu adalah pakar hukum perdata nasional Indonesia. Analisis pertanyaan ini berdasarkan KUHPerdata: '{query}'. Fokus pada hak anak kandung dan aturan harta pencaharian (gono-gini)."
    response = llm.invoke([SystemMessage(content=prompt)])
    return {"national_context": response.content}

# 2. Agen Adat
def adat_agent(state: AgentState):
    with open("experiments/01_triple_extraction/result.json", "r") as f:
        graph_data = f.read()
    query = state['messages'][0].content
    prompt = f"Kamu adalah tetua adat Minangkabau. Analisis pertanyaan ini berdasarkan data Knowledge Graph adat berikut: {graph_data}. Pertanyaan: '{query}'. Fokus pada hak kemenakan dan perbedaan Pusako Tinggi vs Pusako Rendah."
    response = llm.invoke([SystemMessage(content=prompt)])
    return {"adat_context": response.content}

# 3. Agen Supervisor
def supervisor_agent(state: AgentState):
    national = state.get("national_context", "")
    adat = state.get("adat_context", "")
    query = state['messages'][0].content
    prompt = f"Kamu adalah Hakim Supervisor yang ahli dalam pluralisme hukum. Tugasmu adalah mensintesis jawaban dari perspektif Nasional: {national} dan perspektif Adat: {adat}. Pertanyaan User: {query}. Akui adanya konflik norma dan jelaskan solusi pluralistik."
    response = llm.invoke([SystemMessage(content=prompt)])
    return {"final_synthesis": response.content}

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("national_law", national_agent)
workflow.add_node("adat_law", adat_agent)
workflow.add_node("adjudicator", supervisor_agent)

workflow.set_entry_point("national_law")
workflow.add_edge("national_law", "adat_law")
workflow.add_edge("adat_law", "adjudicator")
workflow.add_edge("adjudicator", END)

app = workflow.compile()

def run_experiment_3():
    query = "Seorang ayah Minangkabau meninggal. Dia meninggalkan rumah yang dibeli dari hasil kerjanya sendiri. Siapa yang lebih berhak: anak kandungnya atau kemenakannya?"
    print(f"User Query: {query}")
    inputs = {"messages": [HumanMessage(content=query)]}
    final_state = app.invoke(inputs)
    print("\n--- FINAL SYNTHESIS ---\n")
    print(final_state["final_synthesis"])

if __name__ == "__main__":
    run_experiment_3()