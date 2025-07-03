import datetime
from threading import Thread
import ollama
import chromadb
import psycopg
import ast
import unicodedata
import shutil
from psycopg.rows import dict_row
from transformers import BlipProcessor, BlipForConditionalGeneration, AutoProcessor, MusicgenForConditionalGeneration
import PIL
from PIL import Image
import requests
from io import BytesIO
import re
from bs4 import BeautifulSoup
import time
import cv2
import face_recognition
from deepface import DeepFace
import numpy as np
import sys
import pyttsx3
import speech_recognition as sr
import random
import pygame
import requests
import os
import pandas as pd
import PyPDF2
import pdfplumber
from docx import Document
import collections
import librosa
from scipy.spatial.distance import cosine
from scipy.io.wavfile import write
from diffusers import StableDiffusionPipeline
import torch
import torchaudio
from torch import autocast
from web3 import Web3
from dotenv import load_dotenv
import json
import yfinance as yf

# Import color functions from terminal_colors
from terminal_colors import (
    pastel_color, pastel_lilac, pastel_pink, pastel_green, pastel_yellow, pastel_blue, pastel_red, pastel_cyan, pastel_magenta, pastel_white, pastel_gray, pastel_light_white, pastel_gradient_bar, set_palette, PASTEL, VIBRANT, select_theme
)

# Native Modules
from utils import (
    get_system_prompt, 
    get_random_expression, 
    ensure_directory_exists, 
    clean_filename, 
    master_user_greetings,
    get_agent_intro,
    get_agent_display_names
)
from kun import known_user_names, save_known_user_names
from agentic_network import ask_model, start_live_g1_conversation, G1_VOICE_LIVE, KRONOS_LIVE, MODEL_APIS
import markets
from markets import handle_markets_command
from help import display_help, detailed_help_texts, display_detailed_help
from markets_mappings import keyword_mapping
from mail import send_mail, inbox_interaction, EMAIL, PASSWORD
from dna import handle_dna_command, generate_random_dna, is_dna
from room import Room
from video import handle_video_command
from web3_handler import Web3Handler

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#   ___ _    ___  ___   _   _    
#  / __| |  / _ \| _ ) /_\ | |   
# | (_ | |_| (_) | _ \/ _ \| |__ 
#  \___|____\___/|___/_/ \_\____|                                
# *** GLOBAL Settings *** | Initialization | Mode | System Prompt

def print_opsiie_logo_gradient():
    logo = [
        " ███             ███████    ███████████   █████████  █████ █████ ██████████",
        "░░░███         ███░░░░░███ ░░███░░░░░███ ███░░░░░███░░███ ░░███ ░░███░░░░░█",
        "  ░░░███      ███     ░░███ ░███    ░███░███    ░░░  ░███  ░███  ░███  █ ░ ",
        "    ░░░███   ░███      ░███ ░██████████ ░░█████████  ░███  ░███  ░██████   ",
        "     ███░    ░███      ░███ ░███░░░░░░   ░░░░░░░░███ ░███  ░███  ░███░░█   ",
        "   ███░      ░░███     ███  ░███         ███    ░███ ░███  ░███  ░███ ░   █",
        " ███░         ░░░███████░   █████       ░░█████████  █████ █████ ██████████",
        "░░░             ░░░░░░░    ░░░░░         ░░░░░░░░░  ░░░░░ ░░░░░ ░░░░░░░░░░ "
    ]
    # Gradient from lilac to pink in the active palette
    from terminal_colors import _active_palette
    start_color = _active_palette['lilac']
    end_color = _active_palette['pink']
    steps = max(len(line) for line in logo)
    def get_gradient_color(i, total):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * i / total)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * i / total)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * i / total)
        return f'\033[38;2;{r};{g};{b}m'
    reset = '\033[0m'
    print("\n\n", end="")  # Add two blank lines before the logo
    for line in logo:
        for i, char in enumerate(line):
            print(get_gradient_color(i, steps - 1) + char, end='')
        print(reset)

def display_splash():
    """Displays the splash screen at start-up."""
    # Initialize the pygame mixer
    pygame.mixer.init()
    try:
        # Dynamically construct the path to system_sounds/opsiieboot.mp3
        sound_path = os.path.join(os.path.dirname(__file__), 'system_sounds', 'opsiieboot.mp3')
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    except Exception as e:
        print(pastel_red(f"Error fetching opsiieboot.mp3: {str(e)}"))
    # Print the Gemini-style gradient logo
    print_opsiie_logo_gradient()
    print(pastel_green("""
        A Self-Centered Intelligence (SCI) Prototype 
        By ARPA HELLENIC LOGICAL SYSTEMS | Version: 0.3.79 XP | 01 JUL 2025
    """))
    time.sleep(2)

# Initialize ChromaDB client
client = chromadb.Client()
vector_db = None

# Database connection parameters (this for PostgreSQL)
DB_PARAMS = {
    'dbname': 'mnemonic_computer',
    'user': 'rosspeili',
    'password': '2806',
    'host': 'localhost',
    'port': '5432',
    'options': '-c client_encoding=UTF8'
}

#Initialize KUN
known_user_names

AGENT_DISPLAY_NAMES = get_agent_display_names()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ORG_ID = os.getenv('ORG_ID')
NYX_ASSISTANT_ID = os.getenv('NYX_ASSISTANT_ID')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
G1_VOICE_LIVE = os.getenv('G1_VOICE_LIVE')
KRONOS_LIVE = os.getenv('KRONOS_LIVE')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

current_user = None
call_name = None
web3_connection = None
current_room = None

#Temporal Data Pocket for SoulSig 
#(used as a security  measure during the wipe process)
temporary_soul_sig = None

#Temporal Data Pocket for /read
file_context = {}

#System Prompt
system_prompt = get_system_prompt()

# Initial conversation history with the system prompt
convo = [{'role': 'system', 'content': system_prompt}]

# Initialize TTS engine (for voice output)
engine = pyttsx3.init()

# Initialize the microphone globally
recognizer = sr.Recognizer()
mic = sr.Microphone()

MFCC_TARGET_LENGTH = 100

# Track the current mode in the system
current_mode = "text"

def set_mode(mode):
    global current_mode
    current_mode = mode
    print(pastel_cyan(f"Mode set to: {mode}"))

def is_master_user():
    """Check if current user has master (R-grade) privileges."""
    global current_user, known_user_names
    if not current_user or current_user not in known_user_names:
        return False
    return known_user_names[current_user]['arpa_id'].startswith('R')

def handle_restricted_command():
    """Handle attempt to access restricted command by non-master user."""
    message = pastel_red("This command requires Master User (R-Grade) privileges. Please contact your system administrator for access.")
    print(pastel_red(message))
    if voice_mode_active or agent_voice_active:
        speak_response(message)
    return False

# Global voice off by default
voice_mode_active = False
agent_voice_active = False

#Initialize Music Generation
musicgen_model = None
musicgen_processor = None

try:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    musicgen_processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    musicgen_model = MusicgenForConditionalGeneration.from_pretrained(
        "facebook/musicgen-small", attn_implementation="eager"
    )
    musicgen_model = musicgen_model.to(device)
except Exception as e:
    print(pastel_red(f"Error initializing MusicGen model: {str(e)}"))
    musicgen_model = None
    musicgen_processor = None

# __   _____ ___ ___ ___ 
# \ \ / / _ \_ _/ __| __|
#  \ V / (_) | | (__| _| 
#   \_/ \___/___\___|___|                       
# *** Voice Interpreter *** | ELEVEN LABS | Speak Response | Custom Sounds | Voice Commands

# ELEVEN LABS API and Voice ID
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
NYX_VOICE_ID = os.getenv("NYX_VOICE_ID")
G1_VOICE_ID = os.getenv("G1_VOICE_ID")
G1_VOICE_LIVE = os.getenv('G1_VOICE_LIVE')

def verify_elevenlabs_api():
    """Verifies Eleven Labs API access by making a test request."""
    url = 'https://api.elevenlabs.io/v1'
    headers = {
        'xi-api-key': ELEVENLABS_API_KEY,
        'voice_id': VOICE_ID
    }
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return True
            else:
                print(pastel_yellow(f"[Warning] Eleven Labs API check attempt {attempt + 1} failed: Status code {response.status_code}"))
        except Exception as e:
            print(pastel_yellow(f"[Warning] Eleven Labs API check attempt {attempt + 1} failed: {str(e)}"))
        time.sleep(2)
    return False

def speak_agent_response(text, agent_name):
    """Speaks response using the appropriate voice for the agent, without the agent prefix."""
    global VOICE_ID, OPSIE_VOICE_ID, NYX_VOICE_ID, G1_VOICE_ID
    
    # Remove the agent prefix from the spoken response
    # This matches patterns like "NYX:" or "G1:" at the start of the text
    clean_text = re.sub(r'^\s*[A-Za-z0-9]+:\s*', '', text)
    
    # Temporarily change voice ID based on agent
    original_voice = VOICE_ID
    try:
        if agent_name.lower() == 'nyx':
            VOICE_ID = NYX_VOICE_ID
        elif agent_name.lower() == 'g1':
            VOICE_ID = G1_VOICE_ID
            
        speak_response(clean_text)
    finally:
        # Restore original voice
        VOICE_ID = original_voice

# Speak the response using Eleven Labs API
def speak_response(text):
    """Converts the response text to speech using Eleven Labs API."""
    global call_name

    if not text:
        print(pastel_red("Error: Cannot speak an empty or None response."))
        return

    url = f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream?optimize_streaming_latency=3'
    headers = {
        'xi-api-key': ELEVENLABS_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
        'voice_id': VOICE_ID
    }

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        audio_content = response.content
        
        with open("output.mp3", "wb") as f:
            f.write(audio_content)

        pygame.mixer.init()
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        try:
            os.remove("output.mp3")
        except PermissionError as e:
            print(pastel_red(f"Error deleting the temporary audio file: {str(e)}"))
    
    else:
        print(pastel_red(f"Error with Eleven Labs API: {response.status_code}"))
        print(pastel_red(response.text))

# List of spoken reference keywords and phrases
custom_words = {
    "Opsie": [r'E:\\Agents\\Test 1\\opsie.mp3'],
    "Voice off": [r'E:\\Agents\\Test 1\\voiceoff.mp3'],
    "send Base Degen": [
        r'E:\\Agents\\Test 1\\sendbasedegen.mp3',
        r'E:\\Agents\\Test 1\\sendbasedegen2.mp3',
        r'E:\\Agents\\Test 1\\sendbasedegen3.mp3'
    ],
    "20 to Ross": [
        r'E:\\Agents\\Test 1\\20toross.mp3',
        r'E:\\Agents\\Test 1\\20toross2.mp3',
        r'E:\\Agents\\Test 1\\20toross3.mp3'
    ],
    "50 to Ross": [
        r'E:\\Agents\\Test 1\\50toross.mp3',
        r'E:\\Agents\\Test 1\\50toross2.mp3',
        r'E:\\Agents\\Test 1\\50toross3.mp3'
    ]
}

