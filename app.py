import streamlit as st
import pandas as pd
import json
from deep_translator import GoogleTranslator
from gtts import gTTS
import os, time

# --- Page Config ---
st.set_page_config(page_title="AgriVision Pro", layout="wide", initial_sidebar_state="expanded")

# --- Fixed CSS: Small Emojis + High Quantity + Clean UI ---
st.markdown("""
    <style>
    .stApp { background-color: #0a192f; }

    /* Background Animation */
    .floating-container {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        overflow: hidden; z-index: 0; pointer-events: none;
    }

    .floating-emoji {
        position: absolute; display: block; bottom: -100px;
        animation: animate 20s linear infinite;
        font-size: 1.2rem; /* Reduced size */
        opacity: 0.12;
    }

    @keyframes animate {
        0% { transform: translateY(0) rotate(0deg); opacity: 0; }
        20% { opacity: 0.15; }
        80% { opacity: 0.15; }
        100% { transform: translateY(-110vh) rotate(360deg); opacity: 0; }
    }

    .glass-card {
        background: #112240 !important;
        border: 1px solid #233554;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        position: relative;
        z-index: 1;
    }

    p, span, label, .stMarkdown { color: #ccd6f6 !important; font-weight: 600 !important; }
    h1, h2, h3 { color: #64ffda !important; margin-bottom: 5px !important; }
    
    /* Clean Selectbox - Removing the neon line */
    div[data-baseweb="select"] { border: 1px solid #233554 !important; }
    </style>

    <div class="floating-container">
        <div class="floating-emoji" style="left: 5%; animation-delay: 0s;">🌾</div>
        <div class="floating-emoji" style="left: 15%; animation-delay: 2s;">🌱</div>
        <div class="floating-emoji" style="left: 25%; animation-delay: 5s;">🚜</div>
        <div class="floating-emoji" style="left: 35%; animation-delay: 1s;">🌾</div>
        <div class="floating-emoji" style="left: 45%; animation-delay: 8s;">🍃</div>
        <div class="floating-emoji" style="left: 55%; animation-delay: 3s;">🌽</div>
        <div class="floating-emoji" style="left: 65%; animation-delay: 10s;">🌞</div>
        <div class="floating-emoji" style="left: 75%; animation-delay: 4s;">🌾</div>
        <div class="floating-emoji" style="left: 85%; animation-delay: 12s;">🍎</div>
        <div class="floating-emoji" style="left: 95%; animation-delay: 6s;">🌧️</div>
        <div class="floating-emoji" style="left: 10%; animation-delay: 15s;">🌱</div>
        <div class="floating-emoji" style="left: 30%; animation-delay: 18s;">🚜</div>
        <div class="floating-emoji" style="left: 50%; animation-delay: 14s;">🍃</div>
        <div class="floating-emoji" style="left: 70%; animation-delay: 20s;">🌽</div>
        <div class="floating-emoji" style="left: 90%; animation-delay: 22s;">🌾</div>
    </div>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_all():
    try:
        db = pd.read_csv('processed_nutrients.csv')
        weather = pd.read_csv('forecasting_data.csv')
        with open('crop_requirements.json', 'r') as f: reqs = json.load(f)
        with open('cultivation_details.json', 'r') as f: cult = json.load(f)
        with open('lang_pack.json', 'r', encoding='utf-8') as f: lp = json.load(f)
        return db, reqs, weather, cult, lp
    except: return None, None, None, None, None

db, crop_reqs, weather_db, cult_info, lang_pack = load_all()

if db is not None:
    languages = {"English": "en", "Hindi": "hi", "Marathi": "mr", "Tamil": "ta", "Telugu": "te"}
    with st.sidebar:
        st.header("Settings")
        l_choice = st.selectbox("🌐 Language", list(languages.keys()))
        t_code = languages[l_choice]
        
        def tr(text):
            if t_code == 'en' or not text: return text
            return lang_pack.get(t_code, {}).get(text, text)

        def live_tr(text, target):
            if target == 'en' or not text: return text
            try: return GoogleTranslator(source='auto', target=target).translate(str(text))
            except: return text

        states = sorted(list(set(db['State']).intersection(set(weather_db['State']))))
        sel_state = st.selectbox(f"📍 {tr('Select State')}", states)

    st.markdown(f"<h1>🌾 {tr('AgriVision-AV')}</h1>", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    all_crops = list(crop_reqs.keys())
    tr_crops = [tr(c) for c in all_crops]
    sel_crop_tr = st.selectbox(tr("Select Crop"), tr_crops)
    sel_crop = all_crops[tr_crops.index(sel_crop_tr)]
    req = crop_reqs[sel_crop]

    nut_row = db[db['State'] == sel_state].iloc[0]
    w_row = weather_db[weather_db['State'] == sel_state].iloc[0]
    
    # --- Growing Months Logic ---
    st.markdown(f"🗓️ **{tr('Best Growing Months')}**: `{req['months']}`")
    
    months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    found_m = [m for m in months_list if m.lower() in req['months'].lower()]
    if not found_m: found_m = ['June', 'July', 'Aug']
    avg_temp = w_row[found_m].mean()

    st.markdown("---")
    st.markdown(f"### 🧪 {tr('Parameters')}")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: n_in = st.number_input(tr("Nitrogen"), value=float(nut_row['Nitrogen']))
    with c2: p_in = st.number_input(tr("Phosphorus"), value=float(nut_row['Phosphorus']))
    with c3: k_in = st.number_input(tr("Potassium"), value=float(nut_row['Potassium']))
    with c4: t_in = st.number_input(tr("Avg Seasonal Temp"), value=float(avg_temp))
    with c5: r_in = st.number_input(tr("Rainfall (mm)"), value=float(w_row['Average annual rainfall (mm)']))
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button(tr("Predict & Show Advice")):
        score = 100
        if t_in < req['t_min'] or t_in > req['t_max']: score -= 30
        if r_in < req['r_min']: score -= 20
        final_y = max(0.0, (score/100)*9.0)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        res_c1, res_c2 = st.columns(2)
        res_c1.metric(tr("Suitability"), f"{score}%")
        res_c2.metric(tr("Yield"), f"{final_y:.2f} T/Ha")
        
        # Explicit Growing Month Advice
        month_advice = f"Based on your climate, the ideal time to cultivate {sel_crop} is {req['months']}."
        st.info(f"💡 {live_tr(month_advice, t_code)}")
        st.markdown('</div>', unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs([tr("Action Plan"), tr("Soil Health"), tr("Audio")])

        with tab1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            match = next((v for k, v in cult_info.items() if k.lower() in sel_crop.lower()), None)
            if match: st.markdown(f"<p>{live_tr(match, t_code)}</p>", unsafe_allow_html=True)
            st.markdown(f"### 🛡️ {tr('Pest Management')}")
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            n_col, p_col, k_col = st.columns(3)
            with n_col: st.metric(tr("Nitrogen"), f"{n_in}", f"{round(n_in-req['n'], 1)} vs {tr('Ideal')}")
            with p_col: st.metric(tr("Phosphorus"), f"{p_in}", f"{round(p_in-req['p'], 1)} vs {tr('Ideal')}")
            with k_col: st.metric(tr("Potassium"), f"{k_in}", f"{round(k_in-req['k'], 1)} vs {tr('Ideal')}")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            try:
                voice_text = f"Suitability {score} percent. The best months are {req['months']}."
                tts = gTTS(text=live_tr(voice_text, t_code), lang=t_code)
                fname = f"v_{int(time.time())}.mp3"
                tts.save(fname)
                st.audio(fname)
            except: st.error("Audio error.")
            st.markdown('</div>', unsafe_allow_html=True)