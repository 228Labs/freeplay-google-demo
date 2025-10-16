import asyncio
import logging
import os
import uuid

from freeplay import Freeplay
from freeplay_python_adk.freeplay_observability_plugin import (
    FreeplayObservabilityPlugin,
)
from freeplay_python_adk.test_runs import attach_test_info
from google.adk.apps import App
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app import root_agent

logger = logging.getLogger(__name__)

freeplay = Freeplay(
    freeplay_api_key=os.environ["FREEPLAY_API_KEY"],
    api_base=os.environ["FREEPLAY_API_URL"],
)
freeplay_project_id = os.getenv("FREEPLAY_PROJECT_ID")


async def run_step_async(runner: Runner, message: str, session_id: str) -> None:
    logger.debug(f"Running step with message: {message}")
    content = types.Content(
        role="user",
        parts=[types.Part(text=message)],
    )

    events = runner.run_async(
        user_id="test_user", session_id=session_id, new_message=content
    )

    async for event in events:
        if event.is_final_response() and event.content and event.content.parts:
            response = event.content.parts[0].text
            logger.debug(f"Output: {response}")


async def run_test_case(runner: Runner, input: str):
    session_id = str(uuid.uuid4())
    await runner.session_service.create_session(
        app_name="research_agent",
        user_id="test_user",
        session_id=session_id,
    )

    await run_step_async(
        runner,
        input,
        session_id,
    )
    await run_step_async(runner, "That's great, go ahead.", session_id)


async def run_test():
    session_service = InMemorySessionService()
    app = App(
        name="research_agent",
        root_agent=root_agent,
        plugins=[FreeplayObservabilityPlugin()],
    )
    runner = Runner(
        app=app,
        session_service=session_service,
    )

    test_run = freeplay.test_runs.create(
        project_id=freeplay_project_id,
        testlist="research_questions",
    )

    for test_case in test_run.get_trace_test_cases():
        attach_test_info(test_run.test_run_id, test_case.id)

        await run_test_case(runner, test_case.input)


if __name__ == "__main__":
    asyncio.run(run_test())