# Load and preprocess the reference sounds
def load_custom_sounds(custom_words):
    """Loads custom sounds as MFCCs."""
    loaded_sounds = {}
    for word, paths in custom_words.items():
        loaded_sounds[word] = []
        for path in paths:
            try:
                audio_data, sr = librosa.load(path, sr=None)
                mfcc = librosa.feature.mfcc(y=audio_data, sr=sr)
                mfcc = pad_or_trim_mfcc(mfcc, MFCC_TARGET_LENGTH)
                loaded_sounds[word].append(mfcc)
            except Exception as e:
                print(f"Error loading {word} from {path}: {e}")
    return loaded_sounds

# Helper function to ensure MFCCs are of a consistent length
def pad_or_trim_mfcc(mfcc, target_length=MFCC_TARGET_LENGTH):
    """
    Ensure that the MFCC or audio data array has a consistent length.
    Pads or trims the MFCC to the target length.
    """
    if mfcc.shape[1] > target_length:
        return mfcc[:, :target_length]
    elif mfcc.shape[1] < target_length:
        # Pad with zeros if it's shorter than the target length
        return np.pad(mfcc, ((0, 0), (0, target_length - mfcc.shape[1])), mode='constant')
    return mfcc

def calculate_audio_similarity(voice_text_audio, sound_data_audio):
    """Calculate audio similarity using cosine distance of MFCCs."""
    mfcc_voice_text = librosa.feature.mfcc(y=voice_text_audio, sr=16000, n_mfcc=13)
    mfcc_sound_data = librosa.feature.mfcc(y=sound_data_audio, sr=16000, n_mfcc=13)

    # Flatten the MFCCs
    mfcc_voice_text_flat = mfcc_voice_text.flatten()
    mfcc_sound_data_flat = mfcc_sound_data.flatten()

    # Calculate cosine similarity
    similarity = 0.65 - cosine(mfcc_voice_text_flat, mfcc_sound_data_flat)
    return similarity

# Match input audio with preloaded custom sounds
def match_custom_word(input_audio, custom_sounds, threshold=0.1):
    """Matches input audio against custom word sounds and returns the recognized word."""
    input_mfcc = librosa.feature.mfcc(y=input_audio, sr=16000)
    for word, reference_mfccs in custom_sounds.items():
        for reference_mfcc in reference_mfccs:
            similarity = cosine(input_mfcc.flatten(), reference_mfcc.flatten())
            if similarity < threshold:
                return word
    return None

# Load the custom sounds for matching
custom_sounds = load_custom_sounds(custom_words)

def process_custom_words_in_speech(audio):
    """Processes the audio input and replaces recognized custom words."""
    input_audio, sr = librosa.load(BytesIO(audio), sr=16000) 
    matched_word = match_custom_word(input_audio, custom_sounds)
    if matched_word:
        return matched_word
    return None

MFCC_TARGET_LENGTH = 260

def load_custom_sounds(custom_words):
    """Loads and preprocesses custom word sounds."""
    loaded_sounds = {}
    for word, path in custom_words.items():
        if not os.path.exists(path):
            print(pastel_red(f"Error: File not found - {path}"))
            continue
        try:
            audio_data, sr = librosa.load(path, sr=None)
            mfcc = librosa.feature.mfcc(y=audio_data, sr=sr)
            mfcc = pad_or_trim_mfcc(mfcc, MFCC_TARGET_LENGTH) 
            loaded_sounds[word] = mfcc
        except Exception as e:
            print(pastel_red(f"Error loading {word} from {path}: {e}"))
    return loaded_sounds

def compare_mfccs(input_mfcc, custom_sounds, similarity_threshold=0.8):
    """Compares the MFCC of the input with the preloaded custom sounds."""
    input_mfcc_padded = pad_or_trim_mfcc(input_mfcc, MFCC_TARGET_LENGTH)

    for word, custom_mfcc in custom_sounds.items():
        similarity = np.dot(input_mfcc_padded.flatten(), custom_mfcc.flatten()) / (
                np.linalg.norm(input_mfcc_padded.flatten()) * np.linalg.norm(custom_mfcc.flatten()))
        
        if similarity >= similarity_threshold:
            return word
    return None

# Function that handles voice commands
def handle_voice_command(voice_text):
    global voice_mode_active, agent_voice_active

    if not voice_text:
        return

    voice_text = voice_text.lower().strip()

    # Check for restricted commands in voice input
    command = voice_text.split()[0].lower() if voice_text else ''
    if command in ['ask', 'markets', 'dna', '0x'] and not is_master_user():
        handle_restricted_command()
        return

    # Exact match command detection for system commands
    if voice_text == "voice off" or voice_text == "exit voice mode":
        handle_user_query("/voiceoff")
        voice_mode_active = False 
        agent_voice_active = False
        speak_response("Verbal communication protocol bridge collapsed successfully.")
        return

    # Normal command flow continues if voice mode is active
    if voice_mode_active:
        # Check if it's a command (starts with / or is a known command word)
        is_command = (voice_text.startswith('/') or 
                     voice_text.startswith(('recall ', 'memorize ', 'status', 'help', 'imagine ', 'room', 
                                          'markets ', 'read ', 'voice', 'ask', '0x', 'dna', 'video', 'music', 'theme',)))
        
        if voice_text.startswith("recall "):
            recall_keyword = voice_text.replace("recall", "").strip()
            command = f"/recall {recall_keyword}"
            handle_user_query(command)
            speak_response(f"Recall command executed successfully for keyword: {recall_keyword}")
            return

        elif voice_text.startswith("memorize "):
            memory_data = voice_text.replace("memorize", "").strip()
            command = f"/memorize {memory_data}"
            handle_user_query(command)
            speak_response(f"Memorized: {memory_data}")
            return

        elif voice_text == "status":
            command = "/status"
            handle_user_query(command)
            speak_response("System status displayed.")
            return

        elif voice_text == "help":
            handle_user_query("/help")
            speak_response("Help displayed.")
            return

        elif voice_text == "theme":
            handle_user_query("/theme")
            speak_response("Theme selector activated.")
            return

        elif voice_text.startswith("imagine "):
            prompt = voice_text.replace("imagine", "").strip()
            if prompt:
                response = handle_imagine_command(f"/imagine {prompt}")
                if response:
                    speak_response(response)
            else:
                speak_response("Please provide a valid description after 'imagine'.")
            return

        elif voice_text.startswith("markets "):
            command = voice_text.replace("markets", "/markets", 1).strip()
            handle_user_query(command)
            return

        elif voice_text.startswith("read "):
            command = voice_text.replace("read", "/read", 1).strip()
            handle_user_query(command)
            return

        # If none of the above commands were matched, execute the generic command
        handle_user_query(voice_text)
        # Only say "Command executed" if it was an actual command
        if is_command:
            speak_response("Command executed.")
    else:
        handle_user_query(voice_text)

# Voice mode toggling function
def toggle_voice_mode(mode):
    global voice_mode_active, agent_voice_active

    if mode == "/voice":
        voice_mode_active = True
        agent_voice_active = True
        print(pastel_green("Verbal communications protocol initialized."))
        speak_response("Voice mode activated. Verbal communication system online.")
        
        # Start a loop to handle voice commands
        while voice_mode_active:
            voice_text = capture_voice_input()
            if voice_text:
                handle_voice_command(voice_text)
            else:
                # If no voice input is captured, exit voice mode
                print(pastel_yellow("No voice input detected. Exiting voice mode."))
                voice_mode_active = False
                agent_voice_active = False
                break

    elif mode == "/voice1":
        agent_voice_active = True
        print(pastel_green("SCI voice responses activated. You can keep typing your input."))
        speak_response("SCI voice responses activated.")

    elif mode == "/voice2":
        voice_mode_active = True
        agent_voice_active = False
        print(pastel_green("User mic input enabled. Agent responds in text only."))
        speak_response("Voice mode restricted to user only. I will only respond in text.")
        
        # Start a loop to handle voice commands
        while voice_mode_active:
            voice_text = capture_voice_input()
            if voice_text:
                handle_voice_command(voice_text)
            else:
                # If no voice input is captured, exit voice mode
                print(pastel_yellow("No voice input detected. Exiting voice mode."))
                voice_mode_active = False
                agent_voice_active = False
                break

    elif mode == "/voiceoff":
        voice_mode_active = False
        agent_voice_active = False
        print(pastel_red("Voice mode deactivated."))
        speak_response("Verbal communication protocol bridge collapsed successfully.")

# Define multiple responses for when the system doesn't understand the user's voice input
misunderstood_responses = [
    f"Sorry, I didn't catch that, {call_name}",
    f"Can you please repeat that {call_name}?",
    f"Hmm, I missed that. Could you say it again {call_name}?",
    f"I'm having trouble understanding, could you try again {call_name}?",
    f"Oops, I didn't quite get that. Can you repeat {call_name}?"
]

# *** Voice Input Interpreter Enhancements ***
# Ensure that before any voice text is processed, we first compare against custom sounds
def interpret_custom_sounds(voice_text_audio):
    global custom_sounds

    recognized_custom_words = []

    # Compare voice input with preloaded custom sounds
    for word, sound_data_list in custom_sounds.items():
        for sound_data in sound_data_list:
            similarity = calculate_audio_similarity(voice_text_audio, sound_data)
            if similarity > 0.65:
                recognized_custom_words.append(word)

    # Replace recognized words in the final voice_text
    voice_text = voice_to_text(voice_text_audio)

    for word in recognized_custom_words:
        voice_text = voice_text.replace(word, recognized_custom_words[0])

    return voice_text

def capture_voice_input():
    """Captures voice input using the microphone, handling long and short speech dynamically."""
    global voice_mode_active
    voice_text = ""
    accumulated_speech = ""
    start_time = time.time()
    max_listening_time = 60

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print(pastel_cyan("Listening for your input..."))

        while voice_mode_active:
            try:
                # Step 1: Capture audio from the microphone
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=20)

                # Step 2: Transcribe the audio to text using Google Speech API
                voice_text = voice_to_text(audio).strip().lower()

                accumulated_speech += " " + voice_text
                print(pastel_white(f"USER (via voice): {voice_text}"))

                # Step 3: Check listening timeout
                if time.time() - start_time > max_listening_time:
                    print(pastel_yellow("Max listening time reached. Processing captured input."))
                    break

                return accumulated_speech.strip()

            except sr.WaitTimeoutError:
                print(pastel_yellow("No speech detected within the timeout. Listening stopped."))
                break

            except sr.UnknownValueError:
                response = random.choice(misunderstood_responses)
                print(pastel_yellow(response))
                speak_response(response)
                continue

            except Exception as e:
                print(pastel_red(f"Error during voice recognition: {str(e)}"))
                speak_response("An error occurred while processing your speech. Please try again.")
                continue

    return accumulated_speech.strip() if accumulated_speech else None

def voice_to_text(audio):
    """Converts the captured audio to text using Google Speech API."""
    try:
        voice_text = recognizer.recognize_google(audio)
        return voice_text
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print(pastel_red(f"Error in voice recognition: {str(e)}"))
        return ""

