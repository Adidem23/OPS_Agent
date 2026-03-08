from a2a.types import AgentSkill, AgentCapabilities, AgentCard
from a2a.server.apps import A2AStarletteApplication
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.request_handlers import DefaultRequestHandler
from agent_executor import Analysis_Fectcher_Agent_Executor
import uvicorn


if __name__ == "__main__":

    # --------------------------------------------------
    # Agent Skill
    # --------------------------------------------------

    agent_skill = AgentSkill(
        id="scope_extraction",
        name="Operational Scope Extraction",
        description=(
            "Extracts investigation scope parameters from user queries. "
            "Converts natural language operational questions into structured "
            "JSON filters that can be used by the analytics engine to run "
            "operational investigations."
        ),
        tags=[
            "analytics",
            "scope-extraction",
            "query-parsing",
            "nlp",
            "investigation"
        ]
    )


    # --------------------------------------------------
    # Agent Card
    # --------------------------------------------------

    agent_card = AgentCard(
        name="Analytics_Fetcher_Agent",
        description=(
            "Agent responsible for parsing user queries and extracting "
            "structured investigation parameters such as region, product, "
            "courier, payment status, and other operational filters. "
            "Provides structured scope JSON for the analytics engine."
        ),
        url="http://localhost:8009",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(
            streaming=False
        ),
        skills=[agent_skill]
    )


    # --------------------------------------------------
    # Request Handler
    # --------------------------------------------------

    request_handler = DefaultRequestHandler(
        agent_executor=Analysis_Fectcher_Agent_Executor(),
        task_store=InMemoryTaskStore()
    )


    # --------------------------------------------------
    # A2A Application
    # --------------------------------------------------

    app = A2AStarletteApplication(
        http_handler=request_handler,
        agent_card=agent_card
    )


    # --------------------------------------------------
    # Server
    # --------------------------------------------------

    uvicorn.run(
        app.build(),
        host="0.0.0.0",
        port=8009
    )