from a2a.server.agent_execution import AgentExecutor , RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
    TaskStatus,
    TaskState
) 
from a2a.utils import new_text_artifact
from agent import Analysis_Fectcher_agent

class Analysis_Fectcher_Agent_Executor(AgentExecutor):
    def __init__(self):
        self.agent=Analysis_Fectcher_agent()
    
    async def execute(self,context:RequestContext,event_queue:EventQueue):

        user_query=context.get_user_input()

        if(user_query):
            Analytics_Scope=await self.agent.ScopeRetriver(user_query)
            if(Analytics_Scope):
                final_response=await self.agent.call_Analysis_Data_Engine_mcp_tools(Analytics_Scope)
                
        await event_queue.enqueue_event(
            TaskArtifactUpdateEvent(
                context_id=context.context_id,
                task_id=context.task_id,
                artifact=new_text_artifact(
                    "Analysis_Fetcher_Agent_Answer",
                    str(final_response)
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