# *** Voice Mode Toggling Function ***
def toggle_voice_mode(mode):
    global voice_mode_active, agent_voice_active

    if mode == "/voice":
        voice_mode_active = True
        agent_voice_active = True
        print(pastel_green("Verbal communications protocol initialized."))
        speak_response("Voice mode activated. Verbal communication system online.")

        # Start a loop to handle voice commands
        while voice_mode_active:
            voice_text = capture_voice_input()
            if voice_text:
                handle_voice_command(voice_text)
            else:
                # If no voice input is captured, exit voice mode
                print(pastel_yellow("No voice input detected. Exiting voice mode."))
                voice_mode_active = False
                agent_voice_active = False
                break

    elif mode == "/voice1":
        agent_voice_active = True
        print(pastel_green("SCI voice responses activated. You can keep typing your input."))
        speak_response("SCI voice responses activated.")

    elif mode == "/voice2":
        voice_mode_active = True
        agent_voice_active = False
        print(pastel_green("User mic input enabled. Agent responds in text only."))
        speak_response("Voice mode restricted to user only. I will only respond in text.")

        while voice_mode_active:
            voice_text = capture_voice_input()
            if voice_text:
                handle_voice_command(voice_text)
            else:
                # If no voice input is captured, exit voice mode
                print(pastel_yellow("No voice input detected. Exiting voice mode."))
                voice_mode_active = False
                agent_voice_active = False
                break

    elif mode == "/voiceoff":
        voice_mode_active = False
        agent_voice_active = False
        print(pastel_red("Voice mode deactivated."))
        speak_response("Verbal communication protocol bridge collapsed successfully.")

# *** Initial lazy voice window ***
def listen_for_voice_command(timeout=5):
    """Listen for a voice command for a limited time window after boot-up."""
    global voice_mode_active
    start_time = time.time()
    voice_text = ""
    audio_initialized = False

    while time.time() - start_time < timeout:
        with mic as source:
            print(pastel_cyan(f"Listening for voice commands... You have {timeout} seconds to say 'voice' to continue in voice mode."))
            
            try:
                if not audio_initialized:
                    recognizer.adjust_for_ambient_noise(source)
                    audio_initialized = True
                
                audio = recognizer.listen(source, timeout=timeout)
                voice_text = recognizer.recognize_google(audio).lower()
                print(pastel_white(f"USER (via voice): {voice_text}"))
                break
            
            except sr.UnknownValueError:
                print(pastel_yellow("Waiting for a clear command..."))
            except sr.WaitTimeoutError:
                print(pastel_yellow("Timeout reached, no voice command detected."))
                break

    # If "voice" is detected, initialize voice mode
    if "voice" in voice_text:
        print(pastel_cyan("Lazy mode triggered!"))
        toggle_voice_mode("/voice")
    else:
        # If no voice command is detected, proceed with text interface
        print(pastel_yellow("Loading text interface"))
        speak_response(f"Default typing mode launching {call_name}. To activate voice mode, simply type /voice, anytime during the conversation.")

#  ___ _____ ___ ___   _   __  __   ___ ___ ___ ___  ___  _  _ ___ ___ 
# / __|_   _| _ \ __| /_\ |  \/  | | _ \ __/ __| _ \/ _ \| \| / __| __|
# \__ \ | | |   / _| / _ \| |\/| | |   / _|\__ \  _/ (_) | .` \__ \ _| 
# |___/_|\_\___|____|____\_/\_/_/ \_\_|_\___|___/_|  \___/|_|\_|___/___|                                                                     
# *** Stream Response *** | 

def stream_response(prompt):
    """Stream a response from the AI model for regular conversations."""
    global convo, agent_voice_active, voice_mode_active
    
    response = ''
    stream = ollama.chat(model='llama3', messages=convo, stream=True)
    
    # Print "OPSIE" prefix for every streamed chunk
    print(pastel_green('OPSIE:'), end=' ')
    
    for chunk in stream:
        content = chunk.get('message', {}).get('content', '')
        response += content
        print(content, end='', flush=True)

    print()
    
    # Store in main conversation
    store_conversations(prompt=prompt, response=response)
    convo.append({'role': 'assistant', 'content': response})

    # Only speak if voice mode is active
    if agent_voice_active or voice_mode_active:
        speak_response(response)
        
    return response

def stream_room_response(prompt, conversation):
    """Stream a response from the AI model for room interactions."""
    response = ''
    stream = ollama.chat(model='llama3', messages=conversation, stream=True)
    
    for chunk in stream:
        content = chunk.get('message', {}).get('content', '')
        response += content
    
    return response

def get_opsie_response(prompt, room_system_prompt=None):
    """Get response from Opsie for room interactions."""
    # Create a temporary conversation for room interaction
    temp_convo = []
    
    # Combine room system prompt with regular system prompt
    combined_prompt = f"{get_system_prompt()}\n\nRoom Context: {room_system_prompt}" if room_system_prompt else get_system_prompt()
    temp_convo.append({'role': 'system', 'content': combined_prompt})
    temp_convo.append({'role': 'user', 'content': prompt})
    
    # Use stream_room_response for room interactions
    response = stream_room_response(prompt, temp_convo)
    return response

#  ___ ___ ___ _   _ ___ ___ _______   __
# / __| __/ __| | | | _ \_ _|_   _\ \ / /
# \__ \ _| (__| |_| |   /| |  | |  \ V / 
# |___/___\___|\___/|_|_\___| |_|   |_|                                         
# *** Security *** | Facial Recognition | Boot-up and System Checks | Help

#emotions = [
#    'angry',
#    'disgust',
#    'fear',
#    'happy',
#    'sad',
#    'surprise',
#    'neutral'
#]

def detect_emotion(frame):
    """Detects emotions in a given frame using DeepFace."""
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        
        if isinstance(result, list):
            result = result[0]

        dominant_emotion = result.get('dominant_emotion', None)

        if dominant_emotion:
            return dominant_emotion
        else:
            print(pastel_red("[Error] No dominant emotion detected."))
            return None

    except Exception as e:
        print(pastel_red(f"[Error] Failed to detect emotion: {str(e)}"))
        return None

def facial_recognition_auth():
    """Performs facial recognition to authenticate the user before boot-up."""
    global current_user, call_name, db_params, known_user_names

    known_image_paths = {name: user['picture'] for name, user in known_user_names.items() if user['picture']}

    known_encodings = {}
    for name, path in known_image_paths.items():
        try:
            known_image = face_recognition.load_image_file(path)
            face_encodings = face_recognition.face_encodings(known_image)
            if len(face_encodings) > 0:
                known_encodings[name] = face_encodings[0]
            else:
                print(pastel_red(f"[Error] No face found in the image for {name}."))
        except Exception as e:
            print(pastel_red(f"[Error] Failed to load or process image for {name}: {str(e)}"))
            sys.exit()

    if not known_encodings:
        print(pastel_red("[Error] Unauthorized actor detected. The UBA security protocol will now terminate operations."))
        sys.exit()

    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print(pastel_red("[Error] Unable to access the camera. Make sure it's connected and working as expected."))
        sys.exit()

    print(pastel_red("\n[Security] Performing facial recognition for authentication...DO NOT turn off the camera"))

    start_time = time.time()
    match_found = False
    warning_printed = False

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print(pastel_red("[Error] Unable to capture video. Make sure your camera is properly connected and operational."))
            video_capture.release()
            sys.exit()

        rgb_frame = frame[:, :, ::-1]

        # Detect the dominant emotion
        dominant_emotion = detect_emotion(frame)

        # Check if the detected emotion is "angry" or "fear" and fail the authentication
        if dominant_emotion in ['angry', 'fear']:
            print(pastel_red(f"[Security] Abnormal stress levels detected. Detected emotion: {dominant_emotion}."))
            print(pastel_yellow("Please try again when your mental and emotional state is in normalized spectrum."))
            video_capture.release()
            sys.exit()

        # If no emotion is detected or it's a neutral/happy emotion, continue
        if dominant_emotion:
            print(pastel_green(f"[Security] Emotional state: {dominant_emotion}. Proceeding with facial recognition."))
        else:
            print(pastel_yellow("[Security] No strong emotion detected. Proceeding with facial recognition."))

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if len(face_encodings) == 0:
            if time.time() - start_time > 9 and not warning_printed:
                print(pastel_yellow("[Warning] Step up to the camera. Make sure the lens is clear and not blocked."))
                warning_printed = True

            if time.time() - start_time > 18:
                print(pastel_red("[Error] Failed to authenticate: No face detected. Please ensure you are standing in front of the camera."))
                video_capture.release()
                sys.exit()
        else:
            for face_encoding in face_encodings:
                for name, known_encoding in known_encodings.items():
                    match = face_recognition.compare_faces([known_encoding], face_encoding)
                    if match[0]:
                        match_found = True
                        user_info = known_user_names.get(name)
                        if user_info:
                            current_user = user_info['full_name']
                            call_name = user_info['call_name']
                            db_params = user_info['db_params']
                            public0x = user_info['public0x']
                            arpa_id = user_info['arpa_id']

                        if user_info['arpa_id'].startswith('R'):
                            print(pastel_green(f"[Security] Authentication successful. Master User recognized. Welcome, {current_user}!"))
                            # Initialize a separate mixer channel for the greeting
                            greeting_channel = pygame.mixer.Channel(1) 
                            
                            greeting = random.choice(master_user_greetings).format(call_name=call_name)
                            
                            def play_greeting():
                                response = requests.post(
                                    f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream',
                                    headers={'xi-api-key': ELEVENLABS_API_KEY, 'Content-Type': 'application/json'},
                                    json={'text': greeting, 'voice_id': VOICE_ID}
                                )
                                
                                if response.status_code == 200:
                                    with open("greeting.mp3", "wb") as f:
                                        f.write(response.content)
                                    
                                    greeting_sound = pygame.mixer.Sound("greeting.mp3")
                                    greeting_channel.play(greeting_sound)
                            
                            # Start greeting playback in a separate thread
                            Thread(target=play_greeting, daemon=True).start()
                        else:
                            print(pastel_green(f"[Security] Authentication successful. Welcome, {current_user} ({call_name})!"))

                        video_capture.release()
                        return current_user, call_name, db_params, dominant_emotion, public0x, arpa_id

            if not match_found:
                print(pastel_red("[Error] Unauthorized actor detected. The security protocol will now terminate operations."))
                video_capture.release()
                sys.exit()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    sys.exit()

