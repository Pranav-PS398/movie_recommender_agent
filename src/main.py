import os
from dotenv import load_dotenv
import requests
import json
from openai import OpenAI
from firecrawl import FirecrawlApp
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()


# ----------------- OpenAI Key Setup -----------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ----------------- Memory -----------------
memory = MemorySaver()

# ----------------- OpenAI LLM Setup -----------------
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
    openai_api_key=OPENAI_API_KEY
)
load_dotenv()  


# ----------------- Tool 1: Get Shows -----------------
@tool
def get_show_names(google_query: str) -> str:
    """
    Searches Google for thriller shows using Serper API,
    scrapes the first link with Firecrawl (in markdown),
    and extracts a list of show names using OpenAI GPT-4o.
    """
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

    # Step 1: Google Search
    serper_url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    response = requests.post(serper_url, headers=headers, json={"q": google_query})

    if response.status_code != 200:
        return "[]"

    # Get all organic results
    organic_results = response.json().get("organic", [])

    # Filter for the first Rotten Tomatoes link
    rottentomatoes_link = next(
        (result.get("link") for result in organic_results if "rottentomatoes.com" in result.get("link", "")),
        None
    )

    if not rottentomatoes_link:
        print("❌ No Rotten Tomatoes link found in search results.")
        return "[]"

    # Step 2: Scrape with Firecrawl
    app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
    scrape_status = app.scrape_url(rottentomatoes_link, formats=["markdown"])
    markdown = scrape_status.markdown

    if not markdown:
        return "[]"

    # Step 3: GPT-4o JSON Extraction using new OpenAI client
    prompt = f"""
You are a helpful data extractor.
Below is markdown content from a website listing movies and shows.
Return the data as:
{{ "movies": ["Show 1", "Show 2", "Show 3"] }}
⚠️ Do not wrap the result in markdown, quotes, or code blocks.
Here is the content:{markdown}
"""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return completion.choices[0].message.content.strip()
    except Exception:
        return f"[Error extracting from: {rottentomatoes_link}]"

# ----------------- Tool 2: Telegram Sender -----------------
@tool
def send_to_telegram(message: str) -> dict:
    """
    Sends a message to Telegram using a hardcoded bot token and chat ID.
    """
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }

    response = requests.post(url, data=payload)
    return response.json()

# ----------------- Tools and Prompt -----------------
tools = [get_show_names, send_to_telegram]

system_prompt = """You are an intelligent assistant that helps users discover trending TV shows by genre and optionally send them to Telegram.

You have access to two tools:
1. `get_show_names(query)` — use this to search Google for a list of top shows in a given genre for the current week. It expects a query in the format: "top <genre> shows of this week" (e.g., "top romance shows of this week", "top thriller shows of this week", etc.).
2. `send_to_telegram(message)` — use this to send a message to the user's Telegram. The message should be a string containing the list of show names.

📌 Your job is to:
- Understand the user's intent, even if it's phrased casually (e.g., "I'm in the mood for some good action shows", or "suggest trending romantic series").
- Convert their request into a query in the format: **"top <genre> shows of this week"** before calling the `get_show_names` tool.
- If the genre is ambiguous or missing, ask the user to specify it.

🧠 Use memory to avoid suggesting the same shows again. If the user says "more" or "another 5", show only new shows not already shown. If the user says "send them to Telegram", send the most recent batch.

Always act as a smart assistant that adapts flexibly to natural user inputs but strictly follows the query format when calling tools."""

# ----------------- Agent Setup -----------------
agent_executor = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt,
    checkpointer=memory
)

# ----------------- Interactive Loop with Streaming -----------------
if __name__ == "__main__":
    print("🎬 Agent ready! Ask about thriller shows.")
    thread_id = "demo-thread-001"

    while True:
        user_input = input("\n👤 You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Exiting.")
            break

        print("🤖 Agent:")
        for step in agent_executor.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config={"configurable": {"thread_id": thread_id}},
            stream_mode="values"
        ):
            if "messages" in step:
                print(step["messages"][-1].content)
