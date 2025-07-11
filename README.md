# 🎬 TV Shows Recommender Agent

## 🧠 Objective
An intelligent agent that:
- Searches Google for trending TV shows by genre  
- Scrapes show lists from Rotten Tomatoes using Firecrawl  
- Extracts and formats the show names with GPT-4o  
- Optionally sends the recommendations to Telegram  
⚠️ Note: Despite the name ,The agent is specifically designed to recommend TV shows, not movies. Please ask for "thriller shows", "romance shows", etc.
## ⚙️ Functionality
- 🔍 Tool 1: `get_show_names()` – Searches Google and extracts shows  
- 📬 Tool 2: `send_to_telegram()` – Sends show list to a Telegram user  
- 🧠 Maintains memory (via LangGraph) to avoid repeat suggestions  

---

## 🚀 Setup Instructions

🔑 How to obtain the keys:
🔹 OpenAI API Key: obtain an openAI api key .

🔹 Firecrawl API Key: https://www.firecrawl.dev/

🔹 Serper.dev API Key: https://serper.dev

🔹 Telegram Bot Token: Search “@BotFather” on Telegram → create a bot → copy the token

🔹 Telegram Chat ID:

Start a chat with your bot .send a message .

Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates

Look for "chat":{"id":...} in the JSON response

### 1. Clone this repository

```bash
git clone https://github.com/Pranav-PS398/movie_recommender_agent
cd movie_recommender_agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your environment variables
For Linux/macOS:
Copy the `env.example` to `.env`:

```bash
cp env.example .env
```
For windows:
Copy the `env.example` to `.env`:

```bash
copy env.example .env
```


Then open `.env` and add your actual keys.

### 4. Run the agent

```bash
python src/main.py
```

---

## 💡 Sample Interaction

```text
👤 You: what are the top thriller shows to watch.

🤖 Agent:
1. Squid Game  
2. Alice in Borderland  
3. The Terminal List  

👤 You: send them to Telegram

🤖 Agent: Sent!
```
