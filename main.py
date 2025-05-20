import os
import json
import logging
import requests
from typing import Tuple, Dict
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
from twilio.rest import Client

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
PORT = int(os.getenv("PORT", "80"))
WIT_AI_TOKEN = os.getenv("WIT_AI_TOKEN")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

if not all([WIT_AI_TOKEN, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN]):
    raise ValueError("Missing one or more required credentials in .env file")

# Initialize Twilio REST API client (not used in this version)
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Initialize FastAPI app
app = FastAPI()

# Global dictionary to store conversation state per call (keyed by CallSid)
active_calls: Dict[str, dict] = {}

def process_user_input(text: str, state: dict) -> Tuple[str, dict]:
    """
    Process the input text based on the current conversation state.
    Returns a tuple of (reply_text, updated_state).
    This state machine simulates a hotel booking dialogue.
    If no input is provided, it repeats the current prompt.
    """
    text = text.strip()
    # If no input provided, repeat the current prompt.
    if not text:
        current_step = state.get("step", "ask_location")
        if current_step == "ask_location":
            return "Which city or hotel are you interested in?", state
        elif current_step == "ask_dates":
            return "What dates would you like to book? Please say your check-in and check-out dates.", state
        elif current_step == "ask_room_type":
            return "What type of room would you like? For example, single, double, or suite.", state
        elif current_step == "confirm":
            return "Please confirm your booking. Is that correct?", state
        else:
            return "Please provide your input.", state

    if not state or "step" not in state:
        state = {"step": "ask_location"}
        return "Which city or hotel are you interested in?", state

    step = state.get("step")
    if step == "ask_location":
        state["location"] = text
        state["step"] = "ask_dates"
        reply = f"Great! What dates would you like to book for in {text}? Please say your check-in and check-out dates."
    elif step == "ask_dates":
        state["dates"] = text
        state["step"] = "ask_room_type"
        reply = "Thank you. What type of room would you like? For example, single, double, or suite."
    elif step == "ask_room_type":
        state["room_type"] = text
        state["step"] = "confirm"
        reply = (f"Please confirm: you want to book a {state.get('room_type')} room for dates "
                 f"{state.get('dates')} in {state.get('location')}. Is that correct?")
    elif step == "confirm":
        if "yes" in text.lower():
            state["step"] = "booked"
            reply = "Your booking has been confirmed. Thank you for choosing our service."
        else:
            state = {"step": "ask_location"}
            reply = "Let's start over. Which city or hotel are you interested in?"
    elif step == "booked":
        reply = "Your booking is already confirmed. Thank you for choosing our service."
    else:
        reply = "I'm sorry, I didn't understand that. Could you please repeat?"
    
    return reply, state

@app.get("/", response_class=JSONResponse)
async def index():
    return {"message": "AI Voice Assistant with conversation flow is running!"}

@app.api_route("/incoming-call", methods=["GET", "POST"])
async def incoming_call(request: Request):
    """
    Handles incoming calls.
    Captures the Call SID and returns TwiML that uses <Gather> to capture speech input.
    """
    try:
        form = await request.form()
    except Exception as e:
        form = {}
        logger.warning("No form data received: %s", e)
    
    call_sid = form.get("CallSid", "")
    if call_sid:
        active_calls.setdefault(call_sid, {"step": "ask_location"})
        logger.info(f"Call initiated: {call_sid}")
    else:
        logger.warning("CallSid not found in request.")

    response = VoiceResponse()
    response.say("Welcome to the AI Voice Assistant.", voice="alice")
    gather = Gather(input="speech", action="/gather-response", timeout=5)
    gather.say("Which city or hotel are you interested in?", voice="alice")
    response.append(gather)
    response.say("We did not receive any input.", voice="alice")
    
    logger.debug("Returning TwiML for incoming call:\n%s", str(response))
    return HTMLResponse(content=str(response), media_type="application/xml")

@app.post("/gather-response")
async def gather_response(request: Request):
    """
    Handles the <Gather> response from Twilio.
    Processes the recognized speech, updates the conversation state, and returns new TwiML.
    Loops until the conversation reaches the 'booked' state.
    """
    form = await request.form()
    recognized_text = form.get("SpeechResult", "")
    call_sid = form.get("CallSid", "")
    logger.info("Gathered speech for call %s: %s", call_sid, recognized_text)
    
    state = active_calls.get(call_sid, {"step": "ask_location"})
    reply, updated_state = process_user_input(recognized_text, state)
    active_calls[call_sid] = updated_state

    response = VoiceResponse()
    response.say(reply, voice="alice")
    
    if updated_state.get("step") != "booked":
        # Set prompt based on the next step.
        if updated_state.get("step") == "ask_dates":
            prompt = "Please say your check-in and check-out dates."
        elif updated_state.get("step") == "ask_room_type":
            prompt = "What type of room would you like? For example, single, double, or suite."
        elif updated_state.get("step") == "confirm":
            prompt = "Please confirm your booking by saying yes, or say no to start over."
        else:
            prompt = "Please continue with your response."
        
        gather = Gather(input="speech", action="/gather-response", timeout=5)
        gather.say(prompt, voice="alice")
        response.append(gather)
    else:
        response.say("Thank you for your booking. Goodbye.", voice="alice")
        response.hangup()
    
    logger.debug("Returning TwiML for gather response:\n%s", str(response))
    return HTMLResponse(content=str(response), media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)

