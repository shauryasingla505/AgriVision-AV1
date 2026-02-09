import streamlit as st
import pandas as pd
import json
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import re

# --- Page Config ---
st.set_page_config(page_title="AgriVision Pro", layout="wide", initial_sidebar_state="expanded")

# --- UI CSS (Floating Background & High Contrast Metrics) ---
st.markdown("""
    <style>
    /* Main Background Layer */
    .stApp { 
        background-color: #020c1b; 
    }

    /* Floating Background Icons */
    .bg-animation {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        z-index: 0;
        pointer-events: none;
    }

    .bg-icon {
        position: absolute;
        font-size: 3rem;
        opacity: 0.35;
        animation: floatAround 25s linear infinite;
        filter: drop-shadow(0 0 10px #64ffda);
    }

    @keyframes floatAround {
        0% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(150px, 300px) rotate(120deg); }
        66% { transform: translate(-100px, 150px) rotate(240deg); }
        100% { transform: translate(0, 0) rotate(360deg); }
    }

    /* Content Layering */
    .main-content {
        position: relative;
        z-index: 10;
    }

    .glass-card {
        background: rgba(17, 34, 64, 0.95) !important;
        border: 2px solid #64ffda;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px -15px rgba(2,12,27,0.7);
    }

    h1, h2, h3, h4 { color: #64ffda !important; font-weight: 800; text-shadow: 2px 2px #020c1b; }
    p, span, label, li, .stMarkdown { color: #ccd6f6 !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] { color: #64ffda !important; font-size: 2.2rem !important; }
    [data-testid="stMetricDelta"] svg { fill: #64ffda !important; }
    </style>

    <div class="bg-animation">
        <div class="bg-icon" style="top:10%; left:10%; animation-duration:30s;">🌾</div>
        <div class="bg-icon" style="top:40%; left:80%; animation-duration:22s;">🍀</div>
        <div class="bg-icon" style="top:70%; left:20%; animation-duration:28s;">🌽</div>
        <div class="bg-icon" style="top:20%; left:60%; animation-duration:35s;">🚜</div>
        <div class="bg-icon" style="top:85%; left:75%; animation-duration:25s;">🌱</div>
        <div class="bg-icon" style="top:50%; left:40%; animation-duration:40s;">☀️</div>
    </div>
    """, unsafe_allow_html=True)

# --- Data Loading ---
CROP_ALIASES = {
    "arhar": "PigeonPea", "tur": "PigeonPea", "moong": "GreenGram", 
    "mung": "GreenGram", "urad": "BlackGram", "masoor": "Lentil",
    "chana": "Chickpea", "gram": "Chickpea", "millet": "Bajra", 
    "sorghum": "Jowar", "sarson": "Mustard"
}

@st.cache_resource
def load_all():
    try:
        db = pd.read_csv('processed_nutrients.csv')
        weather = pd.read_csv('forecasting_data.csv')
        dir_file = 'Indian Agriculture Agency Directory - Indian Agriculture Agency Directory.csv'
        agency_db = pd.read_csv(dir_file)
        msp_db = pd.read_csv('msp.csv')
        for df in [db, weather, agency_db]:
            df.columns = df.columns.str.strip()
            state_col = [c for c in df.columns if 'state' in c.lower()][0]
            df.rename(columns={state_col: 'State'}, inplace=True)
            df['State'] = df['State'].astype(str).str.strip().str.upper()
        msp_db.columns = msp_db.columns.str.strip()
        with open('crop_requirements.json', 'r') as f: reqs = json.load(f)
        with open('cultivation_details.json', 'r') as f: cult = json.load(f)
        with open('lang_pack.json', 'r', encoding='utf-8') as f: lp = json.load(f)
        return db, reqs, weather, cult, lp, agency_db, msp_db
    except Exception as e:
        st.error(f"Error loading files: {e}")
        return None, None, None, None, None, None, None

db, crop_reqs, weather_db, cult_info, lang_pack, agency_db, msp_db = load_all()