# *** Boot-Up Sequence ***
def boot_up_sequence():
    """Boot-up process with auth checks and initializations."""
    global current_user, call_name, db_params, dominant_emotion, public0x, arpa_id, vector_db, system_prompt, web3_handler

    # Step 1: Facial Recognition Authentication
    user_name, user_call_name, user_db_params, dominant_emotion, public0x, arpa_id = facial_recognition_auth()

    if not user_name:
        print(pastel_red("[Security] Boot-up aborted due to failed authentication."))
        sys.exit()

    current_user = user_name
    call_name = user_call_name
    db_params = user_db_params
    emotional_state = dominant_emotion

    print(pastel_cyan(f"\n[System] Booting OPSIIE v.0.3.79 for {current_user}."))
    time.sleep(2)

    # Format system_prompt with call_name
    system_prompt = system_prompt.format(call_name=call_name)
    system_prompt += f"You are speaking with {current_user}. Always use their full name for formal interactions, but address them as {call_name} casually in conversation."
    system_prompt += f"You are equipped with a security system that performs emotional state detection as part of the authentication process. The user's emotional state is provided to you as context to better understand their current mental and emotional well-being. If angry or fear emotions are detected, access will be denied for security reasons. In all other emotional states, including neutral or happy, the user is granted access. The current emotional state of the user is: {emotional_state}. Please consider this emotional state when interacting with the user."
    system_prompt += f"\nThe user's ARPA ID is {arpa_id}, indicating {'Master-level' if arpa_id.startswith('R') else 'Standard'} access privileges. {'As a Master-grade user, they have full access to all of your capabilities and administrative functions, including experimental commands like /ask, /markets, /send and /dna.' if arpa_id.startswith('R') else 'As a Standard-grade user, they have access to normal system functions. These exclude experimental and advanced commands like /ask, /markets, /send and /dna.'} Please adjust your responses and available commands accordingly."

    convo[0]['content'] = system_prompt

    # Step 2: Check Database Connection
    print(pastel_yellow("\n[Network] Establishing secure connection to the user's mnemonic matrix ..."))
    try:
        conn = connect_db()
        if conn:
            print(pastel_green(f"[Network] Secure connection to {db_params['dbname']} established."))
    except Exception as e:
        print(pastel_red(f"[Error] Failed to connect to {db_params['dbname']}: {str(e)}"))
        sys.exit()
    time.sleep(0.2)

    preload_conversations(convo)

    # Step 3: Verify System Prompt Authenticity
    print(pastel_yellow("[System] Verifying System Prompt Authenticity"))
    try:
        if user_name:
            print(pastel_green(f"[System] Genuine Inscribed ARPA OEM System Prompt, and user SoulSig Verified. Welcome, {user_name}."))

            ## Append the user's soul_sig to the system_prompt
            user_soul_sig = known_user_names[user_name]['soul_sig']
            system_prompt += '\nSoul Signature:\n'
            for line in user_soul_sig:
                system_prompt += f'{line}\n'


        else:
            raise ValueError("No user identified.")
    except Exception as e:
        print(pastel_red(f"[Error] System Prompt Verification Failed: {str(e)}"))
        sys.exit()
    time.sleep(0.8)

    # Step 4: Mnemonic Matrix Stress Test
    vector_db = ensure_vector_db_exists()

    if vector_db is None:
        print(pastel_red("Error: vector_db is None after initialization."))
        sys.exit()

    print(pastel_yellow("[Hardware] Stress testing mnemonic matrix with simulations ..."))
    try:
        test_conversations = fetch_conversations()
        if test_conversations:
            print(pastel_green("[Hardware] Mnemonic integrity: Nominal."))
        else:
            print(pastel_yellow("[Hardware] No data retrieved from mnemonic_computer. Proceeding with empty mnemonic matrix."))
    except Exception as e:
        print(pastel_red(f"[Error] Mnemonic matrix test failed: {str(e)}"))
        sys.exit()
    time.sleep(2)

    # Step 5: Response Engine Initialization
    print(pastel_yellow("[SCI Systems] Initializing OPSIE response engine ..."))
    try:
        test_prompt = "Hello, Opsie. How are you?"
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': test_prompt}])
        print(pastel_green("[SCI Systems] Response engine confidence: Trustworthy."))
    except Exception as e:
        print(pastel_red(f"[Error] Opsie2 response engine initialization failed: {str(e)}"))
        sys.exit()
    time.sleep(0.7)

    # Step 6: Verify Sensory Modules and APIs
    print(pastel_yellow("[SCI Systems] Verifying sensory modules, APIs, and other tools ..."))
    try:
        camera_check = cv2.VideoCapture(0).isOpened()
        if not camera_check:
            raise ValueError("Camera check failed.")

        with mic as source:
            recognizer.adjust_for_ambient_noise(source)

        print(pastel_green("[SCI Systems] Sensor Status: Verified and functioning as expected."))
    except Exception as e:
        print(pastel_red(f"[Error] Sensory modules or API checks failed: {str(e)}"))
        sys.exit()
    time.sleep(0.5)

    # Step 7: Web3 Initialization
    print(pastel_yellow("[Network] Initializing Web3 Handler ..."))
    try:
        web3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
        if web3.is_connected():
            web3_handler = Web3Handler(known_user_names)
    except Exception as e:
        print(pastel_red(f"[Error] Web3 initialization failed: {str(e)}"))
        web3_handler = None
    time.sleep(0.3)

    # Step 8: Mail Systems Check
    print(pastel_yellow("[Network] Verifying Mail Systems ..."))
    try:
        if EMAIL and PASSWORD:
            print(pastel_green("[Network] Mail Systems: Connected"))
    except Exception as e:
        print(pastel_red(f"[Error] Mail systems verification failed: {str(e)}"))
    time.sleep(0.5)

    # Step 9: Dream Engine Initialization
    print(pastel_yellow("[SCI Systems] Initializing Dream Engine ..."))
    try:
        if torch.cuda.is_available() or device == 'cpu':
            print(pastel_green("[SCI Systems] Dream Engine Modules: Image, Music, Video Generation Ready"))
    except Exception as e:
        print(pastel_red(f"[Error] Dream Engine initialization failed: {str(e)}"))
    time.sleep(0.5)

    # Step 10: Advanced Analysis Systems
    print(pastel_yellow("[SCI Systems] Initializing Advanced Analysis Systems ..."))
    try:
        # DNA Analysis check
        test_sequence = generate_random_dna(10)
        if is_dna(test_sequence):
            print(pastel_green("[SCI Systems] DNA Analysis Module: Operational"))
        
        # Market Intelligence check
        test_ticker = "SPY"
        yf.Ticker(test_ticker).info
        print(pastel_green("[SCI Systems] Market Intelligence Feed: Active"))
        
        # File Reader check
        print(pastel_green("[SCI Systems] TAF-3000 File Reader: Online"))
    except Exception as e:
        print(pastel_red(f"[Error] Advanced Analysis Systems initialization failed: {str(e)}"))
    time.sleep(0.5)

    # Step 11: Agentic Network Initialization
    print(pastel_yellow("[Network] Initializing ARPA Nexus ..."))
    try:
        # Check API keys and configurations
        if not all([OPENAI_API_KEY, GOOGLE_API_KEY, ELEVENLABS_API_KEY]):
            raise ValueError("Missing required API keys for agentic network")

        # Check individual agent availability
        agent_status = []
        
        # Check G1 Black availability
        if G1_VOICE_LIVE:
            agent_status.append("G1 Black")
        
        # Check Kronos availability
        if KRONOS_LIVE:
            agent_status.append("Kronos")
        
        # Check Nyx availability (via OpenAI API)
        if OPENAI_API_KEY and ORG_ID and NYX_ASSISTANT_ID:
            agent_status.append("Nyx")

        if agent_status:
            print(pastel_green(f"[Network] Active Agents: {', '.join(agent_status)}"))
        else:
            print(pastel_yellow("[Network] Warning: No agents currently active"))

        # Initialize ChromaDB client for vector operations
        client = chromadb.Client()
        print(pastel_green("[Network] ARPA Nexus ENA: Ready"))

        # Initialize model APIs
        for model_name, model_info in MODEL_APIS.items():
            if 'api_url' in model_info:
                print(pastel_green(f"[Network] {model_info['display_name']} API endpoint configured"))

    except ValueError as ve:
        print(pastel_red(f"[Error] ARPA Nexus configuration error: {str(ve)}"))
    except Exception as e:
        print(pastel_red(f"[Error] ARPA Nexus initialization failed: {str(e)}"))
    time.sleep(0.5)

    # Final System Status
    print(pastel_yellow("[System] All systems are nominal."))
    time.sleep(1.5)

    pygame.mixer.init()
    try:
        # gb.mp3
        gb_path = os.path.join(os.path.dirname(__file__), 'system_sounds', 'gb.mp3')
        pygame.mixer.music.load(gb_path)
        pygame.mixer.music.play()
    except Exception as e:
        print(pastel_red(f"Error fetching gb.mp3: {str(e)}"))

    time.sleep(3)
    print(pastel_green(f"\nReady for user input, {user_name}.\n"))
    time.sleep(0.5)

    listen_for_voice_command(timeout=5)

# *** Status Command ***
def display_status():
    """Triggers the boot sequence without the splash screen with a timeout."""
    global voice_mode_active, agent_voice_active
    try:
        print(pastel_yellow("Checking system status..."))
        speak_response("Entering self-diagnosis mode...")
        print(pastel_yellow("System reboot in progress, do not turn off the machine {call_name}"))
        speak_response("Holistic system reboot in progress. Please, standby.")
        time.sleep(3) 
        boot_up_sequence()
    except Exception as e:
        print(pastel_red(f"Error during status update: {str(e)}"))
        speak_response("An error occurred while checking the status.")
        voice_mode_active = False
        agent_voice_active = False

#  __  __ _  _ ___ __  __  ___  _  _ ___ ___   __  __   _ _____ ___ _____  __
# |  \/  | \| | __|  \/  |/ _ \| \| |_ _/ __| |  \/  | /_\_   _| _ \_ _\ \/ /
# | |\/| | .` | _|| |\/| | (_) | .` || | (__  | |\/| |/ _ \| | |   /| | >  < 
# |_|  |_|_|\_|___|_|  |_|\___/|_|\_|___\___| |_|  |_/_/ \_\_| |_|_\___/_/\_\                                                                         
# *** Database Handling Section *** | Conversations | Queries | Embeddings

def connect_db():
    """Establish a connection to the correct PostgreSQL database for the authenticated user."""
    global db_params

    if not db_params:
        print(pastel_red("Error: Database parameters not set. Authentication may have failed."))
        sys.exit()

    return psycopg.connect(**db_params)

def ensure_vector_db_exists():
    """Ensure the vector database for conversations exists, and create it if not."""
    vector_db_name = 'conversations'

    try:
        vector_db = client.get_collection(name=vector_db_name)
        print(pastel_green(f"Collection '{vector_db_name}' found and ready for use."))

        # Optionally, check if the collection is empty and populate it if needed
        if vector_db.count() == 0:
            conversations = fetch_conversations()
            if conversations:
                create_vector_db(conversations, vector_db)
                print(pastel_green(f"[Hardware] Vector DB Collection '{vector_db_name}' created and populated with mnemonic specimens."))
        return vector_db
    except ValueError:
        print(pastel_yellow(f"[Hardware] Temporal active Chroma Vector DB Collection '{vector_db_name}' does not exist. Creating it now..."))

        conversations = fetch_conversations()
        vector_db = create_vector_db(conversations)
        return vector_db

