import streamlit as st
import pandas as pd
import base64
from pathlib import Path

# ── CONFIGURACIÓ ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Milanta · Simulador de Pressupost",
    page_icon="🌿",
    layout="centered"
)

# ── CARREGA LOGO ──────────────────────────────────────────────────────────────
def get_logo_base64():
    logo_path = Path("assets/1.Milanta.jpg")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_base64 = get_logo_base64()
logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Milanta Logo">' if logo_base64 else ""

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
        background-color: #F7F4EF !important;
        color: #3A3228 !important;
    }
    .main, .block-container {
        background-color: #F7F4EF !important;
        padding-top: 0 !important;
    }

    .header {
        text-align: center;
        padding: 1.5rem 0 2rem 0;
        border-bottom: 1px solid #D6CFC4;
        margin-bottom: 2rem;
    }
    .logo-container {
        margin-bottom: 1rem;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .logo-container img {
        max-height: 60px;
        max-width: 80px;
        object-fit: contain;
    }
    .header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        color: #2D5A1B;
        letter-spacing: -0.5px;
        margin-bottom: 0.4rem;
        margin-top: 0;
    }
    .header p {
        font-size: 0.85rem;
        color: #9A9288;
        font-weight: 300;
        margin: 0;
        font-style: italic;
    }

    .sec-title {
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        color: #9A9288;
        margin-bottom: 1rem;
        margin-top: 2rem;
    }

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #D6CFC4 !important;
        border-radius: 10px !important;
        color: #3A3228 !important;
    }
    div[data-baseweb="select"] > div:focus-within {
        border-color: #4A7C2F !important;
        box-shadow: 0 0 0 2px rgba(74,124,47,0.12) !important;
    }
    div[data-testid="stNumberInput"] input {
        background-color: #FFFFFF !important;
        border: 1px solid #D6CFC4 !important;
        border-radius: 10px !important;
        color: #3A3228 !important;
    }
    label {
        font-size: 0.85rem !important;
        color: #5A5248 !important;
        font-weight: 400 !important;
    }

    .stButton > button {
        width: 100%;
        background-color: #2D5A1B !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.85rem 1rem !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        font-family: 'Poppins', sans-serif !important;
        margin-top: 1.5rem;
        transition: all 0.2s ease;
        letter-spacing: 0.1px;
    }
    .stButton > button:hover {
        background-color: #3D7A25 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(45,90,27,0.2) !important;
    }

    .cards-wrap {
        display: grid;
        grid-template-columns: 1fr 1.15fr 1fr;
        gap: 12px;
        margin-top: 1.5rem;
    }
    .card {
        background: #FFFFFF;
        border: 1px solid #D6CFC4;
        border-radius: 16px;
        padding: 1.5rem 1.2rem;
        text-align: center;
    }
    .card-mid {
        background: #F0F5EC;
        border: 1.5px solid #B8D4A8;
        border-radius: 16px;
        padding: 1.5rem 1.2rem;
        text-align: center;
    }
    .card-label {
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #9A9288;
        margin-bottom: 0.6rem;
    }
    .card-mid .card-label { color: #5A8A45; }
    .card-value {
        font-size: 1.7rem;
        font-weight: 600;
        color: #2D5A1B;
        line-height: 1.1;
        margin-bottom: 0.3rem;
    }
    .card-mid .card-value { font-size: 2rem; }
    .card-sub {
        font-size: 0.75rem;
        color: #9A9288;
    }

    .badge {
        display: inline-block;
        background: #EAF2E5;
        color: #4A7C2F;
        border-radius: 20px;
        padding: 0.25rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 1.2rem;
        text-align: center;
    }

    .warning {
        background: #FDF6E3;
        border: 1px solid #E8D5A0;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.82rem;
        color: #7A6520;
        margin-top: 1rem;
    }

    .stExpander {
        background: #FFFFFF !important;
        border: 1px solid #D6CFC4 !important;
        border-radius: 12px !important;
        margin-top: 1rem;
    }
    .stExpander summary {
        font-size: 0.85rem !important;
        color: #5A5248 !important;
    }
    .detail-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.875rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid #EDE8E1;
        color: #5A5248;
    }
    .detail-row:last-child { border-bottom: none; }
    .detail-total {
        font-weight: 600;
        color: #2D5A1B;
    }

    .footer {
        text-align: center;
        font-size: 0.75rem;
        color: #B0A89F;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #D6CFC4;
        font-style: italic;
    }

    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── CAPÇALERA ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="header">
    <div class="logo-container">
        {logo_html}
    </div>
    <h1>Simulador de Pressupost Orientatiu</h1>
    <p>Renaturalització de patis escolars · milanta.net</p>
