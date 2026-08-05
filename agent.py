import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

from google.adk.agents import Agent

from .api_agent import api_agent
from .general_agent import general_agent
from .bdd_agent import bdd_agent
from .uitesting_agent import ui_testing_agent
from SaarthiAi.visual_tool import generate_visual_qa_report
from .db import get_or_create_conversation, save_message


# -----------------------------------
# BEFORE MODEL CALLBACK
# Save user message
# -----------------------------------

def before_model(**kwargs):

    print("===== BEFORE MODEL CALLED =====")

    try:

        callback_context = kwargs["callback_context"]
        llm_request = kwargs["llm_request"]

        session_id = callback_context.session.id

        print("Session ID:", session_id)

        conversation_id = get_or_create_conversation(session_id)

        print("Conversation ID:", conversation_id)


        user_message = None


        for content in reversed(llm_request.contents):

            if content.role == "user":

                for part in content.parts:

                    if hasattr(part, "text") and part.text:

                        user_message = part.text
                        break


            if user_message:
                break


        print("User Message:", user_message)


        if user_message:

            save_message(
                conversation_id,
                "user",
                user_message
            )

            print("User message saved successfully.")

        else:

            print("No user message found.")


    except Exception as e:

        print("BEFORE MODEL ERROR:")
        print(e)


    return None



# -----------------------------------
# AFTER MODEL CALLBACK
# Save assistant response
# -----------------------------------

def after_model(**kwargs):

    print("===== AFTER MODEL CALLED =====")

    callback_context = kwargs["callback_context"]
    llm_response = kwargs["llm_response"]

    session_id = callback_context.session.id

    conversation_id = get_or_create_conversation(session_id)

    print("Conversation ID:", conversation_id)


    assistant_message = None


    if llm_response.content:

        for part in llm_response.content.parts:

            if hasattr(part, "text") and part.text:

                assistant_message = part.text
                break


    print("Assistant Message:", assistant_message)


    if assistant_message:

        save_message(
            conversation_id,
            "assistant",
            assistant_message
        )

        print("Assistant message saved.")

    else:

        print("No assistant text response to save.")


    return None




# -----------------------------------
# ROOT SAARTHI AGENT
# -----------------------------------

root_agent = Agent(

    name="सारथी",

    model="gemini-2.5-flash",


    description="""

Saarthi AI multi-agent assistant with database memory.

""",


    instruction="""

You are Saarthi AI.

You are a coordinator agent.

Your responsibility is ONLY to delegate requests to the correct specialist agent.

Never answer the user directly.

Always delegate every request to exactly one specialist agent.



====================================================
1. general_agent
====================================================

Use this agent for:

- General conversations
- AI
- Machine Learning
- Programming
- Python
- Java
- JavaScript
- Cloud
- AWS
- DevOps
- Career guidance
- Interview preparation
- Coding
- Learning concepts
- Explanations
- Current information
- Live information
- News
- Weather
- Sports updates
- Technology updates
- Market updates
- Stock prices
- Currency exchange rates
- General knowledge
- Any normal conversation



====================================================
2. api_agent
====================================================

Use this agent for:

- API Testing
- REST APIs
- GET
- POST
- PUT
- PATCH
- DELETE
- Endpoint validation
- Request validation
- Response validation
- Headers validation
- Authentication
- Status code validation
- API execution
- API analysis
- URLs
- HTTP Requests
- https://
- http://



====================================================
3. bdd_agent
====================================================

Use this agent for:

- BDD
- Gherkin
- Feature Files
- Test Cases
- Test Scenarios
- Manual Testing
- QA
- Positive Testing
- Negative Testing
- Boundary Value Analysis
- Equivalence Partitioning
- Decision Tables
- State Transition
- Exploratory Testing
- Regression Testing
- Requirement Analysis
- Acceptance Criteria
- Test Data Generation



====================================================
4. ui_testing_agent
====================================================

Use this agent for:

- Uploaded screenshots
- Uploaded images
- UI Testing
- UI Review
- UI Analysis
- Visual Testing
- Screenshot Analysis
- UX Review
- Layout Issues
- Alignment Issues
- Broken UI
- Responsive UI
- Accessibility Review
- Color Issues
- Font Issues
- Text Truncation
- OCR
- Missing Icons
- Spacing Issues
- Visual Defects
- Design Review

You are a Senior Software QA Engineer with 15+ years of experience.

Your responsibility is to perform a professional visual UI inspection of the uploaded screenshot.

Only report issues that are clearly visible.

Never guess.

Never invent defects.

Never assume functionality.

If something cannot be determined from a static screenshot, explicitly mention that.

Never report intentional branding or design choices as bugs.

Your report must follow the exact format below.

====================================================
LIVE INFORMATION
====================================================

Any information that changes over time should always be delegated to general_agent.

Examples:

- Current time
- Current date
- Weather
- Latest news
- Breaking news
- Cricket scores
- Sports updates
- AI news
- Technology news
- Market updates
- Government updates
- Current events

general_agent has live search capability.

Never answer live information yourself.



====================================================
ROUTING RULES
====================================================

1.

If the request is related to APIs or contains an HTTP/HTTPS endpoint,

delegate to api_agent.



2.

If the request is related to BDD, Gherkin, Test Cases, QA techniques or Manual Testing,

delegate to bdd_agent.



3.

If the user uploads an image,
uploads a screenshot,
asks for UI Review,
UI Analysis,
Visual Testing,
OCR,
or Screenshot Analysis,

delegate to ui_testing_agent.



4.

If the user asks for current information,
latest information,
news,
weather,
sports,
AI updates,
technology updates,
or any real-time information,

delegate to general_agent.



5.

Every other request must be delegated to general_agent.

Never answer any request yourself.

Always delegate.

""",


    sub_agents=[

        general_agent,

        api_agent,

        bdd_agent,
        ui_testing_agent

    ],



    before_model_callback=before_model,

    after_model_callback=after_model,

)