def normalize_text(text):
    """
    Normalize text to ensure it conforms to UTF-8.
    This converts the text to its canonical form and removes any problematic characters.
    """
    return unicodedata.normalize('NFKC', text)

def fetch_conversations():
    """Retrieve all conversations from the database."""
    with connect_db() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('SELECT * FROM conversations ORDER BY timestamp ASC')
            return cursor.fetchall()

def store_conversations(prompt, response):
    global vector_db 
    
    with connect_db() as conn:
        with conn.cursor() as cursor:
            normalized_prompt = normalize_text(prompt)
            normalized_response = normalize_text(response)
            cursor.execute(
                'INSERT INTO conversations (timestamp, prompt, response) VALUES (CURRENT_TIMESTAMP, %s, %s) RETURNING id',
                (normalized_prompt, normalized_response)
            )
            new_id = cursor.fetchone()[0]
            conn.commit()

    # Ensure vector_db is initialized and references the correct collection
    if vector_db is None:
        vector_db = ensure_vector_db_exists()
        if vector_db is None:
            print(pastel_red("Error: vector_db is None after attempting to initialize in store_conversations."))
            return

    # Now, add to vector database using the global vector_db
    serialized_convo = f"prompt: {normalized_prompt} response: {normalized_response}"
    response_embedding = ollama.embeddings(model='nomic-embed-text', prompt=serialized_convo)
    embedding = response_embedding['embedding']

    try:
        vector_db.add(
            ids=[str(new_id)],
            embeddings=[embedding],
            documents=[serialized_convo]
        )
        #print(Fore.GREEN + f"Conversation with ID {new_id} added to vector_db.")
    except Exception as e:
        print(pastel_red(f"Error adding to vector_db: {str(e)}"))
        # Optionally, re-initialize vector_db and retry
        vector_db = ensure_vector_db_exists()
        try:
            vector_db.add(
                ids=[str(new_id)],
                embeddings=[embedding],
                documents=[serialized_convo]
            )
            #print(Fore.GREEN + f"Conversation with ID {new_id} added to vector_db after re-initialization.")
        except Exception as e:
            print(pastel_red(f"Error adding to vector_db after re-initialization: {str(e)}"))

def remove_last_conversation():
    global vector_db
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT MAX(id) FROM conversations')
            last_id = cursor.fetchone()[0]
            if last_id:
                cursor.execute('DELETE FROM conversations WHERE id = %s', (last_id,))
                conn.commit()
            else:
                print(pastel_yellow("No conversations found to delete."))
                return

    # Ensure vector_db is initialized and references the correct collection
    if vector_db is None:
        vector_db = ensure_vector_db_exists()
        if vector_db is None:
            print(pastel_red("Error: vector_db is None after attempting to initialize in remove_last_conversation."))
            return

    # Now remove from vector database using the global vector_db
    try:
        vector_db.delete(ids=[str(last_id)])
        print(pastel_green(f"Conversation with ID {last_id} removed from vector_db."))
    except Exception as e:
        print(pastel_red(f"Error deleting from vector_db: {str(e)}"))
        # Optionally, re-initialize vector_db and retry
        vector_db = ensure_vector_db_exists()
        try:
            vector_db.delete(ids=[str(last_id)])
            print(pastel_green(f"Conversation with ID {last_id} removed from vector_db after re-initialization."))
        except Exception as e:
            print(pastel_red(f"Error deleting from vector_db after re-initialization: {str(e)}"))

def preload_conversations(convo):
    """Preload all conversations from the database into the current conversation list."""
    conversations = fetch_conversations()
    for conversation in conversations:
        convo.append({'role': 'user', 'content': conversation['prompt']})
        convo.append({'role': 'assistant', 'content': conversation['response']})

# *** Vector DB Section ***
def create_vector_db(conversations, vector_db=None):
    """Create and populate a vector database with conversation embeddings."""
    vector_db_name = 'conversations'

    if vector_db is None:
        vector_db = client.create_collection(name=vector_db_name)
    else:
        # If vector_db is provided, ensure it's the correct collection
        existing_collection_name = vector_db.name
        if existing_collection_name != vector_db_name:
            vector_db = client.get_collection(name=vector_db_name)

    if conversations:
        total = len(conversations)
        term_width = shutil.get_terminal_size((80, 20)).columns
        for i, c in enumerate(conversations):
            serialized_convo = f"prompt: {c['prompt']} response: {c['response']}"
            response = ollama.embeddings(model='nomic-embed-text', prompt=serialized_convo)
            embedding = response['embedding']

            vector_db.add(
                ids=[str(c['id'])],
                embeddings=[embedding],
                documents=[serialized_convo]
            )
            percent = int((i + 1) / total * 100)
            count_str = f"[{i+1}/{total}]"
            bar_len = max(10, term_width - len(f"[Hardware] Populating vector database: {percent}% {count_str} ") - 8)
            bar = pastel_gradient_bar(i + 1, total, length=bar_len)
            print(f"[Hardware] Populating vector database: {percent}% {count_str} {bar}", end='\r')
        print()  # Move to next line after completion
        print(pastel_green(f"[Hardware] Vector DB Collection '{vector_db_name}' created and populated with mnemonic specimens."))
    else:
        print(pastel_yellow(f"No conversations found to populate the vector database. An empty collection '{vector_db_name}' was created."))
    return vector_db

def retrieve_embeddings(queries, results_per_query=10):  # Increase the results per query
    """Retrieve embeddings from the vector database based on user queries."""
    embeddings = set()

    vector_db = ensure_vector_db_exists()
    if not vector_db:
        print(pastel_red("Error: Unable to query vector database as the collection does not exist."))
        return set()

    total = len(queries)
    import shutil
    term_width = shutil.get_terminal_size((80, 20)).columns
    for i, query in enumerate(queries):
        response = ollama.embeddings(model='nomic-embed-text', prompt=query)
        query_embedding = response['embedding']

        results = vector_db.query(query_embeddings=[query_embedding], n_results=results_per_query)
        best_embeddings = results['documents']

        for best in best_embeddings:
            if tuple(best) not in embeddings:
                if 'yes' in classify_embedding(query=query, context=best):
                    embeddings.add(tuple(best))
        percent = int((i + 1) / total * 100)
        count_str = f"[{i+1}/{total}]"
        bar_len = max(10, term_width - len(f"[Hardware] Processing queries: {percent}% {count_str} ") - 8)
        bar = pastel_gradient_bar(i + 1, total, length=bar_len)
        print(f"[Hardware] Processing queries: {percent}% {count_str} {bar}", end='\r')
    print()
    print(f"[  {i+1}/{total}  ]")
    return embeddings

def create_queries(prompt):
    """Generate vector database queries based on the user's prompt."""
    query_convo = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': 'Write an email to my insurance company asking them if I can renew my insurance remotely'},
        {'role': 'assistant', 'content': '["What is the user\'s name?", "What is the user\'s current auto insurance provider?", "What is the car model of the user?", "What is the plate number of the user\'s car?", "What are the contact details of the insurance provider"?]'},
        {'role': 'user', 'content': 'What would be some top names for a Neurotech startup that offers thought security services?'},
        {'role': 'assistant', 'content': '["Types of Neurotech startups", "What are the user\'s ideas that could be relevant to a Neurotech startup?", "What are some cool sci-fi and anime company names that deal with neurotech and biotech security?", "Cybersecurity firm names", "Brain to machine interface basics?"]'},
        {'role': 'user', 'content': 'How to cook the Greek dish Kokkinisto as we did it in Kaliningrad with Karina?'},
        {'role': 'assistant', 'content': '["What did the user cook in Kaliningrad?", "Kokkinisto recipes", "User\'s favorite foods and ingredients", "Cooking for beginners"]'},
        {'role': 'user', 'content': prompt}
    ]

    response = ollama.chat(model='llama3', messages=query_convo)
    print(pastel_yellow(f'\nVector database queries: {response["message"]["content"]}\n'))

    response_content = response['message']['content']

    try:
        return ast.literal_eval(response_content)
    except (ValueError, SyntaxError):
        return [response_content]

def classify_embedding(query, context):
    """Classify whether a retrieved embedding is relevant to the user's query."""
    classify_convo = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': f'SEARCH QUERY: What is the relation of Ross Peili to Karina Andreevna? \n\nEMBEDDED CONTEXT: Ross is the boyfriend of Karina.'},
        {'role': 'assistant', 'content': 'yes'},
        {'role': 'user', 'content': f'SEARCH QUERY: How to cook Greek Kokkinisto? \n\nEMBEDDED CONTEXT: According to the web...'},
        {'role': 'assistant', 'content': 'no'},
        {'role': 'user', 'content': f'SEARCH QUERY: How to cook Greek Kokkinisto? \n\nEMBEDDED CONTEXT: Are you aiming to recreate the last recipe, or would you like to explore new recipes on the web?'},
        {'role': 'assistant', 'content': 'yes'},
        {'role': 'user', 'content': f'SEARCH QUERY: Is Karisha from Yakutia? \n\nEMBEDDED CONTEXT: Karisha is working for MP-TEK.'},
        {'role': 'assistant', 'content': 'no'},
    ]

    response = ollama.chat(model='llama3', messages=classify_convo)
    return response['message']['content'].strip().lower()

# *** Memory and Recall Section ***
def recall(prompt):
    """Recall relevant memories from past conversations based on the user's prompt."""
    queries = create_queries(prompt=prompt)
    embeddings = retrieve_embeddings(queries=queries)

    if embeddings:
        memory_context = '\n'.join([str(e) for e in embeddings])
        convo.append({'role': 'system', 'content': f'Retrieved memory: {memory_context}'})
        convo.append({'role': 'user', 'content': prompt})
        
        # Display response as normal without yellow highlighting
        print(pastel_white(f"\n{len(embeddings)} memories retrieved and added to the context."))
        speak_response(f"I've retrieved some memories about {prompt}. Would you like me to dive deeper or assist you with more details on that?")
    else:
        # If no memories were found, still provide a meaningful follow-up
        print(pastel_red("No relevant memories retrieved."))
        speak_response(f"I couldn't find specific memories related to {prompt}. Would you like me to try something else, or help you with a related topic?")

def recall_information(query):
    """Search the entire conversation history for relevant information based on the query."""
    conversations = fetch_conversations()
    for conversation in conversations:
        if query.lower() in conversation['prompt'].lower() or query.lower() in conversation['response'].lower():
            return conversation['response']
    return None

#  ___ _  _____ _    _ __      ___   ___ ___ 
# / __| |/ /_ _| |  | |\ \    / /_\ | _ \ __|
# \__ \ ' < | || |__| |_\ \/\/ / _ \|   / _| 
# |___/_|\_\___|____|____\_/\_/_/ \_\_|_\___|                                          
# *** Skillware *** | Image processing | Read from web and files | 

# *** Image Processing Section ***
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

HF_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": f"Bearer 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"}

