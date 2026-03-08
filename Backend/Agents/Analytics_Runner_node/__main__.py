from a2a.types import AgentSkill, AgentCapabilities, AgentCard
from a2a.server.apps import A2AStarletteApplication
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.request_handlers import DefaultRequestHandler
from agent_executor import Analysis_Runner_Agent_Executor
import uvicorn


if __name__ == "__main__":



    agent_skill = AgentSkill(
        id="analytics_explanation",
        name="Operational Analytics Explanation",
        description=(
            "Interprets analytics results from operational data investigations "
            "and produces a detailed operational investigation report. "
            "Connects signals across orders, payments, shipments, inventory, "
            "returns, and user activity to explain operational issues."
        ),
        tags=[
            "analytics",
            "investigation",
            "root-cause-analysis",
            "operations",
            "explanation"
        ]
    )


    # --------------------------------------------------
    # Agent Card
    # --------------------------------------------------

    agent_card = AgentCard(
        name="Analytics_Runner_Agent",
        description=(
            "Agent responsible for interpreting analytics results generated "
            "from operational data investigations. Produces structured "
            "operational investigation reports including signals, root causes, "
            "and operational impact insights."
        ),
        url="http://localhost:8010",
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
        agent_executor=Analysis_Runner_Agent_Executor(),
        task_store=InMemoryTaskStore()
    )




    app = A2AStarletteApplication(
        http_handler=request_handler,
        agent_card=agent_card
    )




    uvicorn.run(
        app.build(),
        host="0.0.0.0",
        port=8010
    )