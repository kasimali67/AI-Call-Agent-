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


🛡 Security Note All secrets are kept in .env (excluded via .gitignore)

No credentials are exposed in the codebase or Git history

🙌 Credits Inspired by real-world use cases integrating voice AI in production pipelines. Extended with flexible architecture for local NLP + cloud hybrid deployment.

🚀 Getting Started
See here for a tutorial overview of the code.

This application uses the following Twilio products in conjunction with OpenAI's Realtime API:

Voice (and TwiML, Media Streams) Phone Numbers Note

Outbound calling is beyond the scope of this app. However, we demoed one way to do it here.

Prerequisites To use the app, you will need:

Python 3.9+ We used 3.9.13 for development; download from here. A Twilio account. You can sign up for a free trial here. A Twilio number with Voice capabilities. Here are instructions to purchase a phone number. An OpenAI account and an OpenAI API Key. You can sign up here. OpenAI Realtime API access. Local Setup There are 4 required steps and 1 optional step to get the app up-and-running locally for development and testing:

Run ngrok or another tunneling solution to expose your local server to the internet for testing. Download ngrok here. (optional) Create and use a virtual environment Install the packages Twilio setup Update the .env file Open an ngrok tunnel When developing & testing locally, you'll need to open a tunnel to forward requests to your local development server. These instructions use ngrok.

Open a Terminal and run:

ngrok http 5050 Once the tunnel has been opened, copy the Forwarding URL. It will look something like: https://[your-ngrok-subdomain].ngrok.app. You will need this when configuring your Twilio number setup.

Note that the ngrok command above forwards to a development server running on port 5050, which is the default port configured in this application. If you override the PORT defined in index.js, you will need to update the ngrok command accordingly.

Keep in mind that each time you run the ngrok http command, a new URL will be created, and you'll need to update it everywhere it is referenced below.

(Optional) Create and use a virtual environment To reduce cluttering your global Python environment on your machine, you can create a virtual environment. On your command line, enter:

python3 -m venv env source env/bin/activate Install required packages In the terminal (with the virtual environment, if you set it up) run:

pip install -r requirements.txt Twilio setup Point a Phone Number to your ngrok URL In the Twilio Console, go to Phone Numbers > Manage > Active Numbers and click on the additional phone number you purchased for this app in the Prerequisites.

In your Phone Number configuration settings, update the first A call comes in dropdown to Webhook, and paste your ngrok forwarding URL (referenced above), followed by /incoming-call. For example, https://[your-ngrok-subdomain].ngrok.app/incoming-call. Then, click Save configuration.

Update the .env file Create a /env file, or copy the .env.example file to .env:

cp .env.example .env In the .env file, update the OPENAI_API_KEY to your OpenAI API key from the Prerequisites.

Run the app Once ngrok is running, dependencies are installed, Twilio is configured properly, and the .env is set up, run the dev server with the following command:

python main.py Test the app With the development server running, call the phone number you purchased in the Prerequisites. After the introduction, you should be able to talk to the AI Assistant. Have fun!

Special features Have the AI speak first To have the AI voice assistant talk before the user, uncomment the line # await send_initial_conversation_item(openai_ws). The initial greeting is controlled in async def send_initial_conversation_item(openai_ws).

Interrupt handling/AI preemption When the user speaks and OpenAI sends input_audio_buffer.speech_started, the code will clear the Twilio Media Streams buffer and send OpenAI conversation.item.truncate.

Depending on your application's needs, you may want to use the input_audio_buffer.speech_stopped event, instead, or a combination of the two.
