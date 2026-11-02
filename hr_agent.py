"""Week 5, Day 1: an asynchronous AutoGen HR assistant."""

import asyncio
import os
import sys
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, AuthenticationError


SYSTEM_MESSAGE = (
    "You are an HR assistant. Write a job description for the job role provided "
    "by the user. Each reply must contain exactly five lines. "
    "Each line must be one numbered bullet, numbered 1. through 5., containing "
    "one concise sentence. Mention the job title within the first bullet. "
    "For Python Developer roles, cover Python development, debugging and testing, "
    "teamwork and Git, basic Python and SQL skills, and willingness to learn. "
    "For other roles, cover equivalent responsibilities, collaboration, core "
    "skills, and willingness to learn that are relevant to that role. "
    "Do not include a separate title, introduction, blank lines, or closing text. "
    "Apply these formatting rules to follow-up revisions as well."
)


async def main() -> None:
    """Read user messages, show HR replies, and always close the model client."""
    # Load .env beside the script; existing environment variables take precedence.
    load_dotenv(Path(__file__).with_name(".env"), override=False)
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "Set OPENAI_API_KEY in the .env file beside hr_agent.py "
            "or in your environment."
        )

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=api_key,
        timeout=60,
        max_retries=2,
    )
    try:
        agent = AssistantAgent(
            name="hr_assistant",
            model_client=model_client,
            system_message=SYSTEM_MESSAGE,
        )
        print("HR Assistant ready. Enter a job role, or type exit to quit.")
        while True:
            try:
                task = input("\nYou: ").strip()
            except EOFError:
                print("\nGoodbye!")
                break
            if task.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break
            if not task:
                print("Please enter a message.")
                continue
            # Keep the same agent so follow-up questions retain conversation history.
            await Console(agent.run_stream(task=task))
    finally:
        await model_client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except ValueError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
    except AuthenticationError:
        print(
            "Unable to start: set OPENAI_API_KEY to a valid OpenAI API key.",
            file=sys.stderr,
        )
        sys.exit(1)
    except APIConnectionError:
        print("Could not reach OpenAI. Check your connection and retry.", file=sys.stderr)
        sys.exit(1)
    except APIStatusError as error:
        print(
            f"OpenAI returned HTTP {error.status_code}. "
            "Check your API account, quota, and model access.",
            file=sys.stderr,
        )
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStopped.", file=sys.stderr)
        sys.exit(130)
