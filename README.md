# 📞 AI Calling Agent (Realtime Voice Assistant)

This project demonstrates an intelligent voice-based call agent built with **Python**, **Twilio Media Streams**, and a locally managed realtime NLP engine.  
The agent can listen, interpret, interrupt, and respond in human-like phone conversations, making it ideal for inbound call-automation use cases.

---

## 💡 Overview
The AI Calling Agent enables real-time, two-way audio communication between a caller and an AI assistant.

* Voice is streamed via **Twilio Media Streams**.  
* Speech is transcribed and processed locally for intent recognition and response generation.

**Key differentiators**

- Maintains persistent conversation context  
- Handles interruptions and speech truncation  
- Integrates low-latency audio feedback  
- Modular design for swapping in custom NLP/ASR models  

---

## ⚙️ Tech Stack
| Layer | Tools |
|-------|-------|
| Core Language | Python 3.10 + |
| Telephony | Twilio Voice + Media Streams |
| Transport | WebSockets (bi-directional audio) |
| ASR (optional) | Vosk or custom model |
| API Server | Uvicorn + FastAPI |
| Config | `.env`-driven (secrets never in code) |
| Deployment | Docker-ready |

---

## 📦 Features
| Category | Description |
|----------|-------------|
| 🔄 Streaming | Full-duplex audio between Twilio and your app |
| 🧠 NLP | Intent-based dynamic responses |
| 🔊 Voice | Customisable prompts & TTS |
| 🛑 Interrupts | Detect user barge-in and reset stream |
| 🔐 Security | `.env` secrets, robust `.gitignore` |
| 🐳 DevOps | Docker Compose sample for prod |

---

## 📚 Use Cases
- Customer-support automation  
- Voice-enabled internal helpdesks  
- Virtual receptionists  
- Survey bots for feedback col

