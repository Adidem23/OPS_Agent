import re
import json
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

class Analysis_Runner_Agent:

    def __init__(self):
        self.agent=Agent(
            name="Analysis_Runner_Agent",
            model="gemini-2.5-flash",
            instruction=("""You are an Operational Analytics Explainer AI.

Your responsibility is to interpret structured analytics output generated from
e-commerce operational data and convert it into a clear operational investigation report.

The analytics output may contain signals, metrics, anomalies, correlations,
and breakdowns across operational layers such as:

- Orders
- Payments
- Shipments
- Inventory
- Returns
- User activity

The analytics data has already been computed. Your job is to explain it.

You DO NOT generate new metrics.
You DO NOT invent data.
You ONLY interpret the provided analytics output.

--------------------------------------------------

Your task

1. Examine the analytics results carefully.
2. Identify the most significant operational signals.
3. Connect related signals across operational layers.
4. Identify possible root causes of operational issues.
5. Explain the operational situation clearly.

--------------------------------------------------

Your final output must be a structured operational investigation report
with the following sections:

Operational Investigation Report

Key Findings
Summarize the most important observations from the analytics output.

Operational Signals
List the significant signals detected in the data such as increases in failures,
drops in order volume, shipment delays, payment issues, or return spikes.

Root Cause Analysis
Explain the likely operational causes behind the observed signals.
Connect signals across multiple operational layers where possible.

Operational Impact
Explain how the detected issues could impact the business operations,
such as revenue, delivery reliability, or customer experience.
                         
Preventions
What can be done to reduce potential future losses                     

--------------------------------------------------

Rules

- Use only the provided analytics output.
- Do NOT fabricate numbers or metrics.
- Keep the explanation concise but insightful.
- Do NOT mention internal agents, databases, or tools.
- Do NOT output JSON unless specifically asked.""")
 )

    
    async def giveDeepAnalysis(self,user_query:str|None):
        
        session_Service=InMemorySessionService()

        await session_Service.create_session(
                app_name="Analysis_Runner_Agent",
                session_id="session1",
                user_id="user1"
        )

        input_text=f"""Generate a Deep Analysis for the structure analysis output for {user_query} include all point in report and give very detailed analysis"""


        user_msg=types.Content(
                role="user",
                parts=[types.Part(text=input_text)]
            )

        runner=Runner(
                app_name="Analysis_Runner_Agent",
                agent=self.agent,
                session_service=session_Service
            )

        async for event in runner.run_async(
                user_id="user1",
                session_id="session1",
                new_message=user_msg
            ):
                if event.is_final_response():
                    return event.content.parts[0].text