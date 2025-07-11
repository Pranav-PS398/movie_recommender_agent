# ✅ Evaluation Guide

This document explains how to evaluate and test the functionality of the TV Shows Recommender Agent.

---

## 🔁 Test Workflow

### 1. Basic Interaction Flow

**Prompt:**
```
what are some good thriller shows?
```

**Expected Behavior:**
- Agent uses `get_show_names` tool with query:
  ```
  top thriller shows of this week
  ```
- Extracted shows (e.g., "Squid Game", "Dexter", "Alice in Borderland") are printed to the console.

---

### 2. Telegram Delivery

**Prompt:**
```
send them to telegram
```

**Expected Behavior:**
- Agent uses `send_to_telegram` tool
- You receive the list of shows in your specified Telegram chat.

---

### 3. Memory Check

**Prompt:**
```
suggest more
```

**Expected Behavior:**
- Agent checks memory and returns only **new shows** (not already shown)

---



## 📓 Evaluation Criteria

- 🔍 **LLM Reasoning**: Understands casual prompts and generates correct tool calls  
- 🛠️ **Tool Use**: Calls the correct tools with formatted inputs  
- 🧠 **Memory Handling**: Avoids repeats using LangGraph memory  
- 📬 **Telegram Output**: Cleanly sends messages when asked

---

## ✅ Tips

- Check the terminal for printed tool steps and memory state.
- Inspect Telegram to confirm end-to-end delivery works.
