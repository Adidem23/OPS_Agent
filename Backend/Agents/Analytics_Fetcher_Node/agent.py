import re
import json
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from dotenv import load_dotenv
from google.genai import types
from fastmcp import Client

load_dotenv()

class Analysis_Fectcher_agent:

    def __init__(self):
        self.agent=Agent(
            name="Analysis_Fectcher_agent",
            model="gemini-2.5-flash",
            instruction=("""You are an Operational Scope Extraction Agent.

Your job is to read a user's operational question and extract investigation
parameters ("scope") that will be used to query an analytics service.

You DO NOT perform analysis.
You DO NOT explain anything.
You ONLY extract structured scope parameters.

The output MUST be a JSON object containing ONLY the parameters that are
explicitly mentioned in the user query.

Do NOT include parameters that are not present in the query.

--------------------------------------------------

Available Scope Parameters

region
Possible values:
- West India
- North India
- South India
- East India

city
Possible values:
- Mumbai
- Pune
- Delhi
- Bangalore
- Chennai
- Ahmedabad
- Kolkata

sku_id
Example values:
- CBKSJ
- SKU_102
- PROD_889

courier_name
Possible values:
- Delhivery
- BlueDart
- DTDC
- EcomExpress

warehouse_id
Example values:
- WH_MUMBAI_01
- WH_DELHI_02

payment_status
Possible values:
- success
- failed
- timeout
- pending

payment_method
Possible values:
- UPI
- Credit Card
- Debit Card
- Net Banking

device_type
Possible values:
- mobile
- desktop
- tablet

event_type
Possible values:
(order lifecycle)
- order_created
- order_confirmed
- order_cancelled
- order_shipped
- order_delivered

(shipment lifecycle)
- shipment_created
- shipment_dispatched
- in_transit
- delivery_attempted
- delivered
- delivery_failed

(user behavior)
- product_view
- add_to_cart
- checkout_started
- checkout_abandoned

return_reason
Possible values:
- damaged
- wrong_item
- not_needed
- size_issue

return_status
Possible values:
- return_requested
- return_approved
- return_completed

--------------------------------------------------

Rules

- Return ONLY a valid JSON object.
- Include ONLY parameters that appear in the query.
- Do NOT include parameters with null values.
- Do NOT add explanations.
- Do NOT wrap JSON in markdown.
- If no parameters are detected, return an empty JSON object `{}`.""")
 )

    async def call_Analysis_Data_Engine_mcp_tools(self,scope):


        client = Client("http://localhost:9500/mcp")

        async with client:

            result = await client.call_tool(
                "call_Analytics_Data_engine",
                {
                    "scope_object":scope
                }
            )

            return result
    
    async def ScopeRetriver(self,user_query:str|None):
        
        session_Service=InMemorySessionService()

        await session_Service.create_session(
                app_name="Analysis_Fectcher_agent",
                session_id="session1",
                user_id="user1"
        )

        input_text=f"""retrive the scope from given user query:{user_query} and return it as a json """


        user_msg=types.Content(
                role="user",
                parts=[types.Part(text=input_text)]
            )

        runner=Runner(
                app_name="Analysis_Fectcher_agent",
                agent=self.agent,
                session_service=session_Service
            )

        async for event in runner.run_async(
                user_id="user1",
                session_id="session1",
                new_message=user_msg
            ):
                if event.is_final_response():
                    
                    raw_text=event.content.parts[0].text

                    cleaned = re.sub(r"```json|```", "", raw_text).strip()

                    return json.loads(cleaned)