</div>
""", unsafe_allow_html=True)

# ── DADES ─────────────────────────────────────────────────────────────────────
@st.cache_data
def carregar_dades():
    df = pd.read_excel("DADES GENERALS.xlsx")
    df.columns = df.columns.str.strip()
    return df

df = carregar_dades()

# ── MOTOR DE CÀLCUL NOU ──────────────────────────────────────────────────────
BASE_TIPOLOGIA = {
    "combinat": 202.73,
    "espai trobada": 276.44,
    "moviment": 289.30,
    "sorral": 233.05
}

IMPACTE_REPICAT = {
    "combinat": 0.0983,
    "espai trobada": 0.1010,
    "moviment": 0.0810,
    "sorral": 0.0643
}

FACTOR_COMPLEXITAT = {
    "baixa": 0.95,
    "mitja": 1.00,
    "alta": 1.15
}

def calcular_preu(tipologia, m2, repicat, maquina, complexitat, accessibilitat):
    base = BASE_TIPOLOGIA[tipologia]
    factor_repicat = 1 + IMPACTE_REPICAT[tipologia] if repicat != "no" else 1
    factor_maquina = 1.00 if maquina == "si" else 0.95
    factor_complexitat = FACTOR_COMPLEXITAT[complexitat]
    factor_acc = {"bona": 1.00, "limitada": 1.15, "molt limitada": 1.30}[accessibilitat]

    preu_m2 = base * factor_repicat * factor_maquina * factor_complexitat * factor_acc
    total = preu_m2 * m2

    return (
        round(preu_m2, 2),
        round(total * 0.85, 2),
        round(total, 2),
        round(total * 1.15, 2)
    )

# ── FORMULARI ─────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-title">Dades del projecte</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    m2             = st.number_input("Superfície (m²)", min_value=10, max_value=2000, value=150, step=10)
    complexitat    = st.selectbox("Complexitat", ["baixa", "mitja", "alta"])
    accessibilitat = st.selectbox("Accessibilitat", ["bona", "limitada", "molt limitada"])
with col2:
    tipologia = st.selectbox("Tipologia", ["combinat", "espai trobada", "moviment", "sorral"])
    maquina   = st.selectbox("Màquina necessària", ["no", "si"])
    repicat   = st.selectbox("Repicat", ["no", "parcial", "total"])

calcular = st.button("Calcular pressupost orientatiu")

# ── CÀLCUL ────────────────────────────────────────────────────────────────────
if calcular:
    preu_m2, total_baix, total_mig, total_alt = calcular_preu(
        tipologia=tipologia,
        m2=m2,
        repicat=repicat,
        maquina=maquina,
        complexitat=complexitat,
        accessibilitat=accessibilitat
    )

    st.markdown('<div class="sec-title">Pressupost orientatiu</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="cards-wrap">
        <div class="card">
            <div class="card-label">Estimació baixa</div>
            <div class="card-value">{total_baix:,.0f} €</div>
            <div class="card-sub">{round(total_baix/m2)} €/m²</div>
        </div>
        <div class="card-mid">
            <div class="card-label">Estimació mitjana</div>
            <div class="card-value">{total_mig:,.0f} €</div>
            <div class="card-sub">{preu_m2} €/m² · {m2} m²</div>
        </div>
        <div class="card">
            <div class="card-label">Estimació alta</div>
            <div class="card-value">{total_alt:,.0f} €</div>
            <div class="card-sub">{round(total_alt/m2)} €/m²</div>
        </div>
    </div>
    <div style="text-align:center">
        <span class="badge">📊 Basat en dades històriques de projectes reals</span>
    </div>
    """, unsafe_allow_html=True)

    m2_min = int(df['m²'].min())
    m2_max = int(df['m²'].max())
    if m2 < m2_min or m2 > m2_max:
        st.markdown(f"""
        <div class="warning">
            ⚠️ La superfície introduïda ({m2} m²) està fora del rang habitual dels projectes
            de la base de dades ({m2_min}–{m2_max} m²). L'estimació pot ser menys precisa.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Veure detall del càlcul"):
        st.markdown(f"""
        <div class="detail-row">
            <span>Preu unitari final</span>
            <span>{preu_m2} €/m²</span>
        </div>
        <div class="detail-row">
            <span>Superfície</span>
            <span>{m2} m²</span>
        </div>
        <div class="detail-row detail-total">
            <span>Total estimació mitjana</span>
            <span>{total_mig:,.0f} €</span>
        </div>
        """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Pressupost orientatiu basat en projectes reals ·
    Com més projectes s'introdueixin a la base de dades, més fiable serà l'estimació
</div>
""", unsafe_allow_html=True)