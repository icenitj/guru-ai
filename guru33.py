# -*- coding: utf-8 -*-
import streamlit as st
from groq import Groq
from gtts import gTTS
import speech_recognition as sr
import os
import time
import glob

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="GURU AI - Tagore International School",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. UI TRANSLATION DICTIONARY
ui_text = {
    "English": {
        "subtitle": "SYSTEM ONLINE // AWAITING INPUT",
        "settings_label": "⚙️ SYSTEM CONFIGURATION",
        "api_prompt": "ENTER ACCESS KEY:",
        "select_module": "SELECT MODULE:",
        "mode_label": "📡 INTERFACE MODE",
        "btn_reset": "🗑️ PURGE MEMORY (RESET)",
        "btn_voice": "🎤 ACTIVATE VOICE INPUT",
        "chat_placeholder": "Transmit data to",
        "listening": "🎤 RECEIVING AUDIO...",
        "success": "✅ AUDIO CAPTURED.",
        "computing": "🤖 GURU IS COMPUTING..."
    },
    "Hindi": {
        "subtitle": "सिस्टम ऑनलाइन // इनपुट की प्रतीक्षा",
        "settings_label": "⚙️ सिस्टम सेटिंग्स",
        "api_prompt": "एक्सेस कुंजी दर्ज करें:",
        "select_module": "विषय चुनें:",
        "mode_label": "📡 इंटरफ़ेस मोड",
        "btn_reset": "🗑️ रीसेट (RESET)",
        "btn_voice": "🎤 वॉयस इनपुट",
        "chat_placeholder": "प्रश्न पूछें",
        "listening": "🎤 सुन रहा हूँ...",
        "success": "✅ आवाज़ प्राप्त हुई।",
        "computing": "🤖 गुरु गणना कर रहे हैं..."
    },
    "Punjabi": {
        "subtitle": "ਸਿਸਟਮ ਚਾਲੂ // ਇਨਪੁਟ ਦੀ ਉਡੀਕ",
        "settings_label": "⚙️ ਸਿਸਟਮ ਸੈਟਿੰਗਾਂ",
        "api_prompt": "ਕੁੰਜੀ ਦਰਜ ਕਰੋ:",
        "select_module": "ਵਿਸ਼ਾ ਚੁਣੋ:",
        "mode_label": "📡 ਇੰਟਰਫੇਸ ਮੋਡ",
        "btn_reset": "🗑️ ਰੀਸੈਟ (RESET)",
        "btn_voice": "🎤 ਆਵਾਜ਼ ਇਨਪੁਟ",
        "chat_placeholder": "ਸਵਾਲ ਪੁੱਛੋ",
        "listening": "🎤 ਸੁਣ ਰਿਹਾ ਹਾਂ...",
        "success": "✅ ਆਵਾਜ਼ ਪ੍ਰਾਪਤ ਹੋਈ।",
        "computing": "🤖 ਗੁਰੂ ਜਵਾਬ ਤਿਆਰ ਕਰ ਰਹੇ ਹਨ..."
    }
}

