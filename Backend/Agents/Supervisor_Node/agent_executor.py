from a2a.server.agent_execution import AgentExecutor , RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
    TaskStatus,
    TaskState
) 
from a2a.utils import new_text_artifact
from agent import SupervisorAgent

class SupervisorAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent=SupervisorAgent()
    
    async def execute(self,context:RequestContext,event_queue:EventQueue):

        user_query=context.get_user_input()

        # DATA_UPLOADER_NODE="http://localhost:8008"
        ANALYTICS_FETCHER_NODE="http://localhost:8009"
        ANALYTICS_RUNNER_NODE="http://localhost:8010"

        if(user_query):
                Analytics_fetcher_response=await self.agent.delegateTasks(ANALYTICS_FETCHER_NODE,user_query)
                if(Analytics_fetcher_response):
                    Analytics_runner_response=await self.agent.delegateTasks(ANALYTICS_RUNNER_NODE,Analytics_fetcher_response)
                

        await event_queue.enqueue_event(
            TaskArtifactUpdateEvent(
                context_id=context.context_id,
                task_id=context.task_id,
                artifact=new_text_artifact(
                    "final_answer",
                    str(Analytics_runner_response)
                ),
            )
        )

        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                context_id=context.context_id,
                task_id=context.task_id,
                status=TaskStatus(state=TaskState.completed),
                final=True,
            )
        )

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')