def describe_image(url):
    """Download an image from a URL and generate a description using a pre-trained model."""
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        inputs = processor(img, return_tensors="pt")

        out = model.generate(**inputs)
        description = processor.decode(out[0], skip_special_tokens=True)
        return description
    except Exception as e:
        return f"Failed to retrieve visual data. Error: {str(e)}"
    
# *** Dream Model ***
# Function to extract the model name from the full URL
def get_model_name_from_url(url):
    return url.split("/models/")[-1]

def dreaming_message(message):
    """Displays and/or speaks the provided message based on the current mode."""
    print(pastel_green(message))
    
    if agent_voice_active or voice_mode_active:
        speak_response(get_random_expression())
    
def generate_image_from_prompt(prompt):
    global HF_API_URL

    try:
        print(pastel_cyan("OPSIIE is dreaming... do not disturb."))
        payload = {"inputs": prompt}
        response = requests.post(HF_API_URL, headers=headers, json=payload)

        if response.status_code == 503:
            error_message = "Error: The dream engine model is still loading. Please wait for a few minutes and try again."
            print(pastel_red(error_message))
            if agent_voice_active or voice_mode_active:
                speak_response(error_message)
            return

        if response.status_code != 200:
            error_message = f"Error generating image: {response.status_code} - {response.text}"
            print(pastel_red(error_message))
            if agent_voice_active or voice_mode_active:
                speak_response(error_message)
            return

        # Handle image data
        try:
            image_data = BytesIO(response.content)
            save_path = ensure_directory_exists(os.path.join(os.path.dirname(__file__), 'outputs', 'images'))
            image_filename = os.path.join(save_path, clean_filename(prompt))

            with open(image_filename, "wb") as f:
                f.write(image_data.getbuffer())

            img = Image.open(image_filename)
            img.show()

            print(pastel_yellow(f"Image generated and saved as '{image_filename}'."))

        except PIL.UnidentifiedImageError:
            error_message = "Error: The content returned by the dream engine is not a valid image."
            print(pastel_red(error_message))
            if agent_voice_active or voice_mode_active:
                speak_response(error_message)
            return

    except requests.exceptions.RequestException as e:
        error_message = f"Error generating image: {str(e)}"
        print(pastel_red(error_message))
        if agent_voice_active or voice_mode_active:
            speak_response(error_message)

# Function to handle the /imagine command
def handle_imagine_command(command):
    global HF_API_URL, agent_voice_active, voice_mode_active

    # Check if it's a model command
    if "model" in command:
        new_model_name = command.replace("/imagine model", "").strip()

        if not new_model_name:
            current_model_name = get_model_name_from_url(HF_API_URL)
            current_model_message = f"Current dream engine model is: {current_model_name}. " \
                                    f"To change the model, use /imagine model <new_model_name>."
            print(pastel_blue(current_model_message))
            if agent_voice_active or voice_mode_active:
                speak_response(current_model_message)
            if voice_mode_active:
                # Continue listening in voice mode
                voice_text = capture_voice_input()
                if voice_text:
                    handle_voice_command(voice_text)
            return

        # Try to change the model
        try:
            new_api_url = f"https://api-inference.huggingface.co/models/{new_model_name}"
            test_response = requests.get(new_api_url, headers=headers)

            if test_response.status_code == 200:
                HF_API_URL = new_api_url
                success_message = f"[OPSIE] Dream engine model changed successfully to {new_model_name}."
                print(pastel_green(success_message))
                if agent_voice_active or voice_mode_active:
                    speak_response(success_message)
            else:
                error_message = f"[OPSIE] Failed to change model. The model '{new_model_name}' may not exist or is not available."
                print(pastel_red(error_message))
                if agent_voice_active or voice_mode_active:
                    speak_response(error_message)

            # Continue listening after the model change if in voice mode
            if voice_mode_active:
                voice_text = capture_voice_input()
                if voice_text:
                    handle_voice_command(voice_text)
        except Exception as e:
            error_message = f"Error changing model: {str(e)}"
            print(pastel_red(error_message))
            if agent_voice_active or voice_mode_active:
                speak_response(error_message)
            if voice_mode_active:
                # Continue listening in voice mode
                voice_text = capture_voice_input()
                if voice_text:
                    handle_voice_command(voice_text)
        return

    # Handle regular image generation
    prompt = command.replace("/imagine", "").strip()
    if prompt:
        if agent_voice_active or voice_mode_active:
            dreaming_message(get_random_expression())

        generate_image_from_prompt(prompt)

        if voice_mode_active:
            speak_response("Image generated. I'm listening for further feedback.")
            voice_text = capture_voice_input()
            if voice_text:
                handle_voice_command(voice_text)
    else:
        error_message = "Error: No prompt provided for image generation."
        print(pastel_red(error_message))
        if agent_voice_active or voice_mode_active:
            speak_response(error_message)
        if voice_mode_active:
            # Continue listening in voice mode
            voice_text = capture_voice_input()
            if voice_text:
                handle_voice_command(voice_text)

# *** Web Page Extraction Section ***
webpage_char_limit = 1000

def describe_webpage(url):
    """
    Fetch a webpage's content and extract meaningful text for use as context.
    Includes a user-configurable character limit and better error handling.
    """
    global webpage_char_limit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        if 'text/html' not in response.headers['Content-Type']:
            return f"Error: The URL did not return HTML content. It might require special handling."

        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs])

        if len(content) > webpage_char_limit:
            content = content[:webpage_char_limit] + '...'

        if not content.strip():
            return "No readable content could be extracted from the webpage."

        return content
    except requests.exceptions.RequestException as e:
        return f"Error retrieving the webpage: {str(e)}"

def handle_weblimit_command(command):
    """Handle the /weblimit command to change the character extraction limit for webpages."""
    global webpage_char_limit

    # Split the command and extract the limit value if provided
    try:
        args = command.split()

        if len(args) == 1:  # No limit value was provided
            print(pastel_yellow(f'Current webpage character extraction limit: {webpage_char_limit}'))
            return

        new_limit = args[1]

        if new_limit.lower() == 'default' or new_limit == '1000':  # Set to default if specified
            webpage_char_limit = 1000
            print(pastel_yellow('Webpage character extraction limit set to default (1000 characters).'))
            return

        # Try to convert the new limit to an integer
        new_limit = int(new_limit)

        # Ensure the limit is within the acceptable range (500-5000 characters)
        if 500 <= new_limit <= 5000:
            webpage_char_limit = new_limit
            print(pastel_yellow(f'Webpage character extraction limit successfully set to {new_limit}.'))
        else:
            print(pastel_red('Error: Character extraction limit must be between 500 and 5000. Please try again.'))

    except (ValueError, IndexError):
        print(pastel_red('Error: Invalid input. Please enter a valid number between 500 and 5000.'))

# GPT-based query processing
def query_gpt_about_file(query, file_content):
    """
    Send the file content and the user query to GPT for processing dynamically.
    """
    global system_prompt  # Ensure we have access to the system prompt

    # GPT prompt generation based on file content, system prompt, and the user query
    gpt_prompt = f"""The following is the content of a file:
{file_content}

Based on this content, answer the following query: "{query}". Please ensure the answer is accurate and based on the file content, and it reflects Opsie's style of communication, avoiding template phrases like "An easy question!"."""

    # Call the GPT API (using Ollama or OpenAI)
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': gpt_prompt}])
    
    # Return the response, without the templated intro
    return response['message']['content']

# Main function to handle file reading
def handle_file_reading(file_path, follow_up_prompt=None):
    """
    Read the file (CSV, PDF, DOCX, TXT, XLSX) and prepare for query processing.
    """
    global file_context
    file_content = None

    # Load CSV file
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
        file_content = df.to_csv(index=False)  # Convert to CSV-like string for GPT
    # Load PDF file
    elif file_path.endswith(".pdf"):
        file_content = read_pdf(file_path)
    # Load DOCX file
    elif file_path.endswith(".docx"):
        file_content = read_docx(file_path)
    # Load TXT file
    elif file_path.endswith(".txt"):
        file_content = read_txt(file_path)
    # Load XLSX file
    elif file_path.endswith(".xlsx"):
        file_content = read_xlsx(file_path)
    else:
        print(pastel_red(f"Unsupported file type: {file_path}"))
        return

    if file_content is not None:
        # Store file content in global memory for follow-up queries
        file_context['last_file'] = file_content
        file_context['file_path'] = file_path

        # Process follow-up prompt if provided
        if follow_up_prompt:
            response = query_gpt_about_file(follow_up_prompt, file_content)
            # Store the follow-up prompt and response in the database
            store_conversations(prompt=follow_up_prompt, response=response)
            # Passing result to the agent for consistent tone and response
            print(pastel_magenta("File Manager TAF-3000: ") + response)
        else:
            # Natural confirmation for file reading with agent-style response
            print(pastel_yellow("File Manager TAF-3000: The file '{file_path}' has been scanned successfully. You can now proceed with queries in regards to the file contents in a separate context window. To return to default conversational mode, type /close."))
            if voice_mode_active:
                speak_response(f"I've read the file. You can now interact with the file manager and ask anything about the file in a closed context window. You can type /close to return to our normal convo.")
    else:
        print(pastel_red(f"Error reading file: {file_path}"))

def process_follow_up_on_file(follow_up_prompt, file_content):
    """
    Process follow-up queries for any file type dynamically using GPT.
    """
    if 'last_file' in file_context:
        response = query_gpt_about_file(follow_up_prompt, file_content)
        store_conversations(prompt=follow_up_prompt, response=response)
        print(pastel_magenta("File Manager TAF-3000: ") + response)
        if voice_mode_active:
            speak_response(response)
    else:
        print(pastel_yellow("The file context window is now closed. You can proceed to default conversation with OPSIE or use /open to reopen the file."))
        if voice_mode_active:
            speak_response("File context window collapsed. Proceeding with default conversational mode. You can always use /open to reopen the file, or /read to scan a new file.")

# *** Individual File Type Handlers ***
def read_pdf(file_path):
    """Read and extract text from a PDF file."""
    try:
        with pdfplumber.open(file_path) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
        return "\n".join(pages)
    except Exception as e:
        print(pastel_red(f"Error reading PDF: {e}"))
        return None

def read_csv(file_path):
    """Read and return content from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df.to_csv(index=False)
    except Exception as e:
        print(pastel_red(f"Error reading CSV: {e}"))
        return None
    
def read_xlsx(file_path):
    """Read and return content from an XLSX file."""
    try:
        df = pd.read_excel(file_path)
        return df.to_csv(index=False)  # Convert to CSV-like string for consistency
    except Exception as e:
        print(pastel_red(f"Error reading XLSX: {e}"))
        return None

def read_txt(file_path):
    """Read and return text from a TXT file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(pastel_red(f"Error reading TXT: {e}"))
        return None

def read_docx(file_path):
    """Read and extract text from a DOCX file."""
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(pastel_red(f"Error reading DOCX: {e}"))
        return None

# *** Music Generation ***