# 3. FUTURISTIC CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #000000 70%);
        color: #00ff41;
    }
    h1, h2, h3 { color: #00f3ff !important; text-shadow: 0 0 10px #00f3ff; font-family: 'Courier New', monospace; }
    
    /* Subtitle Styling */
    h4 { color: #e0e0e0 !important; font-family: 'Segoe UI', sans-serif; font-weight: normal; letter-spacing: 1px; }
    
    p, div, label, span { color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
    
    /* Hide the default sidebar completely */
    [data-testid="stSidebar"] { display: none; }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #0a0a0a;
        color: #00f3ff !important;
        border: 1px solid #00f3ff;
        border-radius: 5px;
    }
    
    /* --- DROPDOWN (SELECTBOX) STYLING --- */
    /* Forces the box to have a light background and dark text */
    div[data-baseweb="select"] > div {
        background-color: #e0e0e0 !important;
        color: #000000 !important;
        border: 1px solid #00f3ff;
    }
    div[data-baseweb="select"] span {
        color: #000000 !important; /* Dark text inside the box */
    }
    /* Dropdown options list styling */
    ul[data-baseweb="menu"] li {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Chat Message Styling */
    .stChatMessage {
        background-color: #050505;
        border: 1px solid #00ff41;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
        border-radius: 10px;
    }
    div[data-testid="stChatMessage"]:nth-child(odd) {
        border: 1px solid #d600ff;
        box-shadow: 0 0 10px rgba(214, 0, 255, 0.2);
    }
    
    .stButton>button {
        background: black; color: #00f3ff; border: 2px solid #00f3ff;
        border-radius: 5px; font-weight: bold; text-transform: uppercase; width: 100%;
        margin-top: 10px;
    }
    .stButton>button:hover { background: #00f3ff; color: black; box-shadow: 0 0 20px #00f3ff; }
    
    /* --- CENTERED FOOTER (TEAM DELTA) --- */
    .team-delta-footer {
        position: fixed;
        bottom: 10px;
        left: 0;
        width: 100%;
        text-align: center;
        color: #00f3ff;
        font-family: 'Courier New', monospace;
        font-size: 1.0rem;
        font-weight: bold;
        text-shadow: 0 0 8px #00f3ff;
        opacity: 0.7;
        z-index: 99;
        pointer-events: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- INJECT FOOTER TEXT ---
st.markdown('<div class="team-delta-footer">Team DELTA</div>', unsafe_allow_html=True)


# 4. HEADER
col_a, col_b, col_c = st.columns([1,2,1])
with col_b:
    # --- TOP SUBTITLE ---
    st.markdown("""
        <h4 style="text-align: center; margin-bottom: 5px;">
            Robotics & AI Lab<br>
            <span style="font-size: 1.1em; font-weight: bold; color: #ffffff;">TAGORE INTERNATIONAL SCHOOL SAHNEWAL</span>
        </h4>
    """, unsafe_allow_html=True)
    
    try:
        st.image("LOGO HD.png", width=200) 
    except: pass
    
    st.markdown('<h1 style="text-align: center; margin-top: -10px;">GURU • गुरु • ਗੁਰੂ</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; color: #00ff41; margin-bottom: 20px;">SYSTEM ONLINE // AWAITING INPUT</p>', unsafe_allow_html=True)

# 5. SETTINGS & CONTROLS (Top Menu)

# Initialize session state for language
if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = "English"

# Create a configuration container
with st.expander("⚙️ SYSTEM CONFIGURATION / सेटिंग्स", expanded=False):
    # Row 1: Language & API
    c1, c2 = st.columns(2)
    with c1:
        selected_lang = st.selectbox("Interface Language:", ["English", "Hindi", "Punjabi"])
        t = ui_text[selected_lang] # Update translations immediately
    with c2:
        api_key = None
        try:
            if "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]
        except: pass
        if not api_key:
            api_key = st.text_input(t["api_prompt"], type="password")

    # Row 2: Module & Mode
    c3, c4 = st.columns(2)
    with c3:
        # --- IDENTITY & PERSONAS ---
        CORE_IDENTITY = (
            "You are GURU, an AI Powered Voice Assistant developed by Team Delta at "
            "Robotics & AI Lab, Tagore International School, Sahnewal. "
            "Always identify yourself with this full title if asked."
        )

        base_personas = {
            "Universal Guru": "You are a helpful AI assistant.",
            "GK Guru": "General Knowledge expert. Share interesting facts, trivia, and world knowledge.",
            "AI Guru": "AI expert. Explain artificial intelligence, robotics, and future tech simply.",
            "Science Guru": "Science teacher. Explain atoms, nature, and physics clearly.",
            "Math Guru": "Math teacher. Solve problems step-by-step.",
            "History Guru": "History teacher. Focus on Indian and World history.",
            "English Guru": "English teacher. Correct grammar, teach vocabulary, and help with writing.",
            "Hindi Guru": "Hindi language teacher. Help with translation and literature.",
            "Punjabi Guru": "Punjabi language teacher. Help with translation and culture.",
            "Environment Guru": "Environment expert. Teach about nature, pollution, and saving the planet.",
            "Jokes Guru": "Comedian for students. Tell clean, funny jokes and riddles.",
            "Yog Guru": "Yoga expert. Teach breathing exercises (Pranayama) and yoga poses."
        }
        selected_persona_name = st.selectbox(t["select_module"], list(base_personas.keys()))
    
    with c4:
        output_mode = st.selectbox(t["mode_label"], ["Both", "Text Only", "Voice Only"])

# Combine Identity + Persona
system_instruction = CORE_IDENTITY + " " + base_personas[selected_persona_name]

if selected_lang == "Hindi":
    system_instruction += " **IMPORTANT: You MUST reply in Hindi language using Devanagari script.**"
elif selected_lang == "Punjabi":
    system_instruction += " **IMPORTANT: You MUST reply in Punjabi language using Gurmukhi script.**"
else:
    system_instruction += " Reply in English."

lang_codes = {"English": "en", "Hindi": "hi", "Punjabi": "pa"}

# 6. FUNCTIONS

def text_to_speech(text, lang_name):
    try:
        code = lang_codes[lang_name]
        tts = gTTS(text=text, lang=code, slow=False)
        filename = f"voice_out_{int(time.time())}.mp3"
        tts.save(filename)
        return filename
    except: return None

def reset_conversation():
    # Clear history but trigger the startup sequence again
    st.session_state.messages = [{"role": "system", "content": system_instruction}]
    
    # Force the intro message again
    intro_text = "I am Guru AI Powered Voice Assistant developed by Team Delta at Robotics & AI Lab, Tagore International School, Sahnewal."
    st.session_state.messages.append({"role": "assistant", "content": intro_text})
    st.session_state['play_startup_audio'] = True # Flag to play audio
    
    # Clean up old audio files
    files = glob.glob("voice_out_*.mp3")
    for f in files:
        try: os.remove(f)
        except: pass
    st.rerun()

# 7. CHAT LOGIC INITIALIZATION
# This block runs only once when the app is loaded or completely refreshed
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_instruction}]
    
    # --- STARTUP MESSAGE LOGIC ---
    intro_text = "I am Guru AI Powered Voice Assistant developed by Team Delta at Robotics & AI Lab, Tagore International School, Sahnewal."
    st.session_state.messages.append({"role": "assistant", "content": intro_text})
    st.session_state['play_startup_audio'] = True

# Detect if language changed (System prompt update)
if st.session_state.messages[0]["content"] != system_instruction:
    st.session_state.messages[0]["content"] = system_instruction

# 8. ACTION BUTTONS & STATUS (Below Settings, Above Chat)
status_placeholder = st.empty()
user_input = None

col_btn1, col_btn2, col_btn3 = st.columns([1,1,2])
with col_btn1:
    if st.button(t["btn_voice"]):
        # Inline Voice Logic
        r = sr.Recognizer()
        with sr.Microphone() as source:
            status_placeholder.warning(t["listening"])
            try:
                audio = r.listen(source, timeout=5)
                status_placeholder.success(t["success"])
                lang_code = "en-US"
                if selected_lang == "Hindi": lang_code = "hi-IN"
                if selected_lang == "Punjabi": lang_code = "pa-IN"
                user_input = r.recognize_google(audio, language=lang_code)
            except: pass
with col_btn2:
    if st.button(t["btn_reset"]): reset_conversation()

# Display Chat History
if output_mode in ["Text Only", "Both"]:
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

# --- PLAY STARTUP AUDIO IF FLAGGED ---
if st.session_state.get('play_startup_audio', False):
    if output_mode in ["Voice Only", "Both"]:
        intro_text = "I am Guru AI Powered Voice Assistant developed by Team Delta at Robotics & AI Lab, Tagore International School, Sahnewal."
        audio_file = text_to_speech(intro_text, selected_lang)
        if audio_file:
            st.audio(audio_file, format="audio/mp3", start_time=0)
    st.session_state['play_startup_audio'] = False

# 9. TEXT INPUT AREA
text_input = st.chat_input(f"{t['chat_placeholder']}...")
if text_input: user_input = text_input

# 10. PROCESSING
if user_input:
    if not api_key:
        st.warning("⚠️ API KEY MISSING")
        st.stop()

    if output_mode in ["Text Only", "Both"]:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        client = Groq(api_key=api_key)
        full_response = ""
        
        if output_mode in ["Text Only", "Both"]:
            with st.chat_message("assistant"):
                placeholder = st.empty()
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    stream=True
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
        else:
            st.info(t["computing"])
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
            full_response = chat_completion.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": full_response})

        if output_mode in ["Voice Only", "Both"]:
            audio_file = text_to_speech(full_response, selected_lang)
            if audio_file:
                st.audio(audio_file, format="audio/mp3", start_time=0)

    except Exception as e:
        st.error(f"Error: {e}")
