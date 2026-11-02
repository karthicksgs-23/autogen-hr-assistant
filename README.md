# AutoGen HR Assistant - interactive terminal chat

Enter a job role and the AutoGen assistant generates a five-line job description. Ask
follow-up questions in the same session; type `exit` or `quit` to finish.
There is no automatically submitted task.

## Setup and run (Windows PowerShell)

Requires Python 3.10 or newer and an OpenAI API key with API credits/model access.

```powershell
cd D:\GenAI_2\week5\Day1\hr-agent
```

For a new setup, create the virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Create `.env` in the same folder as `hr_agent.py`, containing:

```dotenv
OPENAI_API_KEY=your-actual-key
```

The script loads this file automatically. Existing environment variables take
precedence. Keep `.env` private; it is excluded by `.gitignore`. API requests use
your OpenAI API account and may incur charges.

Start the assistant:

```powershell
.\.venv\Scripts\python.exe hr_agent.py
```

At `You:`, enter a job role, for example:

```text
Python Developer
```

The response appears in the terminal. You can then enter a follow-up such as
`Make it suitable for a fresher.` Blank messages are ignored. The same agent
keeps history for the current session; restarting clears that history.
AutoGen Console also displays message headers and the user task.

## Implementation

All application code is in `hr_agent.py`. It uses `AssistantAgent` named
`hr_assistant`, with a system message beginning `You are an HR assistant.`, and an
`OpenAIChatCompletionClient` configured for `gpt-4o-mini`. `asyncio.run(main())`
runs the chat, `Console(agent.run_stream(task=task))` displays replies, and a
`finally` block closes the client when the session ends or a request fails.

The system message requires exactly five numbered sentences, numbered 1. through
5., with the job title in the first bullet and no title, introduction, blank lines,
or closing text. For Python Developer roles, it covers Python development,
debugging and testing, teamwork and Git, basic Python and SQL skills, and
willingness to learn. For other roles, it adapts the content to the role. These
rules also apply to follow-up revisions. Model output may vary; inspect the
reply before capturing your screenshot.

## Troubleshooting

- Missing `dotenv` or other module: install `requirements.txt` with the same virtual environment's Python.
- Missing/invalid key: check the `OPENAI_API_KEY` entry in `.env` beside `hr_agent.py` and any existing environment variable.
- HTTP 429: check API quota, billing, or rate limits.
- Connection error: verify network access to the OpenAI API.

`requirements-lock.txt` records the verified environment. You can install that
file instead of `requirements.txt` to reproduce its versions.

Reference: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/quickstart.html