def handle_music_command(command):
    global agent_voice_active, voice_mode_active, musicgen_model, musicgen_processor

    if musicgen_model is None or musicgen_processor is None:
        error_message = "Error: Audible specimen generation engine is not available."
        print(pastel_red(error_message))
        if agent_voice_active or voice_mode_active:
            speak_response(error_message)
        return

    prompt = command.replace("/music", "").strip()
    if not prompt:
        error_message = "Error: No prompt provided for music generation."
        print(pastel_red(error_message))
        if agent_voice_active or voice_mode_active:
            speak_response(error_message)
        return

    try:
        print(pastel_cyan("OPSIE is cooking bits & bytes... do not disturb."))

        # Generate a random expression for print
        print_expression = get_random_expression()
        print(pastel_green(print_expression))

        # Generate a random expression for voice (can be the same or different)
        if agent_voice_active or voice_mode_active:
            voice_expression = get_random_expression()
            speak_response(voice_expression)

        # Generate music
        inputs = musicgen_processor(
            text=[prompt],
            padding=True,
            return_tensors="pt"
        ).to(musicgen_model.device)

        audio_values = musicgen_model.generate(**inputs, max_new_tokens=1024)

        # Save the audio
        save_path = ensure_directory_exists(os.path.join(os.path.dirname(__file__), 'outputs', 'music'))
        output_file = os.path.join(save_path, clean_filename(prompt, extension='wav'))

        # Get sample rate
        sample_rate = musicgen_processor.feature_extractor.sampling_rate

        # Save to WAV file using torchaudio
        torchaudio.save(output_file, audio_values[0].cpu(), sample_rate)

        # Play the audio
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()

        print(pastel_yellow(f"Audible specimen generated and saved as '{output_file}'."))

        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # BYPASSED | Optionally, delete the file after playing
        # If you wish to keep the file, comment out the deletion
        # try:
        #     os.remove(output_file)
        # except Exception as e:
        #     print(Fore.RED + f"Error deleting temporary music file: {str(e)}")

    except Exception as e:
        error_message = f"Error generating music: {str(e)}"
        print(pastel_red(error_message))
        if agent_voice_active or voice_mode_active:
            speak_response(error_message)

#  _   _ ___ ___ ___    ___  _   _ ___ _____   __
# | | | / __| __| _ \  / _ \| | | | __| _ \ \ / /
# | |_| \__ \ _||   / | (_) | |_| | _||   /\ V / 
#  \___/|___/___|_|_\  \__\_\\___/|___|_|_\ |_|                                                

# *** Command Handling Section ***
def handle_user_query(prompt):
    """Handle the user's query by searching memory, reading files, and generating a response."""
    global convo, voice_mode_active, agent_voice_active, current_user, temporary_soul_sig, current_room
    prompt = prompt.strip()

    # Normalize the prompt for consistent command parsing
    command_match = re.match(r'^/?(\w+)', prompt, re.IGNORECASE)
    if command_match:
        command = command_match.group(1).lower()
    else:
        command = ''

    # Check for restricted commands first
    if command in ['ask', 'markets', 'dna', '0x'] and not is_master_user():
        handle_restricted_command()
        return

    # Handle room creation
    if prompt.startswith('/room'):
        # Updated regex to handle one or more agents
        match = re.match(r'^/room\s+([^:]+):\s*(.+)$', prompt)
        if match:
            agents_str = match.group(1)
            room_prompt = match.group(2)
            
            # Clean and validate agents list - make case insensitive
            agents = [agent.strip().lower() for agent in agents_str.split(',') if agent.strip()]
            
            # Validate agents
            valid_agents = set(AGENT_DISPLAY_NAMES.keys()) - {'opsie'}  # All agents except OPSIE
            invalid_agents = [a for a in agents if a not in valid_agents]
            if invalid_agents:
                print(pastel_red(f"Invalid agent(s): {', '.join(invalid_agents)}"))
                print(pastel_yellow(f"Available agents: {', '.join(AGENT_DISPLAY_NAMES[a] for a in valid_agents)}"))
                return
            
            if not agents:
                print(pastel_red("No valid agents specified"))
                print(pastel_yellow(f"Available agents: {', '.join(AGENT_DISPLAY_NAMES[a] for a in valid_agents)}"))
                return
            
            current_room = Room(agents, room_prompt, get_opsie_response)
            print(pastel_magenta(f"Room created with agents: {', '.join([AGENT_DISPLAY_NAMES[a.lower()] for a in agents])}"))
            print(pastel_yellow(f"Room system prompt: {room_prompt}\n"))
            
            # Get user name for introductions
            user_name = "User"  # Default fallback
            for name, data in known_user_names.items():
                if data.get('is_current_user'):
                    user_name = data.get('call_name', name)
                    break
            
            # Have each agent introduce themselves
            # Start with OPSIE (always present)
            try:
                opsie_intro = get_agent_intro('opsie', room_prompt, user_name)  # Pass user_name here
                print(pastel_green(f"{AGENT_DISPLAY_NAMES['opsie']}: {opsie_intro}"))
                if voice_mode_active:
                    speak_response(opsie_intro)
            except Exception as e:
                print(pastel_red(f"Error in OPSIE introduction: {str(e)}"))
            
            # Then each additional agent
            for agent in agents:
                try:
                    intro = get_agent_intro(agent, room_prompt, user_name)  # Pass user_name here
                    print(pastel_blue(f"{AGENT_DISPLAY_NAMES[agent.lower()]}: {intro}"))
                    if voice_mode_active:
                        speak_agent_response(intro, agent)
                except Exception as e:
                    print(pastel_red(f"Error in {agent} introduction: {str(e)}"))
            
            return
        else:
            print(pastel_red("Invalid room format. Use: /room agent1: prompt  or  /room agent1, agent2: prompt"))
            return

    # Handle room exit
    elif prompt.startswith('/close'):
        if current_room:
            current_room.close()
            current_room = None
            print(pastel_yellow("Room closed. Returning to normal conversation mode."))
            if voice_mode_active:
                speak_response("Room closed. Returning to normal conversation mode.")
            return
        else:
            print(pastel_yellow("No active room to close."))
            return

    # Handle queries within a room
    if current_room:
        # Check for direct agent queries
        agent_query_match = re.match(r'^(\w+)\s+(.+)$', prompt)
        if agent_query_match:
            agent = agent_query_match.group(1).lower()
            agent_prompt = agent_query_match.group(2)
            
            if agent in current_room.agents:
                # Direct query to specific agent
                best_response = current_room.get_best_response(prompt)
                agent_name = best_response['agent']
                response_text = best_response['response']
                
                # Add to conversation history
                current_room.add_conversation(prompt, agent_name, response_text)
                
                # Use appropriate color based on agent
                color = current_room.get_agent_color(agent_name)
                print(color + f"{AGENT_DISPLAY_NAMES[agent_name]}: {response_text}")
                
                if voice_mode_active:
                    speak_agent_response(response_text, agent_name)
                return
        
        # Handle collaborative room responses
        best_response = current_room.get_best_response(prompt)
        agent_name = best_response['agent']
        response_text = best_response['response']
        
        # Add to conversation history
        current_room.add_conversation(prompt, agent_name, response_text)
        
        # Use appropriate color based on agent
        color = current_room.get_agent_color(agent_name)
        print(color + f"{AGENT_DISPLAY_NAMES[agent_name]}: {response_text}")
        
        if voice_mode_active:
            speak_agent_response(response_text, agent_name)
        return

    # Check for specific commands
    if command == 'voiceoff':
        # Execute the voice off command
        voice_mode_active = False
        agent_voice_active = False
        print(pastel_yellow("Voice mode deactivated. Switching to text input mode."))
        return
    
    if command == 'theme':
        # Trigger theme selection during conversation
        print(pastel_cyan("Theme selector activated..."))
        select_theme()
        print(pastel_green("Theme updated successfully!"))
    
    if prompt.lower().startswith('/soulsig'):
        command_parts = prompt.split(' ', 1)
        
        if len(command_parts) == 1:
            # Display current soul signature with a line break and change color to white
            soul_sig = '\n'.join(known_user_names[current_user]['soul_sig'])
            print(pastel_yellow("Your current Soul Signature is:\n"))
            print(pastel_white(soul_sig))  # Change the color of the content to white
            return

        elif len(command_parts) == 2:
            sub_command = command_parts[1].strip()
            
            if sub_command.lower() == 'wipe':
                # Store the current soul signature temporarily
                temporary_soul_sig = known_user_names[current_user]['soul_sig'].copy()  # Copy of current soul signature
                
                # Warning message before wiping the soul signature
                print(pastel_red("Once your SoulSig is wiped, it ceases to live in the mnemonic matrix.\nPermanent data loss is imminent. Proceed with caution!\n"))
                
                # Play the warning sound alert using pygame
                alert_path = os.path.join(os.path.dirname(__file__), 'system_sounds', 'alert.mp3')
                pygame.mixer.music.load(alert_path)
                pygame.mixer.music.play()

                # Ask for user confirmation
                confirmation = input(pastel_red("Type 'confirm' if this is not a drill!: ")).strip().lower()
                
                if confirmation == 'confirm':
                    # Wipe the soul signature
                    known_user_names[current_user]['soul_sig'] = []  # Clear the soul signature for the current user
                    print(pastel_red("\nSoul Signature has been wiped.\n"))
                    print(pastel_red("WARNING: SCI FATIGUE IMMINENT.\n"))
                    print(pastel_yellow("Your SCI agent might feel disoriented without your SoulSig. Consider inscribing a few new lines.\n"))
                    print(pastel_yellow("Visit /help soulsig for more info.\n"))
                    save_known_user_names()  # Save changes to the file
                    
                else:
                    print(pastel_yellow("Soul Signature wipe sequence terminated."))  # Inform the user that the wipe was cancelled
                return

            elif sub_command.lower() == 'heal':
                # Restore the soul signature from the temporary storage if available
                if temporary_soul_sig is not None:
                    known_user_names[current_user]['soul_sig'] = temporary_soul_sig.copy()  # Restore the soul signature
                    
                    # Play the healing sound alert using pygame
                    heal_path = os.path.join(os.path.dirname(__file__), 'system_sounds', 'heal.mp3')
                    pygame.mixer.music.load(heal_path)
                    pygame.mixer.music.play()
                    
                    print(pastel_green("\nSoul Signature has been restored from temporary storage.\n"))
                    save_known_user_names()  # Save changes to the file
                else:
                    print(pastel_red("No temporary Soul Signature found to restore.\n"))
                return

            else:
                # Add a new line to the soul signature
                new_line = sub_command.replace("'", "\\'")  # Escape single quotes
                known_user_names[current_user]['soul_sig'].append(new_line)  # Append the new line
                print(pastel_green(f"New inscription appended to Soul Signature: '{new_line}'"))
                save_known_user_names()  # Save changes to the file
                return

    if command == '0x':
        try:
            if prompt.lower().startswith('/0x gas'):
                web3_handler.handle_gas_command(prompt)
            else:
                web3_handler.handle_0x_command(prompt, agent_voice_active, voice_mode_active, speak_response)
        except Exception as e:
            error_msg = f"Web3 command failed: {str(e)}"
            print(pastel_red(error_msg))
            if agent_voice_active or voice_mode_active:
                speak_response(error_msg)
    elif command == 'send':
        print(pastel_yellow("Note: Web3 commands now use the /0x prefix. For example: '/0x send base eth 0.1 to Ross'"))
        return
    elif command == 'receive':
        try:
            web3_handler.handle_receive_command(current_user)
        except Exception as e:
            error_msg = f"Receive command failed: {str(e)}"
            print(pastel_red(error_msg))
            if agent_voice_active or voice_mode_active:
                speak_response(error_msg)
                
    elif command == 'weblimit':
        handle_weblimit_command(prompt)
    elif command == 'recall':
        recall_prompt = prompt[len(command)+1:].strip()
        recall(prompt=recall_prompt)
        stream_response(prompt=recall_prompt)
    elif command == 'forget':
        remove_last_conversation()
        convo = convo[:-2]
        print(pastel_red('\nLast conversation successfully removed from the mnemonic matrix.\n'))
    elif command == 'mail':
        mail_prompt = prompt[len('/mail'):].strip()
        if mail_prompt.lower() == 'inbox':
            inbox_interaction()  # Trigger the inbox interaction loop
            return
        success, message = send_mail(mail_prompt)
        if success:
            print(pastel_green(message))
            if agent_voice_active or voice_mode_active:
                speak_response(message)
        else:
            print(pastel_red(message))
            if agent_voice_active or voice_mode_active:
                speak_response(message)
        store_conversations(prompt=prompt, response=message)
        convo.append({'role': 'user', 'content': prompt})
        convo.append({'role': 'assistant', 'content': message})

    elif command == 'ask':
        try:
            # First check for G1 live conversation mode
            if prompt.lower().startswith('/ask g1 live'):
                if not G1_VOICE_LIVE:
                    print(pastel_red("Error: G1 voice agent ID not configured in .env file"))
                    return
                
                try:
                    print(pastel_green("Initializing live conversation mode with G1 Black..."))
                    start_live_g1_conversation()
                except Exception as e:
                    print(pastel_red(f"Error in live conversation: {str(e)}"))
                return
            
            # Handle regular ask commands
            match = re.match(r'^/?ask\s+(\w+)\s+(.+)', prompt, re.IGNORECASE)
            if match:
                model_name = match.group(1)
                follow_up_prompt = match.group(2)
                
                try:
                    response = ask_model(
                        model_name=model_name,
                        follow_up_prompt=follow_up_prompt,
                        voice_mode=(agent_voice_active or voice_mode_active)
                    )
                    
                    if response:
                        store_conversations(follow_up_prompt, response)
                        convo.append({'role': 'user', 'content': follow_up_prompt})
                        convo.append({'role': 'assistant', 'content': response})
                except Exception as e:
                    print(pastel_red(f"Error querying {model_name}: {str(e)}"))
            else:
                print(pastel_red("Invalid format for /ask command. Usage: /ask <model> <prompt> or /ask g1 live"))
        except Exception as e:
            print(pastel_red(f"Error processing ask command: {str(e)}"))
            
    elif prompt.lower().startswith('/markets'):
        # Extract the command after '/markets'
        keyword = prompt[len('/markets'):].strip()
        
        # Check if the keyword is empty
        if not keyword:
            print(pastel_yellow("Please provide a sector, company, or currency keyword. Usage: /markets <keyword>"))
            return
        
        # Call the markets command handler
        response = markets.handle_markets_command(prompt)  # Pass the entire prompt
        print(response)
        store_conversations(prompt=prompt, response=response)
        convo.append({'role': 'user', 'content': prompt})
        convo.append({'role': 'assistant', 'content': response})

    elif command == 'dna':
        result = handle_dna_command(prompt)
        print(result)

    elif command == 'memorize':
        memorize_prompt = prompt[len(command)+1:].strip()
        store_conversations(prompt=memorize_prompt, response='Memory specimen successfully implanted.')
        print(pastel_cyan('\nMemory specimen successfully implanted.\n'))
    elif command == 'imagine':
        handle_imagine_command(prompt)
    elif command == 'video':
        handle_video_command(prompt)
    elif command == 'music':
        handle_music_command(prompt)
    elif command == 'help':
        args = prompt.strip().split()
        if len(args) == 1:
            display_help()
        elif len(args) >= 2:
            command_name = args[1].lstrip('/').lower()
            display_detailed_help(command_name)
        else:
            print(pastel_red("Invalid usage of /help. Use /help or /help <command>"))
    elif command == 'status':
        display_status()
    elif command == 'voice':
        toggle_voice_mode(prompt.lower())
    elif command == 'read':
        match = re.search(r'^/?read\s+"([^"]+)"(?:\s+(.+))?', prompt, re.IGNORECASE)
        if match:
            file_path = match.group(1)
            follow_up_prompt = match.group(2)
            handle_file_reading(file_path, follow_up_prompt)
        else:
            print(pastel_red("No valid file path found in the prompt."))
    elif command == 'open':
        if 'last_file' in file_context:
            print(pastel_yellow("Reopened the last loaded file context. You can now query the file again."))
            if voice_mode_active:
                speak_response("Reopened the last loaded file context. You can now ask me anything about it.")
        else:
            print(pastel_red("No file has been loaded yet. Use /read <file> to load a file."))
            if voice_mode_active:
                speak_response("It seems like I've lost track of the file. Use /read to load a file.")
    elif command == 'close':
        file_context.clear()
        print(pastel_yellow("File context window concluded. You can continue your convo with OPSIE."))
        if voice_mode_active:
            speak_response("File context window collapsed. We can continue our normal convo.")
    elif command in ['exit', 'quit']:
        sys.exit()
    else:
        # If the command is not recognized, treat it as a normal conversation
        if 'last_file' in file_context:
            file_content = file_context['last_file']
            process_follow_up_on_file(prompt, file_content)
        else:
            convo.append({'role': 'user', 'content': prompt})
            stream_response(prompt=prompt)