if db is not None:
    languages = {"English": "en", "Hindi": "hi", "Marathi": "mr", "Tamil": "ta", "Telugu": "te"}
    
    with st.sidebar:
        st.title("🍀 AgriVision Pro")
        l_choice = st.selectbox("🌐 Language", list(languages.keys()))
        t_code = languages[l_choice]
        def tr(text): return lang_pack.get(t_code, {}).get(text, text) if t_code != 'en' else text
        def live_tr(text, target):
            if target == 'en': return text
            try: return GoogleTranslator(source='auto', target=target).translate(str(text))
            except: return text
        states = sorted(list(set(db['State'].unique()) & set(weather_db['State'].unique())))
        sel_state = st.selectbox(f"📍 {tr('Select State')}", states)

    st.markdown(f'<h1>🌾 {tr("AgriVision-AV")}</h1>', unsafe_allow_html=True)
    
    nut_row = db[db['State'] == sel_state].iloc[0]
    w_row = weather_db[weather_db['State'] == sel_state].iloc[0]
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    all_crops = list(crop_reqs.keys())
    tr_crops = [tr(c) for c in all_crops]
    sel_crop_tr = st.selectbox(tr("Select Crop"), tr_crops)
    sel_crop = all_crops[tr_crops.index(sel_crop_tr)]
    req = crop_reqs[sel_crop]

    # Season Temp Logic
    months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    found_m = [m for m in months_list if m.lower() in req['months'].lower()]
    avg_temp_val = pd.to_numeric(w_row[found_m or ['June']]).mean()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: n_in = st.number_input(f"{tr('Nitrogen')} (kg/ha)", value=float(nut_row['Nitrogen']))
    with c2: p_in = st.number_input(f"{tr('Phosphorus')} (kg/ha)", value=float(nut_row['Phosphorus']))
    with c3: k_in = st.number_input(f"{tr('Potassium')} (kg/ha)", value=float(nut_row['Potassium']))
    with c4: t_in = st.number_input(f"{tr('Avg Temp')} (°C)", value=float(avg_temp_val))
    with c5: r_in = st.number_input(f"{tr('Rainfall')} (mm)", value=float(w_row.get('Average annual rainfall (mm)', 1000)))
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button(f"🚀 {tr('Predict & Show Advice')}"):
        st.session_state.clicked = True
        
        # Scoring Logic
        score = 100
        if t_in < req['t_min'] or t_in > req['t_max']: score -= 20
        if r_in < req['r_min']: score -= 20
        n_p = min(1.0, n_in/req['n']) if req['n'] > 0 else 1.0
        p_p = min(1.0, p_in/req['p']) if req['p'] > 0 else 1.0
        k_p = min(1.0, k_in/req['k']) if req['k'] > 0 else 1.0
        score -= ((1-n_p)*30 + (1-p_p)*15 + (1-k_p)*15)
        st.session_state.score = max(5, int(score)) 
        
        yield_val = (st.session_state.score / 100) * 9.0
        st.session_state.yield_val = yield_val
        
        # MSP Logic
        clean_sel = re.sub(r'\(.*?\)', '', sel_crop).strip().lower()
        search_term = CROP_ALIASES.get(clean_sel, clean_sel)
        msp_row = msp_db[msp_db['Crop'].str.lower().str.contains(search_term)]
        
        if not msp_row.empty:
            st.session_state.earnings = yield_val * 10 * msp_row.iloc[0]['MSP_INR_per_Quintal']
            st.session_state.msp_available = True
        else:
            st.session_state.msp_available = False
            st.session_state.earnings = 0

        audio_text = f"Suitability is {st.session_state.score} percent. Yield is {yield_val:.2f} tons per hectare."
        try:
            tts = gTTS(text=live_tr(audio_text, t_code), lang=t_code)
            tts.save("v.mp3")
            st.session_state.audio_ready = True
        except: st.session_state.audio_ready = False

    if st.session_state.get('clicked'):
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        r_c1, r_c2, r_c3 = st.columns(3)
        r_c1.metric(tr("Suitability"), f"{st.session_state.score}%")
        r_c2.metric(tr("Yield Estimate"), f"{st.session_state.yield_val:.2f} T/Ha")
        if st.session_state.get('msp_available'):
            r_c3.metric(f"{tr('Potential Earnings')} (per Hectare)", f"₹{int(st.session_state.earnings):,}")
        else: r_c3.metric(tr("Potential Earnings"), "N/A")
        st.markdown('</div>', unsafe_allow_html=True)

        tab1, tab2, tab3, tab4 = st.tabs([tr("Action Plan"), tr("Soil Health"), tr("Audio"), tr("Agency Directory")])

        with tab1:
            plan = next((v for k, v in cult_info.items() if k.lower() in sel_crop.lower()), "N/A")
            st.info(live_tr(plan, t_code))

        with tab2:
            st.markdown(f"### 🧪 {tr('Detailed NPK Gap Analysis')}")
            s_c1, s_c2, s_c3 = st.columns(3)
            s_c1.metric(f"{tr('Nitrogen')} (N)", f"{int(n_in)} kg/ha", delta=f"{int(n_in - req['n'])} gap", delta_color="normal")
            s_c2.metric(f"{tr('Phosphorus')} (P)", f"{int(p_in)} kg/ha", delta=f"{int(p_in - req['p'])} gap", delta_color="normal")
            s_c3.metric(f"{tr('Potassium')} (K)", f"{int(k_in)} kg/ha", delta=f"{int(k_in - req['k'])} gap", delta_color="normal")
            
            st.markdown("---")
            st.write(f"📊 **{tr('Requirement for')} {sel_crop}:**")
            st.write(f"Target N: `{req['n']} kg/ha` | Target P: `{req['p']} kg/ha` | Target K: `{req['k']} kg/ha`")
            st.progress(st.session_state.score / 100)
            st.caption(tr("Overall Soil Suitability Progress"))

        with tab3:
            if st.session_state.get('audio_ready'): st.audio("v.mp3")
        with tab4:
            st.dataframe(agency_db[agency_db['State'] == sel_state], use_container_width=True)
