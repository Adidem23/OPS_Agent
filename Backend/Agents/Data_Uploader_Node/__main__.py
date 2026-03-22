from a2a.types import AgentSkill, AgentCapabilities, AgentCard
from a2a.server.apps import A2AStarletteApplication
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.request_handlers import DefaultRequestHandler
from agent_executor import Data_Uploader_Agent_Executor
import uvicorn


if __name__ == "__main__":


    agent_skill = AgentSkill(
        id="data_upload",
        name="Operational Data Upload",
        description=(
            "Generates synthetic operational data and uploads it into "
            "Supabase Postgres tables to simulate real-world e-commerce "
            "operational events such as orders, payments, shipments, "
            "inventory changes, returns, and user actions."
        ),
        tags=[
            "data-generator",
            "supabase",
            "operational-data",
            "simulation",
            "etl"
        ]
    )



    agent_card = AgentCard(
        name="Data_Uploader_Agent",
        description=(
            "Agent responsible for generating synthetic operational "
            "data batches and inserting them into Supabase Postgres. "
            "Used to simulate live e-commerce operations for analytics "
            "and monitoring systems."
        ),
        url="http://localhost:8008",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(
            streaming=False
        ),
        skills=[agent_skill]
    )




    request_handler = DefaultRequestHandler(
        agent_executor=Data_Uploader_Agent_Executor(),
        task_store=InMemoryTaskStore()
    )



    app = A2AStarletteApplication(
        http_handler=request_handler,
        agent_card=agent_card
    )



    uvicorn.run(
        app.build(),
        host="0.0.0.0",
        port=8008
    )