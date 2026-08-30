import os
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from sqlalchemy.orm import Session
from database.models import College, Cutoff, CollegePlacementRecord

class AgenticRAGService:
    @staticmethod
    def create_agent_executor(session: Session):
        """
        Builds and compiles a stateful LangGraph agentic workflow powered by Groq 
        and LangChain tools for dynamic database and telemetry reasoning.
        
        - Inference Layer: Groq (llama-3.3-70b-versatile) for high-speed token generation.
        - Orchestration Layer: LangGraph state machine handling loops, tool calls, and execution state.
        """
        
        # 1. Define custom tools tied to operational database sessions
        @tool
        def query_placement_telemetry(college_name: str) -> str:
            """Queries verified placement CTC statistics for a specific engineering college."""
            college = session.query(College).filter(College.name.ilike(f"%{college_name}%")).first()
            if not college:
                return f"Institution '{college_name}' not found in master directory."
            
            placement = session.query(CollegePlacementRecord).filter_by(college_id=college.id).first()
            if not placement:
                return f"Placement telemetry records pending for {college.name}."
                
            return f"Institution: {college.name} | Average CTC: {placement.average_ctc} LPA | Peak Offer: {placement.highest_ctc} LPA | Placement Rate: {placement.placement_percentage}%"

        @tool
        def query_cutoff_rank(branch_name: str) -> str:
            """Queries historical Round-2 cutoff ranks for a given engineering branch."""
            cutoff = session.query(Cutoff).filter(Cutoff.branch_name.ilike(f"%{branch_name}%")).first()
            if not cutoff:
                return f"No cutoff telemetry found for branch '{branch_name}'."
            
            college = session.query(College).filter_by(id=cutoff.college_id).first()
            c_name = college.name if college else "Tier-1 Institution"
            
            return f"Branch: {cutoff.branch_name} at {c_name} | Round-2 Cutoff Rank: {cutoff.cutoff_rank} ({cutoff.category})"

        tools = [query_placement_telemetry, query_cutoff_rank]

        # 2. Initialize the ultra-fast Groq LPU inference engine via LangChain (langchain-groq)
        groq_api_key = os.environ.get("GROQ_API_KEY", "")
        llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0,
            groq_api_key=groq_api_key
        )
        llm_with_tools = llm.bind_tools(tools)

        # 3. Define LangGraph State structure using TypedDict and message reducers
        class AgentState(TypedDict):
            messages: Annotated[list[BaseMessage], add_messages]

        # 4. Define Graph Nodes (Logic blocks for reasoning & tool execution)
        def call_model(state: AgentState):
            """Invokes the Groq LLM with message history and requested tool bindings."""
            messages = state["messages"]
            response = llm_with_tools.invoke(messages)
            return {"messages": [response]}

        def should_continue(state: AgentState):
            """Conditional router: evaluates if the model triggered a tool call or reached completion."""
            messages = state["messages"]
            last_message = messages[-1]
            if last_message.tool_calls:
                return "tools"
            return END

        # 5. Construct the LangGraph StateGraph workflow
        workflow = StateGraph(AgentState)
        
        # Add primary agent reasoning node
        workflow.add_node("agent", call_model)
        
        # Add prebuilt tool execution node
        tool_node = ToolNode(tools=tools)
        workflow.add_node("tools", tool_node)

        # Establish cyclic edges & conditional routing
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
        workflow.add_edge("tools", "agent")  # Cyclic loop back to agent after tool output

        return workflow.compile()

    @staticmethod
    def run_agent_query(session: Session, user_query: str) -> str:
        """
        Executes the compiled LangGraph agent workflow with Groq inference 
        to synthesize a precise, multi-step reasoned answer.
        """
        try:
            app = AgenticRAGService.create_agent_executor(session)
            initial_state = {"messages": [HumanMessage(content=user_query)]}
            
            final_response = ""
            for event in app.stream(initial_state, stream_mode="values"):
                latest_msg = event["messages"][-1]
                if latest_msg.type == "ai" and latest_msg.content:
                    final_response = latest_msg.content
                    
            return final_response or "Agentic workflow completed successfully, but returned an empty text response."
        except Exception as e:
            return f"Agentic RAG execution notice: {str(e)}. (Please ensure a valid GROQ_API_KEY is configured in your environment)."
