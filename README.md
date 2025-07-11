# 🎬 TV Shows Recommender Agent

## 🧠 Objective
An intelligent agent that:
- Searches Google for trending TV shows by genre  
- Scrapes show lists from Rotten Tomatoes using Firecrawl  
- Extracts and formats the show names with GPT-4o  
- Optionally sends the recommendations to Telegram  

## ⚙️ Functionality
- 🔍 Tool 1: `get_show_names()` – Searches Google and extracts shows  
- 📬 Tool 2: `send_to_telegram()` – Sends show list to a Telegram user  
- 🧠 Maintains memory (via LangGraph) to avoid repeat suggestions  

---

## 🚀 Setup Instructions

### 1. Clone this repository

```bash
git clone https://github.com/Pranav-PS398/movie_recommender_agent
cd show-recommender-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your environment variables

Copy the `.env.example` to `.env`:

```bash
cp .env.example .env
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