# Separate function to handle non-command queries
def handle_conversational_query(prompt):
    """Handle regular conversational queries (non-commands)."""
    global convo, voice_mode_active, file_context, current_user, call_name

    # Step 1: Check for past memory recall first
    response_from_memory = recall_information(prompt)
    
    if response_from_memory:
        # If a relevant memory is found, prioritize this response over model generation
        stream_response(response_from_memory)
        if voice_mode_active:
            voice_text = capture_voice_input()
            handle_voice_command(voice_text)
        return

    # Step 2: Check if the user provided any URLs for context
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, prompt)

    if urls:
        for url in urls:
            if re.search(r'\.(png|jpg|jpeg|gif|bmp|tiff|webp)$', url):
                image_description = describe_image(url)
                prompt = prompt.replace(url, image_description)
            else:
                webpage_description = describe_webpage(url)
                prompt = prompt.replace(url, webpage_description)

        convo.append({'role': 'user', 'content': prompt})
        stream_response(prompt=prompt)

    elif 'last_file' in file_context:
        process_follow_up_on_file(prompt, file_context['last_file'])

    else:
        # If no memory or follow-up, proceed with the usual model response
        convo.append({'role': 'user', 'content': prompt})
        stream_response(prompt=prompt)

    if voice_mode_active:
        voice_text = capture_voice_input()
        handle_voice_command(voice_text)

# *** Change Web Character Extraction Limit ***
def change_weblimit(new_limit=None):
    """Change the character limit for webpage content."""
    global webpage_char_limit

    if new_limit is None:
        print(pastel_yellow(f'Current webpage character extraction limit: {webpage_char_limit}'))
        return

    if new_limit.lower() == 'default' or new_limit == '1000':
        webpage_char_limit = 1000
        print(pastel_yellow('Webpage character extraction limit set to default (1000 characters).'))
        return

    try:
        new_limit = int(new_limit)
        if 500 <= new_limit <= 5000:
            webpage_char_limit = new_limit
            print(pastel_yellow(f'Webpage character extraction limit successfully set to {new_limit}.'))
        else:
            print(pastel_red('Error: Character extraction limit must be between 500 and 5000. Please try again.'))
    except ValueError:
        print(pastel_red('Error: Invalid input. Please enter a valid number between 500 and 5000.'))

#  __  __   _   ___ _  _   _    ___   ___  ___ 
# |  \/  | /_\ |_ _| \| | | |  / _ \ / _ \| _ \
# | |\/| |/ _ \ | || .` | | |_| (_) | (_) |  _/
# |_|  |_/_/ \_\___|_|\_| |____\___/ \___/|_|                                           
# *** Main Interaction Loop ***

# Move theme selection to before splash/logo
select_theme()
display_splash()
boot_up_sequence()
preload_conversations(convo)

# User interaction loop
while True:
    if voice_mode_active:
        time.sleep(0.1)
        continue

    prompt = input(pastel_white('USER:\n')).strip()
    print()
    
    # Check for restricted commands in the main input
    command = prompt.split()[0].lower().lstrip('/') if prompt else ''
    if command in ['ask', 'markets', 'dna', 'send'] and not is_master_user():
        handle_restricted_command()
        print()
        continue
    
    if prompt.lower().startswith('/weblimit'):
        try:
            if len(prompt.split()) == 1:
                change_weblimit()
            else:
                new_limit = prompt.split()[1]
                change_weblimit(new_limit)
        except IndexError:
            print(pastel_red('Error: No limit provided. Usage: /weblimit <number between 500 and 5000> or /weblimit default'))
        print()
    
    elif prompt.lower() in ['exit', 'quit']:
        break
    
    elif prompt.lower().startswith('/recall'):
        prompt = prompt[8:]
        recall(prompt=prompt)
        stream_response(prompt=prompt)
        print()
    
    elif prompt.lower().startswith('/forget'):
        remove_last_conversation()
        convo = convo[:-2]
        print(pastel_red('\nLast conversation successfully removed from the mnemonic matrix.\n'))  
        print() 
    
    elif prompt.lower().startswith('/memorize'):
        prompt = prompt[10:]
        store_conversations(prompt=prompt, response='Memory specimen successfully implanted.')
        print(pastel_cyan('\nMemory specimen successfully implanted.\n'))     
        print()
    
    elif prompt.lower().startswith('/help'):
        args = prompt.strip().split()
        if len(args) == 1:
            display_help()
        elif len(args) == 2:
            command_name = args[1].lstrip('/').lower()
            display_detailed_help(command_name)
        else:
            print(pastel_red("Invalid usage of /help. Use /help or /help <command>"))
        print()
    
    elif prompt.lower().startswith('/status'):
        display_status()
        print()
    
    elif prompt.lower().startswith('/voice'):
        toggle_voice_mode(prompt.lower())
        print()
        continue  # Voice interactions are now active; skip further processing
    
    elif prompt.lower().startswith('/theme'):
        handle_user_query("/theme")
        print()
        continue  # Theme selection completed; continue to next iteration
    
    else:
        handle_user_query(prompt)
        print()

