"""
EduPrepPro — EAMCET & JEE Mains Preparation Platform
Complete Streamlit Application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import os

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduPrepPro – EAMCET & JEE Mains",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* hero */
.hero-header {
    background: linear-gradient(135deg,#1a1a2e 0%,#16213e 35%,#0f3460 65%,#533483 100%);
    padding:48px 32px; border-radius:20px; text-align:center; margin-bottom:28px;
    position:relative; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.4);
}
.hero-header::before {
    content:''; position:absolute; width:200%; height:200%; top:-50%; left:-50%;
    background:radial-gradient(circle,rgba(83,52,131,.3) 0%,transparent 60%),
               radial-gradient(circle at 80% 20%,rgba(15,52,96,.4) 0%,transparent 50%);
    animation:rotateBg 12s linear infinite;
}
@keyframes rotateBg{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
.hero-title  { font-size:3rem; font-weight:800; color:#fff; position:relative; text-shadow:0 2px 20px rgba(0,0,0,.5); margin:0 0 8px; }
.hero-subtitle { font-size:1.2rem; color:rgba(255,255,255,.8); position:relative; margin:0; }

/* cards */
.metric-card {
    background:linear-gradient(135deg,#1e1e2e,#2a2a3e);
    border:1px solid rgba(255,255,255,.08); border-radius:16px; padding:24px;
    text-align:center; transition:transform .2s,box-shadow .2s;
    box-shadow:0 4px 24px rgba(0,0,0,.3);
}
.metric-card:hover{transform:translateY(-4px);box-shadow:0 8px 32px rgba(0,0,0,.4);}
.metric-value{font-size:2.4rem;font-weight:700;margin:0;}
.metric-label{font-size:.85rem;color:rgba(255,255,255,.6);margin:4px 0 0;}

.subject-card {
    background:linear-gradient(135deg,#1e1e2e,#16213e); border-radius:16px;
    padding:24px; border-left:4px solid; margin-bottom:16px;
    box-shadow:0 4px 20px rgba(0,0,0,.3); transition:transform .2s;
}
.subject-card:hover{transform:translateX(4px);}

.question-card {
    background:linear-gradient(135deg,#1a1a2e,#2d2d44); border-radius:16px;
    padding:28px; margin-bottom:20px; border:1px solid rgba(255,255,255,.07);
    box-shadow:0 6px 24px rgba(0,0,0,.35);
}

/* leaderboard */
.rank-1{background:linear-gradient(90deg,rgba(255,215,0,.15),rgba(255,215,0,.05));border-left:4px solid #ffd700;}
.rank-2{background:linear-gradient(90deg,rgba(192,192,192,.15),rgba(192,192,192,.05));border-left:4px solid #c0c0c0;}
.rank-3{background:linear-gradient(90deg,rgba(205,127,50,.15),rgba(205,127,50,.05));border-left:4px solid #cd7f32;}
.leaderboard-row{
    border-radius:12px; padding:16px 20px; margin-bottom:10px;
    border:1px solid rgba(255,255,255,.06);
}

/* sidebar */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f0f1a 0%,#1a1a2e 100%);}
[data-testid="stSidebar"] .stRadio label{color:rgba(255,255,255,.85)!important;font-size:.95rem;padding:6px 0;}

/* buttons */
.stButton>button{border-radius:10px;font-weight:600;transition:all .2s;border:none;}
.stButton>button:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.3);}

/* badges */
.badge{display:inline-block;padding:4px 12px;border-radius:20px;font-size:.75rem;font-weight:600;margin:2px;}
.badge-physics{background:rgba(100,149,237,.25);color:#6495ed;border:1px solid rgba(100,149,237,.4);}
.badge-chemistry{background:rgba(50,205,50,.2);color:#32cd32;border:1px solid rgba(50,205,50,.3);}
.badge-math{background:rgba(255,165,0,.2);color:#ffa500;border:1px solid rgba(255,165,0,.3);}
.badge-easy{background:rgba(0,255,127,.15);color:#00ff7f;}
.badge-medium{background:rgba(255,215,0,.15);color:#ffd700;}
.badge-hard{background:rgba(255,69,0,.15);color:#ff4500;}

/* info boxes */
.info-box{background:rgba(100,149,237,.1);border:1px solid rgba(100,149,237,.3);border-radius:12px;padding:16px 20px;margin:12px 0;}
.success-box{background:rgba(50,205,50,.1);border:1px solid rgba(50,205,50,.3);border-radius:12px;padding:16px 20px;margin:12px 0;}
.error-box{background:rgba(255,69,0,.1);border:1px solid rgba(255,69,0,.3);border-radius:12px;padding:16px 20px;margin:12px 0;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  PATHS
# ─────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# ─────────────────────────────────────────────────────────────
#  DATA HELPERS
# ─────────────────────────────────────────────────────────────
def load_csv(filename: str) -> pd.DataFrame:
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        try:
            return pd.read_csv(path)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

def save_csv(df: pd.DataFrame, filename: str):
    path = os.path.join(DATA_DIR, filename)
    df.to_csv(path, index=False)

def verify_login(username: str, password: str):
    df = load_csv("students.csv")
    if df.empty:
        return None
    row = df[df["username"] == username]
    if row.empty:
        return None
    if str(row.iloc[0]["password"]) == password:
        return row.iloc[0].to_dict()
    return None

def get_student_results(username: str) -> pd.DataFrame:
    df = load_csv("results.csv")
    if df.empty:
        return pd.DataFrame()
    return df[df["username"] == username].copy()

def get_questions(subject=None, chapter=None) -> pd.DataFrame:
    df = load_csv("questions.csv")
    if df.empty:
        return pd.DataFrame()
    if subject and subject != "All":
        df = df[df["subject"] == subject]
    if chapter and chapter != "All":
        df = df[df["chapter"] == chapter]
    return df.copy()

def save_result(username, subject, chapter, score, total, correct, incorrect, unattempted, time_taken, test_type):
    df = load_csv("results.csv")
    new_row = pd.DataFrame([{
        "username": username, "test_date": datetime.now().strftime("%Y-%m-%d"),
        "subject": subject, "chapter": chapter, "score": score,
        "total_questions": total, "correct": correct, "incorrect": incorrect,
        "unattempted": unattempted, "time_taken": time_taken, "test_type": test_type,
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    save_csv(df, "results.csv")

def save_mistake(username, question_id, subject, chapter, student_ans, correct_ans):
    df = load_csv("mistakes.csv")
    if not df.empty:
        mask = (df["username"] == username) & (df["question_id"].astype(int) == int(question_id))
        if mask.any():
            return  # already recorded
    new_row = pd.DataFrame([{
        "username": username, "question_id": int(question_id),
        "subject": subject, "chapter": chapter,
        "date_attempted": datetime.now().strftime("%Y-%m-%d"),
        "student_answer": student_ans, "correct_answer": correct_ans, "bookmarked": False,
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    save_csv(df, "mistakes.csv")

def subject_badge(subject):
    mapping = {"Physics": "badge-physics", "Chemistry": "badge-chemistry", "Mathematics": "badge-math"}
    return mapping.get(subject, "badge-physics")

def subject_color(subject):
    mapping = {"Physics": "#6495ed", "Chemistry": "#32cd32", "Mathematics": "#ffa500"}
    return mapping.get(subject, "#6495ed")

# ─────────────────────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────────────────────
_DEFAULTS = {
    "logged_in": False,
    "user": None,
    "page": "Home",
    # test state
    "test_active": False,
    "test_questions": [],
    "test_answers": {},
    "test_start_time": None,
    "test_end_time": None,
    "test_submitted": False,
    "test_config": {"subject": "All", "chapter": "All", "duration": 1200, "neg_marking": True},
    # daily practice
    "daily_submitted": False,
    "daily_questions": [],
    "daily_answers": {},
    # chatbot
    "chatbot_history": [],
    # challenge
    "active_challenge": None,
    "ch_questions": [],
    "ch_answers": {},
    "ch_submitted": False,
    "ch_start_time": None,
    "ch_end_time": None,
    # take test: once-per-session flag
    "test_completed": False,
}

for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─────────────────────────────────────────────────────────────
#  STUDY MATERIALS DATA
# ─────────────────────────────────────────────────────────────
MATERIALS = {
    "Physics": {
        "Mechanics": {
            "theory": """
### 🔵 Mechanics

**Newton's Laws of Motion**
- **First Law (Inertia):** A body stays at rest or uniform motion unless acted upon by a net external force.
- **Second Law:** **F = ma** — Net force = mass × acceleration.
- **Third Law:** Every action has an equal and opposite reaction.

**Kinematics Equations** *(uniform acceleration)*
| Equation | Variables |
|---|---|
| v = u + at | v, u, a, t |
| s = ut + ½at² | s, u, a, t |
| v² = u² + 2as | v, u, a, s |

**Projectile Motion**
- Horizontal range: **R = u²sin2θ / g** → maximum at **θ = 45°**
- Maximum height: **H = u²sin²θ / 2g**
- Time of flight: **T = 2u sinθ / g**

**Work, Energy & Power**
- Work: W = Fd cosθ
- Kinetic Energy: KE = ½mv²
- Potential Energy: PE = mgh
- Conservation of Energy: KE + PE = constant (no friction)
""",
            "questions": [
                {"q": "A body is projected at 45° with speed 20 m/s. Find range. (g = 10 m/s²)", "a": "40 m", "exp": "R = u²sin90°/g = 400/10 = 40 m"},
                {"q": "Calculate KE of 2 kg body moving at 3 m/s.", "a": "9 J", "exp": "KE = ½ × 2 × 3² = 9 J"},
                {"q": "A 10 N force moves a body 5 m at 60°. Find work done.", "a": "25 J", "exp": "W = 10 × 5 × cos60° = 50 × 0.5 = 25 J"},
            ],
        },
        "Thermodynamics": {
            "theory": """
### 🔴 Thermodynamics

**Laws of Thermodynamics**
- **Zeroth Law:** Thermal equilibrium is transitive.
- **First Law:** ΔU = Q − W  *(energy conservation)*
- **Second Law:** Entropy of the universe always increases.
- **Third Law:** Entropy → 0 as T → 0 K.

**Thermodynamic Processes**
| Process | Condition | Work |
|---|---|---|
| Isothermal | T = const | nRT ln(V₂/V₁) |
| Adiabatic | Q = 0 | (P₁V₁ − P₂V₂)/(γ−1) |
| Isobaric | P = const | PΔV |
| Isochoric | V = const | 0 |

**Carnot Efficiency:** η = 1 − T_cold / T_hot
""",
            "questions": [
                {"q": "Work done in isochoric process?", "a": "Zero", "exp": "W = PΔV = 0 because ΔV = 0"},
                {"q": "Efficiency of Carnot engine between 500 K and 300 K?", "a": "40%", "exp": "η = 1 − 300/500 = 0.4 = 40%"},
            ],
        },
        "Optics": {
            "theory": """
### 🟡 Optics

**Lens Formula:** 1/f = 1/v − 1/u

**Mirror Formula:** 1/f = 1/v + 1/u

**Snell's Law:** n₁ sinθ₁ = n₂ sinθ₂

**Total Internal Reflection** occurs when θ > θ_critical where sin θ_c = 1/n

**Magnification:**
- Lens: m = v/u = h'/h
- Mirror: m = −v/u

**Key Sign Convention (New Cartesian):** Distances measured from pole; incident light travels left to right.
""",
            "questions": [
                {"q": "Object at 30 cm from convex lens of f = 20 cm. Find image distance.", "a": "60 cm", "exp": "1/v − 1/(-30) = 1/20 → 1/v = 1/20 − 1/30 = 1/60 → v = 60 cm"},
                {"q": "Refractive index of glass is 1.5. Find critical angle.", "a": "~41.8°", "exp": "sin C = 1/1.5 = 0.667, C = arcsin(0.667) ≈ 41.8°"},
            ],
        },
    },
    "Chemistry": {
        "Atomic Structure": {
            "theory": """
### 🟢 Atomic Structure

**Bohr's Model**
- Electrons revolve in fixed orbits without radiating energy.
- Energy: **E_n = −13.6 / n²  eV**
- Radius: r_n = 0.529 × n²  Å (for hydrogen)
- Angular momentum: mvr = nh/2π

**Quantum Numbers**
| Symbol | Name | Values |
|---|---|---|
| n | Principal | 1, 2, 3 … |
| l | Azimuthal | 0 to n−1 |
| m | Magnetic | −l to +l |
| s | Spin | ±½ |

**Electronic Configuration Rules**
1. **Aufbau Principle:** Fill lowest energy first.
2. **Pauli Exclusion:** No two electrons have all four quantum numbers identical.
3. **Hund's Rule:** Fill degenerate orbitals singly before pairing.
""",
            "questions": [
                {"q": "Energy of electron in 2nd orbit of hydrogen?", "a": "−3.4 eV", "exp": "E = −13.6/n² = −13.6/4 = −3.4 eV"},
                {"q": "Total orbitals in n = 3 shell?", "a": "9", "exp": "Total orbitals = n² = 9"},
            ],
        },
        "Organic Chemistry": {
            "theory": """
### 🟡 Organic Chemistry

**Hybridization**
| Type | Shape | Angle | Example |
|---|---|---|---|
| sp³ | Tetrahedral | 109.5° | CH₄ |
| sp² | Trigonal planar | 120° | C₂H₄ |
| sp | Linear | 180° | C₂H₂ |

**IUPAC Rules (summary)**
1. Find the longest carbon chain → parent chain.
2. Number from the end nearer to the first substituent.
3. Name substituents as prefixes (methyl, ethyl …).
4. Add suffix based on functional group.

**Functional Group Suffixes**
| Group | Suffix |
|---|---|
| −OH | −ol |
| −CHO | −al |
| −COOH | −oic acid |
| −CO− | −one |
""",
            "questions": [
                {"q": "IUPAC name of CH₃COCH₃?", "a": "Propan-2-one", "exp": "Ketone with 3 carbons; keto at C2 → propan-2-one"},
                {"q": "Hybridization of carbon in ethylene?", "a": "sp²", "exp": "C=C double bond: σ + π; each C uses sp² hybrid orbitals"},
            ],
        },
        "Electrochemistry": {
            "theory": """
### ⚡ Electrochemistry

**Key Definitions**
- **Electrolyte:** Substance that conducts electricity in solution.
- **Electrode potential:** Tendency of electrode to gain/lose electrons.
- **EMF of cell:** E_cell = E_cathode − E_anode

**Nernst Equation:**
E = E° − (RT/nF) ln Q  ≈  E° − (0.0592/n) log Q  at 25°C

**Faraday's Laws**
1. Mass deposited ∝ charge passed: m = (M/nF) × Q
2. For same charge, masses deposited ∝ equivalent weights.

**Standard Reduction Potentials (25°C)**
- SHE (H₂/H⁺): 0.00 V  *(reference)*
- Cu²⁺/Cu: +0.34 V
- Zn²⁺/Zn: −0.76 V
- F₂/F⁻: +2.87 V *(strongest oxidising agent)*
""",
            "questions": [
                {"q": "EMF of Daniell cell (Zn-Cu)?", "a": "1.10 V", "exp": "E = E_Cu − E_Zn = 0.34 − (−0.76) = 1.10 V"},
                {"q": "Mass of Cu deposited by 2 F of charge (M=64)?", "a": "64 g", "exp": "m = (64/2) × 2 = 64 g"},
            ],
        },
    },
    "Mathematics": {
        "Calculus": {
            "theory": """
### 🟠 Calculus

**Differentiation Formulas**
| Function | Derivative |
|---|---|
| xⁿ | nxⁿ⁻¹ |
| eˣ | eˣ |
| ln x | 1/x |
| sin x | cos x |
| cos x | −sin x |
| tan x | sec²x |

**Key Rules**
- **Chain Rule:** d/dx[f(g(x))] = f′(g(x)) · g′(x)
- **Product Rule:** d/dx[uv] = u′v + uv′
- **Quotient Rule:** d/dx[u/v] = (u′v − uv′)/v²

**Integration Formulas**
| Integral | Result |
|---|---|
| ∫xⁿ dx | xⁿ⁺¹/(n+1) + C |
| ∫eˣ dx | eˣ + C |
| ∫sin x dx | −cos x + C |
| ∫cos x dx | sin x + C |
| ∫1/x dx | ln|x| + C |
""",
            "questions": [
                {"q": "Find dy/dx if y = x³ + 2x² − 5.", "a": "3x² + 4x", "exp": "Differentiate term by term: 3x² + 4x + 0"},
                {"q": "Evaluate ∫(2x + 3)dx.", "a": "x² + 3x + C", "exp": "∫2x dx + ∫3 dx = x² + 3x + C"},
            ],
        },
        "Algebra": {
            "theory": """
### 🟣 Algebra

**Quadratic Equations** ax² + bx + c = 0
- Roots: x = (−b ± √(b²−4ac)) / 2a
- Discriminant D = b²−4ac:  D>0 real distinct | D=0 equal | D<0 complex
- Sum of roots: α+β = −b/a  |  Product: αβ = c/a

**Arithmetic Progression (AP)**
- General term: aₙ = a + (n−1)d
- Sum of n terms: Sₙ = n/2 · [2a + (n−1)d]

**Geometric Progression (GP)**
- General term: aₙ = arⁿ⁻¹
- Sum of n terms: Sₙ = a(rⁿ−1)/(r−1) for r ≠ 1
- Sum to infinity (|r|<1): S∞ = a/(1−r)

**Logarithm Laws**
- log(mn) = log m + log n
- log(m/n) = log m − log n
- log mⁿ = n log m
- log_b x = log x / log b  *(change of base)*
""",
            "questions": [
                {"q": "Sum of first 10 natural numbers.", "a": "55", "exp": "S = n(n+1)/2 = 10×11/2 = 55"},
                {"q": "If α,β are roots of x²−5x+6=0, find α²+β².", "a": "13", "exp": "α+β=5, αβ=6, α²+β²=(α+β)²−2αβ = 25−12 = 13"},
            ],
        },
        "Trigonometry": {
            "theory": """
### 🔵 Trigonometry

**Fundamental Identities**
- sin²θ + cos²θ = 1
- 1 + tan²θ = sec²θ
- 1 + cot²θ = cosec²θ

**Important Values**
| Angle | sin | cos | tan |
|---|---|---|---|
| 0° | 0 | 1 | 0 |
| 30° | ½ | √3/2 | 1/√3 |
| 45° | 1/√2 | 1/√2 | 1 |
| 60° | √3/2 | ½ | √3 |
| 90° | 1 | 0 | ∞ |

**Addition Formulas**
- sin(A±B) = sinA cosB ± cosA sinB
- cos(A±B) = cosA cosB ∓ sinA sinB
- tan(A+B) = (tanA + tanB)/(1 − tanA tanB)

**Double Angle**
- sin2A = 2 sinA cosA
- cos2A = cos²A − sin²A = 1−2sin²A = 2cos²A−1
""",
            "questions": [
                {"q": "Value of sin 30° + cos 60°?", "a": "1", "exp": "sin 30° = 0.5, cos 60° = 0.5, sum = 1"},
                {"q": "Prove: sin²45° + cos²45° = 1.", "a": "1", "exp": "(1/√2)² + (1/√2)² = 0.5 + 0.5 = 1 ✓"},
            ],
        },
    },
}

# ─────────────────────────────────────────────────────────────
#  LOGIN PAGE
# ─────────────────────────────────────────────────────────────
def render_login():
    st.markdown("""
    <div class="hero-header">
        <p class="hero-title">🎓 EduPrepPro</p>
        <p class="hero-subtitle">Your Ultimate Preparation Platform for EAMCET &amp; JEE Mains</p>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("### 🔐 Login to Your Account")
        st.markdown("---")
        username = st.text_input("👤 Username", placeholder="Enter username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
        login_btn = st.button("🚀 Login", use_container_width=True, type="primary")

        if login_btn:
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                user = verify_login(username.strip(), password.strip())
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.page = "Home"
                    st.success(f"✅ Welcome, {user['name']}!")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

        st.markdown("---")
        st.markdown("""
        <div style='text-align:center;color:rgba(255,255,255,.5);font-size:.8rem;'>
        Demo — Student: <b>ravi_kumar / pass123</b> &nbsp;|&nbsp; Admin: <b>admin / admin123</b>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────
def render_sidebar():
    user = st.session_state.user
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center;padding:20px 0 10px;'>
            <div style='font-size:3rem;'>{"👑" if user["role"]=="admin" else "🎓"}</div>
            <div style='font-weight:700;font-size:1.1rem;color:white;'>{user["name"]}</div>
            <div style='font-size:.8rem;color:rgba(255,255,255,.5);'>{user["role"].title()}</div>
        </div>
        <hr style='border-color:rgba(255,255,255,.1);'>
        """, unsafe_allow_html=True)

        pages = [
            "🏠 Home", "📊 Dashboard", "📚 Materials",
            "✏️ Daily Practice", "📝 Take Test",
            "⚔️ Challenges", "🏆 Leaderboard", "📖 Mistake Notebook",
        ]
        if user["role"] == "admin":
            pages.append("⚙️ Admin Panel")

        # find current index
        current = st.session_state.page
        idx = 0
        for i, p in enumerate(pages):
            label = " ".join(p.split()[1:])
            if label == current:
                idx = i
                break

        choice = st.radio("Navigation", pages, index=idx, key="nav_radio")
        # strip leading emoji word
        parts = choice.split()
        st.session_state.page = " ".join(parts[1:]) if len(parts) > 1 else choice

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

# ─────────────────────────────────────────────────────────────
#  PAGE: HOME
# ─────────────────────────────────────────────────────────────
def page_home():
    user = st.session_state.user
    st.markdown(f"""
    <div class="hero-header">
        <p class="hero-title">🎓 EduPrepPro</p>
        <p class="hero-subtitle">Welcome back, <strong>{user['name']}</strong>! Ready to ace EAMCET &amp; JEE Mains?</p>
    </div>
    """, unsafe_allow_html=True)

    features = [
        ("⚡", "Smart Practice", "Daily", "10 daily questions tailored to your weak areas", "#6495ed"),
        ("🧪", "Deep Materials", "Theory", "Comprehensive notes with solved examples", "#32cd32"),
        ("📐", "Math Mastery", "Concepts", "Step-by-step solutions with visual aids", "#ffa500"),
        ("🏆", "Live Challenges", "Compete", "Real-time timed competitions with peers", "#ff6b6b"),
        ("📊", "Analytics", "Track", "Performance insights and progress graphs", "#9b59b6"),
        ("🎯", "Mock Tests", "Simulate", "Full exam simulation with negative marking", "#1abc9c"),
    ]
    cols = st.columns(3)
    for i, (icon, title, tag, desc, color) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="metric-card" style="border-top:3px solid {color};margin-bottom:16px;">
                <div style="font-size:2.5rem;">{icon}</div>
                <div style="font-weight:700;font-size:1.1rem;color:white;margin:8px 0 4px;">{title}</div>
                <div class="badge" style="background:rgba(255,255,255,.1);color:{color};border:1px solid {color}55;">{tag}</div>
                <div style="font-size:.85rem;color:rgba(255,255,255,.6);margin-top:8px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="info-box">
        <h4 style="color:#6495ed;margin-top:0;">📋 About EAMCET</h4>
        <ul style="color:rgba(255,255,255,.8);margin:0;padding-left:20px;">
        <li>Engineering Agriculture Medical Common Entrance Test</li>
        <li>Conducted by JNTU for AP &amp; Telangana</li>
        <li>160 questions | 160 marks | 3 hours</li>
        <li>Physics (40) + Chemistry (40) + Math (80)</li>
        </ul></div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-box">
        <h4 style="color:#ffa500;margin-top:0;">📋 About JEE Mains</h4>
        <ul style="color:rgba(255,255,255,.8);margin:0;padding-left:20px;">
        <li>Joint Entrance Examination Main</li>
        <li>Conducted by NTA twice a year</li>
        <li>90 questions | 300 marks | 3 hours</li>
        <li>Physics (30) + Chemistry (30) + Math (30)</li>
        </ul></div>
        """, unsafe_allow_html=True)

    results = get_student_results(user["username"])
    if not results.empty:
        st.markdown("### 📈 Your Quick Stats")
        c1, c2, c3, c4 = st.columns(4)
        total_tests = len(results)
        avg_score = results["score"].mean()
        total_c = results["correct"].sum()
        total_w = results["incorrect"].sum()
        accuracy = (total_c / (total_c + total_w) * 100) if (total_c + total_w) > 0 else 0
        best_score = results["score"].max()
        for col, val, label, color in [
            (c1, total_tests, "Tests Taken", "#6495ed"),
            (c2, f"{avg_score:.1f}", "Avg Score", "#ffa500"),
            (c3, f"{accuracy:.1f}%", "Accuracy", "#32cd32"),
            (c4, best_score, "Best Score", "#ff6b6b"),
        ]:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color:{color};">{val}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────
def page_dashboard():
    user = st.session_state.user
    st.markdown("## 📊 Performance Dashboard")

    results = get_student_results(user["username"])
    if results.empty:
        st.info("🔔 No test data yet. Take some tests to see your analytics!")
        return

    # KPIs
    total_c = results["correct"].sum()
    total_w = results["incorrect"].sum()
    accuracy = (total_c / (total_c + total_w) * 100) if (total_c + total_w) > 0 else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, val, label, color in [
        (c1, len(results), "Tests Taken", "#6495ed"),
        (c2, f"{results['score'].mean():.1f}", "Avg Score", "#ffa500"),
        (c3, f"{accuracy:.1f}%", "Accuracy", "#32cd32"),
        (c4, results.iloc[-1]["score"], "Last Score", "#9b59b6"),
        (c5, results["score"].max(), "Best Score", "#ff6b6b"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color:{color};">{val}</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Safe subject performance
    grp = results.groupby("subject")
    subj_perf = grp.agg(avg_score=("score", "mean"), tests=("score", "count")).reset_index()
    def _acc(g):
        c, w = g["correct"].sum(), g["incorrect"].sum()
        return (c / (c + w) * 100) if (c + w) > 0 else 0
    acc_df = grp.apply(_acc).reset_index()
    acc_df.columns = ["subject", "avg_accuracy"]
    subj_perf = subj_perf.merge(acc_df, on="subject", how="left")
    subj_perf["avg_accuracy"] = subj_perf["avg_accuracy"].fillna(0)

    CMAP = {"Physics": "#6495ed", "Chemistry": "#32cd32", "Mathematics": "#ffa500"}

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 📈 Score Trend")
        results["test_date"] = pd.to_datetime(results["test_date"], errors="coerce")
        fig = px.line(results.sort_values("test_date"), x="test_date", y="score",
                      color="subject", markers=True, template="plotly_dark",
                      color_discrete_map=CMAP)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="white", margin=dict(l=0,r=0,t=20,b=0),
                          legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("#### 🎯 Subject Average Score")
        fig2 = px.bar(subj_perf, x="subject", y="avg_score", color="subject",
                      template="plotly_dark", color_discrete_map=CMAP, text="avg_score")
        fig2.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="white", margin=dict(l=0,r=0,t=20,b=0), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### ✅ Correct vs Incorrect")
        fig3 = go.Figure(go.Pie(
            labels=["Correct", "Incorrect", "Unattempted"],
            values=[int(results["correct"].sum()), int(results["incorrect"].sum()), int(results["unattempted"].sum())],
            hole=0.55, marker_colors=["#32cd32", "#ff4444", "#888888"],
        ))
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white",
                           margin=dict(l=0,r=0,t=0,b=0), legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        st.markdown("#### 💪 Strength Analysis")
        max_score_ref = 50
        for _, row in subj_perf.iterrows():
            subj = row["subject"]
            pct = min(row["avg_score"] / max_score_ref, 1.0)
            color = subject_color(subj)
            label = "💪 Strong" if pct >= 0.7 else "⚠️ Average" if pct >= 0.5 else "🔴 Needs Work"
            st.markdown(f"**{subj}** — {label}")
            st.progress(float(pct))
            st.markdown("")

    st.markdown("#### 📋 Recent Test History")
    display_cols = [c for c in ["test_date","subject","chapter","score","correct","incorrect","unattempted","test_type"] if c in results.columns]
    st.dataframe(results.sort_values("test_date", ascending=False).head(10)[display_cols],
                 use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────
#  PAGE: MATERIALS
# ─────────────────────────────────────────────────────────────
def page_materials():
    st.markdown("## 📚 Study Materials")

    subjects = list(MATERIALS.keys())
    c1, c2 = st.columns(2)
    with c1:
        sel_subj = st.selectbox("📚 Subject", subjects, key="mat_subject")
    with c2:
        chapters = list(MATERIALS[sel_subj].keys())
        sel_chap = st.selectbox("📖 Chapter", chapters, key="mat_chapter")

    mat = MATERIALS[sel_subj][sel_chap]

    tab1, tab2, tab3 = st.tabs(["📖 Theory", "❓ Practice Q&A", "🤖 AI Tutor"])

    with tab1:
        color = subject_color(sel_subj)
        bc = subject_badge(sel_subj)
        st.markdown(f'<span class="badge {bc}">{sel_subj}</span><span class="badge badge-easy">{sel_chap}</span>', unsafe_allow_html=True)
        st.markdown(mat["theory"])

    with tab2:
        st.markdown(f"### Practice Questions — {sel_chap}")
        for i, item in enumerate(mat["questions"], 1):
            with st.expander(f"**Q{i}.** {item['q']}"):
                st.markdown(f"""
                <div class="success-box"><strong>✅ Answer:</strong> {item['a']}</div>
                <div class="info-box"><strong>💡 Explanation:</strong> {item['exp']}</div>
                """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### 🤖 AI Tutor — Ask Anything!")
        st.markdown("""
        <div class="info-box">
        ℹ️ Currently running in <strong>smart keyword mode</strong>.
        To enable full AI responses connect your Anthropic API key in the code.
        </div>""", unsafe_allow_html=True)

        for msg in st.session_state.chatbot_history:
            bg = "rgba(100,149,237,.1)" if msg["role"] == "user" else "rgba(50,205,50,.1)"
            who = "🧑 You" if msg["role"] == "user" else "🤖 AI Tutor"
            st.markdown(f"""
            <div style='background:{bg};border-radius:12px;padding:12px 16px;margin:8px 0;'>
            <strong>{who}:</strong><br>{msg["content"]}
            </div>""", unsafe_allow_html=True)

        user_q = st.text_input("💬 Ask your question here...", key="ai_q")
        bc1, bc2 = st.columns([1, 4])
        with bc1:
            send = st.button("📤 Send", type="primary")
        with bc2:
            clear = st.button("🗑️ Clear Chat")

        if send and user_q.strip():
            st.session_state.chatbot_history.append({"role": "user", "content": user_q})
            q_low = user_q.lower()
            if any(w in q_low for w in ["newton", "force", "motion", "acceleration"]):
                ans = "Newton's Second Law: F = ma. The net force equals mass times acceleration. Third Law: every action has an equal and opposite reaction."
            elif any(w in q_low for w in ["photon", "energy", "wavelength", "quantum"]):
                ans = "Energy of a photon: E = hf = hc/λ where h = 6.626×10⁻³⁴ J·s and c = 3×10⁸ m/s."
            elif any(w in q_low for w in ["integral", "integrate", "differentiat", "derivative", "calculus"]):
                ans = "Power rule: d/dx(xⁿ) = nxⁿ⁻¹. Integration: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C. Don't forget the constant C!"
            elif any(w in q_low for w in ["organic", "carbon", "hybridis", "hybridiz", "iupac"]):
                ans = "Carbon is tetravalent (4 bonds). sp³ → tetrahedral (109.5°), sp² → planar (120°), sp → linear (180°). IUPAC: longest chain → number from substituent end → name by functional group."
            elif any(w in q_low for w in ["equilibrium", "pH", "acid", "base", "buffer"]):
                ans = "pH = −log[H⁺]. For strong acids like HCl: [H⁺] = concentration. At equilibrium: rate(forward) = rate(reverse). Kw = [H⁺][OH⁻] = 10⁻¹⁴ at 25°C."
            elif any(w in q_low for w in ["bohr", "orbit", "electron", "atom", "quantum number"]):
                ans = "Bohr's model: Eₙ = −13.6/n² eV. rₙ = 0.529 n² Å. Quantum numbers: n (shell), l (subshell, 0 to n-1), m (−l to +l), s (±½)."
            elif any(w in q_low for w in ["sin", "cos", "tan", "trigon", "identity"]):
                ans = "Key identities: sin²θ + cos²θ = 1, tan θ = sinθ/cosθ, sin(A+B) = sinA cosB + cosA sinB. sin 30°=½, cos 60°=½, tan 45°=1."
            else:
                ans = f"Great question! For '{user_q}' please check the Theory tab for detailed notes on this topic. To get full AI-powered answers, connect your Anthropic API key in the source code."
            st.session_state.chatbot_history.append({"role": "assistant", "content": ans})
            st.rerun()

        if clear:
            st.session_state.chatbot_history = []
            st.rerun()

# ─────────────────────────────────────────────────────────────
#  PAGE: DAILY PRACTICE
# ─────────────────────────────────────────────────────────────
def page_daily_practice():
    st.markdown("## ✏️ Daily Practice — 10 Questions")
    user = st.session_state.user

    # Initialise questions for today (seed = date so same questions all day)
    if not st.session_state.daily_questions:
        df = get_questions()
        if df.empty or len(df) < 5:
            st.error("Not enough questions in the database.")
            return
        seed = int(datetime.now().strftime("%Y%m%d"))
        sampled = df.sample(min(10, len(df)), random_state=seed)
        st.session_state.daily_questions = sampled.to_dict("records")
        st.session_state.daily_answers = {}
        st.session_state.daily_submitted = False

    questions = st.session_state.daily_questions

    if not st.session_state.daily_submitted:
        st.markdown(f"""
        <div class="info-box">
        📅 <strong>Today's Practice</strong> — {datetime.now().strftime("%B %d, %Y")}
        | {len(questions)} Questions | No time limit | +4 per correct
        </div>""", unsafe_allow_html=True)

        for i, q in enumerate(questions):
            bc = subject_badge(q["subject"])
            diff = q.get("difficulty", "Easy")
            diff_cls = "badge-easy" if diff == "Easy" else "badge-medium" if diff == "Medium" else "badge-hard"
            st.markdown(f"""
            <div class="question-card">
            <span class="badge {bc}">{q['subject']}</span>
            <span class="badge {diff_cls}">{diff}</span>
            <h4 style="color:white;margin:12px 0 4px;">Q{i+1}. {q['question']}</h4>
            </div>""", unsafe_allow_html=True)

            opts = {"A": q["option_a"], "B": q["option_b"], "C": q["option_c"], "D": q["option_d"]}
            choices = ["Not Attempted", "A", "B", "C", "D"]
            prev = st.session_state.daily_answers.get(i)
            default_idx = choices.index(prev) if prev in choices else 0

            sel = st.radio(
                f"q{i}",
                options=choices,
                format_func=lambda k, o=opts: k if k == "Not Attempted" else f"{k}. {o[k]}",
                index=default_idx,
                key=f"dp_{i}",
                label_visibility="collapsed",
            )
            st.session_state.daily_answers[i] = None if sel == "Not Attempted" else sel

        st.markdown("")
        if st.button("📤 Submit Daily Practice", type="primary", use_container_width=True):
            st.session_state.daily_submitted = True
            st.rerun()

    else:
        # Results
        correct = 0
        wrong = 0
        for i, q in enumerate(questions):
            ans = st.session_state.daily_answers.get(i)
            if ans == q["correct_answer"]:
                correct += 1
            elif ans is not None:
                wrong += 1
                save_mistake(user["username"], q["id"], q["subject"], q["chapter"], ans, q["correct_answer"])

        unattempted = len(questions) - correct - wrong
        score = correct * 4
        save_result(user["username"], "Mixed", "Daily Practice", score, len(questions),
                    correct, wrong, unattempted, 0, "daily_practice")

        pct = correct / len(questions) * 100
        color = "#32cd32" if pct >= 70 else "#ffa500" if pct >= 50 else "#ff4444"
        msg = "🎉 Excellent!" if pct >= 80 else "👍 Good Job!" if pct >= 60 else "📖 Keep Practicing!"
        st.markdown(f"""
        <div class="metric-card" style="border-top:4px solid {color};margin-bottom:24px;">
            <div class="metric-value" style="color:{color};">{correct}/{len(questions)}</div>
            <div class="metric-label">{msg} &nbsp;|&nbsp; Score: {score} marks</div>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        for col, val, label, clr in [(c1, correct, "✅ Correct", "#32cd32"), (c2, wrong, "❌ Wrong", "#ff4444"), (c3, unattempted, "⏭️ Skipped", "#888")]:
            with col:
                st.markdown(f"""<div class="metric-card"><div class="metric-value" style="color:{clr};">{val}</div><div class="metric-label">{label}</div></div>""", unsafe_allow_html=True)

        st.markdown("### 📋 Question Review")
        for i, q in enumerate(questions):
            ans = st.session_state.daily_answers.get(i)
            is_correct = ans == q["correct_answer"]
            opts = {"A": q["option_a"], "B": q["option_b"], "C": q["option_c"], "D": q["option_d"]}
            icon = "✅" if is_correct else ("❌" if ans else "⏭️")
            with st.expander(f"{icon} Q{i+1}: {q['question'][:80]}"):
                bg = "rgba(50,205,50,.07)" if is_correct else "rgba(255,68,68,.07)" if ans else "rgba(128,128,128,.07)"
                your_ans = f"{ans}. {opts.get(ans,'')}" if ans else "Not Attempted"
                st.markdown(f"""
                <div style='background:{bg};border-radius:12px;padding:16px;'>
                <b>Your Answer:</b> {your_ans}<br>
                <b>Correct Answer:</b> {q['correct_answer']}. {opts[q['correct_answer']]}
                </div>
                <div class="info-box" style="margin-top:8px;">
                <b>💡 Explanation:</b> {q['explanation']}
                </div>""", unsafe_allow_html=True)

        if st.button("🔄 Reset for New Session", type="primary"):
            st.session_state.daily_questions = []
            st.session_state.daily_answers = {}
            st.session_state.daily_submitted = False
            st.rerun()

# ─────────────────────────────────────────────────────────────
#  PAGE: TAKE TEST
# ─────────────────────────────────────────────────────────────
def page_take_test():
    st.markdown("## 📝 Take a Test")
    user = st.session_state.user

    # ── Once-per-session guard
    if st.session_state.get("test_completed") and not st.session_state.test_submitted:
        st.markdown("""
        <div class="error-box">
        🔒 <b>You have already completed a test this session.</b><br>
        Log out and log back in to take another test.
        </div>""", unsafe_allow_html=True)
        return

    # ── Setup screen
    if not st.session_state.test_active and not st.session_state.test_submitted:
        st.markdown("### ⚙️ Configure Your Test")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            subject = st.selectbox("📚 Subject", ["All", "Physics", "Chemistry", "Mathematics"], key="cfg_subj")
        with c2:
            df_q = get_questions(subject if subject != "All" else None)
            chapters = ["All"] + sorted(df_q["chapter"].unique().tolist()) if not df_q.empty else ["All"]
            chapter = st.selectbox("📖 Chapter", chapters, key="cfg_chap")
        with c3:
            num_q = st.selectbox("🔢 Questions", [5, 10, 15, 20, 30], index=1, key="cfg_num")
        with c4:
            duration_min = st.selectbox("⏱️ Duration (min)", [10, 15, 20, 30, 45, 60], index=2, key="cfg_dur")

        neg = st.checkbox("➖ Negative marking (−1 for wrong)", value=True, key="cfg_neg")
        st.markdown("""<div class="info-box">ℹ️ <b>Scoring:</b> Correct = +4 &nbsp;|&nbsp; Wrong = −1 (if enabled) &nbsp;|&nbsp; Unattempted = 0</div>""", unsafe_allow_html=True)

        if st.button("🚀 Start Test", type="primary", use_container_width=True):
            qs = get_questions(subject if subject != "All" else None, chapter if chapter != "All" else None)
            if qs.empty or len(qs) < 3:
                st.error("Not enough questions for this selection. Try a broader filter.")
                return
            sampled = qs.sample(min(num_q, len(qs))).to_dict("records")
            st.session_state.test_questions = sampled
            st.session_state.test_answers = {}
            st.session_state.test_active = True
            st.session_state.test_submitted = False
            st.session_state.test_end_time = None
            st.session_state.test_start_time = time.time()
            st.session_state.test_config = {
                "subject": subject, "chapter": chapter,
                "duration": duration_min * 60, "neg_marking": neg,
            }
            st.rerun()

    # ── Active test
    elif st.session_state.test_active and not st.session_state.test_submitted:
        cfg = st.session_state.get("test_config", {"subject": "All", "chapter": "All", "duration": 1200, "neg_marking": True})
        elapsed = time.time() - (st.session_state.test_start_time or time.time())
        remaining = max(0.0, cfg["duration"] - elapsed)
        questions = st.session_state.test_questions

        mins, secs = int(remaining // 60), int(remaining % 60)
        pct_rem = remaining / cfg["duration"] if cfg["duration"] > 0 else 0
        tcol = "#32cd32" if pct_rem > 0.5 else "#ffa500" if pct_rem > 0.25 else "#ff4444"

        hdr_col, stat_col = st.columns([3, 1])
        with hdr_col:
            st.markdown(f"""
            <div style='background:rgba(0,0,0,.3);border-radius:12px;padding:16px;margin-bottom:16px;'>
            <div style='display:flex;justify-content:space-between;align-items:center;'>
                <span style='font-weight:700;font-size:1.1rem;'>📝 {cfg["subject"]} Test — {len(questions)} Qs</span>
                <span style='font-size:1.8rem;font-weight:800;color:{tcol};'>⏱️ {mins:02d}:{secs:02d}</span>
            </div>
            <div style='background:rgba(255,255,255,.1);border-radius:3px;height:6px;margin-top:10px;'>
                <div style='background:{tcol};width:{pct_rem*100:.1f}%;height:6px;border-radius:3px;'></div>
            </div></div>""", unsafe_allow_html=True)
        with stat_col:
            answered = sum(1 for v in st.session_state.test_answers.values() if v is not None)
            st.markdown(f"""<div class="metric-card"><div class="metric-value" style="color:#6495ed;">{answered}/{len(questions)}</div><div class="metric-label">Answered</div></div>""", unsafe_allow_html=True)

        # Render questions
        for i, q in enumerate(questions):
            opts = {"A": q["option_a"], "B": q["option_b"], "C": q["option_c"], "D": q["option_d"]}
            bc = subject_badge(q["subject"])
            neg_label = "-1" if cfg["neg_marking"] else "0"
            st.markdown(f"""
            <div class="question-card">
            <span class="badge {bc}">{q['subject']}</span>
            <span class="badge badge-easy" style="background:rgba(255,255,255,.1);color:rgba(255,255,255,.7);">+4 / {neg_label}</span>
            <h4 style="color:white;margin:12px 0 4px;">Q{i+1}. {q['question']}</h4>
            </div>""", unsafe_allow_html=True)

            choices = ["Not Attempted", "A", "B", "C", "D"]
            prev = st.session_state.test_answers.get(i)
            default_idx = choices.index(prev) if prev in choices else 0

            sel = st.radio(
                f"tq{i}",
                options=choices,
                format_func=lambda k, o=opts: k if k == "Not Attempted" else f"{k}. {o[k]}",
                index=default_idx,
                key=f"test_q_{i}",
                label_visibility="collapsed",
            )
            st.session_state.test_answers[i] = None if sel == "Not Attempted" else sel

        st.markdown("")
        col_sub, col_end = st.columns(2)
        with col_sub:
            if st.button("📤 Submit Test", type="primary", use_container_width=True):
                st.session_state.test_active = False
                st.session_state.test_submitted = True
                st.session_state.test_end_time = time.time()
                st.rerun()
        with col_end:
            if st.button("🚫 Abandon Test", use_container_width=True):
                st.session_state.test_active = False
                st.session_state.test_submitted = False
                st.session_state.test_questions = []
                st.session_state.test_answers = {}
                st.rerun()

        # Auto-submit when timer expires
        if remaining <= 0:
            st.warning("⏰ Time's up! Auto-submitting your test...")
            st.session_state.test_active = False
            st.session_state.test_submitted = True
            st.session_state.test_end_time = time.time()
            st.rerun()

    # ── Results screen
    elif st.session_state.test_submitted:
        questions = st.session_state.test_questions
        answers = st.session_state.test_answers
        cfg = st.session_state.get("test_config", {"subject": "Mixed", "chapter": "All", "neg_marking": True, "duration": 1200})
        t_start = st.session_state.get("test_start_time") or time.time()
        t_end = st.session_state.get("test_end_time") or time.time()
        time_taken = int(t_end - t_start)

        correct = wrong = unattempted = score = 0
        for i, q in enumerate(questions):
            ans = answers.get(i)
            if ans is None:
                unattempted += 1
            elif ans == q["correct_answer"]:
                correct += 1
                score += 4
            else:
                wrong += 1
                if cfg["neg_marking"]:
                    score -= 1
                save_mistake(user["username"], q["id"], q["subject"], q["chapter"], ans, q["correct_answer"])

        max_score = len(questions) * 4
        save_result(user["username"], cfg["subject"], cfg["chapter"], score, len(questions),
                    correct, wrong, unattempted, time_taken, "chapter_test")

        pct = max(0, score / max_score * 100) if max_score > 0 else 0
        grade = "A+" if pct >= 90 else "A" if pct >= 80 else "B" if pct >= 70 else "C" if pct >= 60 else "D" if pct >= 50 else "F"
        grade_color = "#32cd32" if pct >= 70 else "#ffa500" if pct >= 50 else "#ff4444"
        msg = "🎉 Outstanding!" if pct >= 90 else "👏 Well Done!" if pct >= 70 else "📚 Keep Studying!"

        st.markdown(f"""
        <div class="hero-header">
            <div style="font-size:4rem;">{grade}</div>
            <div class="hero-title" style="font-size:2.5rem;color:{grade_color};">{score} / {max_score}</div>
            <div class="hero-subtitle">{msg}</div>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        for col, val, label, clr in [
            (c1, correct, "✅ Correct", "#32cd32"),
            (c2, wrong, "❌ Wrong", "#ff4444"),
            (c3, unattempted, "⏭️ Unattempted", "#888"),
            (c4, f"{time_taken//60}m {time_taken%60}s", "⏱️ Time", "#6495ed"),
        ]:
            with col:
                st.markdown(f"""<div class="metric-card"><div class="metric-value" style="color:{clr};">{val}</div><div class="metric-label">{label}</div></div>""", unsafe_allow_html=True)

        st.markdown("### 📋 Detailed Solutions")
        for i, q in enumerate(questions):
            ans = answers.get(i)
            opts = {"A": q["option_a"], "B": q["option_b"], "C": q["option_c"], "D": q["option_d"]}
            is_correct = ans == q["correct_answer"]
            icon = "✅" if is_correct else ("❌" if ans else "⏭️")
            with st.expander(f"{icon} Q{i+1}: {q['question'][:70]}"):
                bg = "rgba(50,205,50,.07)" if is_correct else "rgba(255,68,68,.07)" if ans else "rgba(128,128,128,.07)"
                your_ans = f"{ans}. {opts.get(ans,'')}" if ans else "Not Attempted"
                st.markdown(f"""
                <div style='background:{bg};border-radius:12px;padding:16px;'>
                <b>Your Answer:</b> {your_ans}<br>
                <b>Correct Answer:</b> {q['correct_answer']}. {opts[q['correct_answer']]}
                </div>
                <div class="info-box" style="margin-top:8px;"><b>💡 Explanation:</b> {q['explanation']}</div>
                """, unsafe_allow_html=True)

        st.session_state.test_completed = True

        st.markdown("""
        <div class="info-box" style="margin-top:20px;">
        ⚠️ <b>Test completed.</b> You can only take one test per session. Log out and log back in to take a new test.
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  CHALLENGE HELPERS
# ─────────────────────────────────────────────────────────────
def _user_already_joined(username: str, ch_id) -> bool:
    df = load_csv("challenge_results.csv")
    if df.empty:
        return False
    return not df[(df["username"] == username) & (df["challenge_id"].astype(str) == str(ch_id))].empty


def _save_challenge_result(username, ch_id, ch_subject, score, correct, wrong, unattempted, time_sec):
    df = load_csv("challenge_results.csv")
    new_row = pd.DataFrame([{
        "challenge_id": ch_id,
        "username": username,
        "subject": ch_subject,
        "score": score,
        "correct": correct,
        "incorrect": wrong,
        "unattempted": unattempted,
        "time_taken": round(time_sec / 60, 1),
        "date": datetime.now().strftime("%Y-%m-%d"),
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    save_csv(df, "challenge_results.csv")
    # also write to results.csv so dashboard/leaderboard picks it up
    save_result(username, ch_subject, "Challenge", score,
                correct + wrong + unattempted, correct, wrong, unattempted,
                int(time_sec), "challenge")


# ─────────────────────────────────────────────────────────────
#  PAGE: CHALLENGES
# ─────────────────────────────────────────────────────────────
def page_challenges():
    user = st.session_state.user
    username = user["username"]

    # ── If a challenge test is actively running, render it
    if st.session_state.get("active_challenge"):
        _render_challenge_test(username)
        return

    st.markdown("## ⚔️ Live Challenges")
    challenges = load_csv("challenges.csv")
    ch_results = load_csv("challenge_results.csv")

    if challenges.empty:
        st.info("No challenges available. Ask your admin to create some!")
        return

    for _, ch in challenges.iterrows():
        ch_id  = ch["challenge_id"]
        status = str(ch.get("status", "upcoming"))
        scol   = "#32cd32" if status == "active" else "#ffa500" if status == "upcoming" else "#888"
        sicon  = "🟢" if status == "active" else "🟡" if status == "upcoming" else "⚫"
        bc     = subject_badge(str(ch.get("subject", "Physics")))
        joined = _user_already_joined(username, ch_id)

        st.markdown(f"""
        <div class="question-card" style="border-left:4px solid {scol};">
        <div style="display:flex;justify-content:space-between;align-items:start;">
            <div>
                <h3 style="color:white;margin:0 0 8px;">{ch['title']}</h3>
                <span class="badge {bc}">{ch['subject']}</span>
                <span class="badge" style="background:rgba(255,255,255,.1);color:rgba(255,255,255,.7);">{sicon} {status.title()}</span>
                <span class="badge" style="background:rgba(255,255,255,.1);color:rgba(255,255,255,.7);">⏱️ {ch['duration_minutes']} min</span>
            </div>
            <div style="text-align:right;color:rgba(255,255,255,.5);font-size:.85rem;">
                Created by {ch['created_by']}<br>{ch['created_date']}
            </div>
        </div></div>""", unsafe_allow_html=True)

        if status == "active":
            if joined:
                st.markdown('<div class="success-box">✅ You have already completed this challenge.</div>', unsafe_allow_html=True)
            else:
                if st.button(f"⚔️ Join: {ch['title']}", key=f"join_{ch_id}", type="primary"):
                    # load questions for this challenge
                    subj = str(ch.get("subject", "All"))
                    qs = get_questions(None if subj == "All" else subj)
                    if qs.empty or len(qs) < 3:
                        st.error("Not enough questions for this challenge. Ask admin to add more.")
                    else:
                        num_q = min(15, len(qs))
                        sampled = qs.sample(num_q).to_dict("records")
                        st.session_state.active_challenge = {
                            "id": ch_id,
                            "title": ch["title"],
                            "subject": subj,
                            "duration": int(ch.get("duration_minutes", 30)) * 60,
                        }
                        st.session_state.ch_questions  = sampled
                        st.session_state.ch_answers    = {}
                        st.session_state.ch_submitted  = False
                        st.session_state.ch_start_time = time.time()
                        st.session_state.ch_end_time   = None
                        st.rerun()
        elif status == "upcoming":
            st.markdown(f'<div class="info-box">📅 Starts: {ch.get("start_time","TBD")}</div>', unsafe_allow_html=True)

        # Per-challenge mini leaderboard
        if status in ["completed", "active"] and not ch_results.empty:
            filt = ch_results[ch_results["challenge_id"].astype(str) == str(ch_id)]
            if not filt.empty:
                with st.expander(f"🏆 Results — {ch['title']}"):
                    filt_sorted = filt.sort_values("score", ascending=False).reset_index(drop=True)
                    for idx2, row2 in filt_sorted.iterrows():
                        rank = idx2 + 1
                        rclass = f"rank-{rank}" if rank <= 3 else ""
                        medal  = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
                        st.markdown(f"""
                        <div class="leaderboard-row {rclass}">
                            <span style="font-size:1.3rem;margin-right:16px;">{medal}</span>
                            <span style="flex:1;font-weight:600;color:white;">{row2['username']}</span>
                            <span style="color:#ffd700;font-weight:700;">{int(row2['score'])} pts</span>
                            <span style="color:rgba(255,255,255,.5);margin-left:16px;">⏱️ {row2['time_taken']}m</span>
                        </div>""", unsafe_allow_html=True)
        st.markdown("")


def _render_challenge_test(username: str):
    ch_meta   = st.session_state.active_challenge
    questions = st.session_state.ch_questions

    st.markdown(f"## ⚔️ {ch_meta['title']}")

    if not st.session_state.ch_submitted:
        elapsed   = time.time() - (st.session_state.ch_start_time or time.time())
        remaining = max(0.0, ch_meta["duration"] - elapsed)
        mins, secs = int(remaining // 60), int(remaining % 60)
        pct_rem    = remaining / ch_meta["duration"] if ch_meta["duration"] > 0 else 0
        tcol       = "#32cd32" if pct_rem > 0.5 else "#ffa500" if pct_rem > 0.25 else "#ff4444"

        st.markdown(f"""
        <div style='background:rgba(0,0,0,.3);border-radius:12px;padding:16px;margin-bottom:16px;'>
        <div style='display:flex;justify-content:space-between;align-items:center;'>
            <span style='font-weight:700;font-size:1.1rem;'>⚔️ {ch_meta["subject"]} — {len(questions)} Qs</span>
            <span style='font-size:1.8rem;font-weight:800;color:{tcol};'>⏱️ {mins:02d}:{secs:02d}</span>
        </div>
        <div style='background:rgba(255,255,255,.1);border-radius:3px;height:6px;margin-top:10px;'>
            <div style='background:{tcol};width:{pct_rem*100:.1f}%;height:6px;border-radius:3px;'></div>
        </div></div>""", unsafe_allow_html=True)

        for i, q in enumerate(questions):
            opts = {"A": q["option_a"], "B": q["option_b"], "C": q["option_c"], "D": q["option_d"]}
            bc   = subject_badge(q["subject"])
            st.markdown(f"""
            <div class="question-card">
            <span class="badge {bc}">{q['subject']}</span>
            <h4 style="color:white;margin:12px 0 4px;">Q{i+1}. {q['question']}</h4>
            </div>""", unsafe_allow_html=True)

            choices = ["Not Attempted", "A", "B", "C", "D"]
            prev = st.session_state.ch_answers.get(i)
            default_idx = choices.index(prev) if prev in choices else 0
            sel = st.radio(
                f"chq{i}",
                options=choices,
                format_func=lambda k, o=opts: k if k == "Not Attempted" else f"{k}. {o[k]}",
                index=default_idx,
                key=f"ch_q_{i}",
                label_visibility="collapsed",
            )
            st.session_state.ch_answers[i] = None if sel == "Not Attempted" else sel

        col_s, col_a = st.columns(2)
        with col_s:
            if st.button("📤 Submit Challenge", type="primary", use_container_width=True):
                st.session_state.ch_submitted  = True
                st.session_state.ch_end_time   = time.time()
                st.rerun()
        with col_a:
            if st.button("🚫 Abandon", use_container_width=True):
                for k in ["active_challenge", "ch_questions", "ch_answers", "ch_submitted", "ch_start_time", "ch_end_time"]:
                    st.session_state[k] = [] if k in ("ch_questions", "ch_answers") else (False if k == "ch_submitted" else None)
                st.rerun()

        if remaining <= 0:
            st.session_state.ch_submitted = True
            st.session_state.ch_end_time  = time.time()
            st.rerun()

    else:
        # ── Challenge results ─────────────────────────────────────────────
        answers    = st.session_state.ch_answers
        t_start    = st.session_state.ch_start_time or time.time()
        t_end      = st.session_state.ch_end_time   or time.time()
        time_taken = t_end - t_start

        correct = wrong = unattempted = score = 0
        for i, q in enumerate(questions):
            ans = answers.get(i)
            if ans is None:
                unattempted += 1
            elif ans == q["correct_answer"]:
                correct += 1
                score   += 4
            else:
                wrong += 1
                score -= 1
                save_mistake(username, q["id"], q["subject"], q["chapter"], ans, q["correct_answer"])

        # Save once (guard: already joined check happens before starting)
        _save_challenge_result(
            username, ch_meta["id"], ch_meta["subject"],
            score, correct, wrong, unattempted, time_taken
        )

        max_score = len(questions) * 4
        pct   = max(0, score / max_score * 100) if max_score > 0 else 0
        grade_color = "#32cd32" if pct >= 70 else "#ffa500" if pct >= 50 else "#ff4444"

        st.markdown(f"""
        <div class="hero-header">
            <div style="font-size:4rem;">⚔️</div>
            <div class="hero-title" style="font-size:2.5rem;color:{grade_color};">{score} / {max_score}</div>
            <div class="hero-subtitle">Challenge Complete! {correct} correct · {wrong} wrong · {unattempted} skipped</div>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        for col, val, label, clr in [
            (c1, correct,     "✅ Correct",     "#32cd32"),
            (c2, wrong,       "❌ Wrong",        "#ff4444"),
            (c3, unattempted, "⏭️ Unattempted", "#888"),
            (c4, f"{int(time_taken//60)}m {int(time_taken%60)}s", "⏱️ Time", "#6495ed"),
        ]:
            with col:
                st.markdown(f"""<div class="metric-card"><div class="metric-value" style="color:{clr};">{val}</div><div class="metric-label">{label}</div></div>""", unsafe_allow_html=True)

        st.markdown("### 📋 Detailed Solutions")
        for i, q in enumerate(questions):
            ans  = answers.get(i)
            opts = {"A": q["option_a"], "B": q["option_b"], "C": q["option_c"], "D": q["option_d"]}
            is_correct = ans == q["correct_answer"]
            icon = "✅" if is_correct else ("❌" if ans else "⏭️")
            with st.expander(f"{icon} Q{i+1}: {q['question'][:70]}"):
                bg       = "rgba(50,205,50,.07)" if is_correct else "rgba(255,68,68,.07)" if ans else "rgba(128,128,128,.07)"
                your_ans = f"{ans}. {opts.get(ans,'')}" if ans else "Not Attempted"
                st.markdown(f"""
                <div style='background:{bg};border-radius:12px;padding:16px;'>
                <b>Your Answer:</b> {your_ans}<br>
                <b>Correct Answer:</b> {q['correct_answer']}. {opts[q['correct_answer']]}
                </div>
                <div class="info-box" style="margin-top:8px;"><b>💡 Explanation:</b> {q['explanation']}</div>
                """, unsafe_allow_html=True)

        if st.button("← Back to Challenges", type="primary", use_container_width=True):
            for k in ["active_challenge", "ch_questions", "ch_answers", "ch_start_time", "ch_end_time"]:
                st.session_state[k] = [] if k in ("ch_questions","ch_answers") else None
            st.session_state.ch_submitted = False
            st.rerun()

# ─────────────────────────────────────────────────────────────
#  PAGE: LEADERBOARD
# ─────────────────────────────────────────────────────────────
def _lb_rows(df: pd.DataFrame, val_col: str, val_fmt=None, extra_cols=None):
    """Render ranked leaderboard rows."""
    students = load_csv("students.csv")
    if not students.empty:
        df = df.merge(students[["username", "name"]], on="username", how="left")
        df["display_name"] = df["name"].fillna(df["username"])
    else:
        df["display_name"] = df["username"]

    for idx, row in df.iterrows():
        rank   = idx + 1
        rclass = f"rank-{rank}" if rank <= 3 else ""
        medal  = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        val    = val_fmt(row[val_col]) if val_fmt else str(row[val_col])
        extra  = ""
        if extra_cols:
            extra = " &nbsp;|&nbsp; ".join(
                f'<span style="color:rgba(255,255,255,.5);">{lbl}: {row.get(col, 0)}</span>'
                for col, lbl in extra_cols
            )
        st.markdown(f"""
        <div class="leaderboard-row {rclass}" style="display:flex;align-items:center;">
            <span style="font-size:1.4rem;margin-right:16px;">{medal}</span>
            <span style="flex:1;font-weight:600;color:white;font-size:1rem;">{row['display_name']}</span>
            {extra}&nbsp;
            <span style="color:#ffd700;font-weight:700;font-size:1.1rem;margin-left:16px;">{val}</span>
        </div>""", unsafe_allow_html=True)


def page_leaderboard():
    st.markdown("## 🏆 Leaderboard")
    ch_results = load_csv("challenge_results.csv")
    results    = load_csv("results.csv")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⚔️ Challenge Points",
        "🔥 Streak",
        "📅 Daily Practice",
        "🔬 Subject: Physics",
        "⚗️ Subject: Chemistry",
    ])

    # ── Tab 1: Challenge Points (PRIMARY) ────────────────────────────────────
    with tab1:
        st.markdown("""<div class="info-box">🏆 <b>Primary Leaderboard</b> — ranked by total points earned across all challenges (score column from challenge_results.csv). Challenges use +4 / −1 scoring.</div>""", unsafe_allow_html=True)
        if ch_results.empty:
            st.info("No challenge results yet. Join an active challenge to appear here!")
        else:
            lb = (
                ch_results.groupby("username")
                .agg(total_pts=("score", "sum"), challenges=("score", "count"))
                .reset_index()
                .sort_values("total_pts", ascending=False)
                .reset_index(drop=True)
            )
            _lb_rows(lb, "total_pts",
                     val_fmt=lambda v: f"{int(v)} pts",
                     extra_cols=[("challenges", "Challenges")])

            st.markdown("### 📊 Points Comparison")
            students = load_csv("students.csv")
            if not students.empty:
                lb2 = lb.merge(students[["username", "name"]], on="username", how="left")
                lb2["display_name"] = lb2["name"].fillna(lb2["username"])
            else:
                lb2 = lb.copy()
                lb2["display_name"] = lb2["username"]

            fig = px.bar(lb2.head(10), x="display_name", y="total_pts",
                         color="total_pts", color_continuous_scale="viridis",
                         template="plotly_dark",
                         labels={"total_pts": "Challenge Points", "display_name": "Student"})
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color="white", margin=dict(l=0,r=0,t=20,b=0), coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

    # ── Tab 2: Streak (based on daily practice completions) ──────────────────
    with tab2:
        st.markdown("""<div class="info-box">🔥 <b>Streak Leaderboard</b> — ranked by number of consecutive days with at least one daily practice or challenge completed (based on results.csv test_type = daily_practice).</div>""", unsafe_allow_html=True)
        if results.empty:
            st.info("No data yet.")
        else:
            daily = results[results["test_type"] == "daily_practice"].copy()
            if daily.empty:
                st.info("No daily practice sessions recorded yet.")
            else:
                daily["test_date"] = pd.to_datetime(daily["test_date"], errors="coerce")
                daily = daily.dropna(subset=["test_date"])

                def _streak(dates):
                    dates = sorted(set(dates.dt.date))
                    if not dates:
                        return 0
                    streak = cur = 1
                    for i in range(1, len(dates)):
                        if (dates[i] - dates[i - 1]).days == 1:
                            cur += 1
                            streak = max(streak, cur)
                        else:
                            cur = 1
                    return streak

                streak_lb = (
                    daily.groupby("username")["test_date"]
                    .apply(_streak)
                    .reset_index()
                )
                streak_lb.columns = ["username", "streak"]
                streak_lb = streak_lb.sort_values("streak", ascending=False).reset_index(drop=True)
                _lb_rows(streak_lb, "streak", val_fmt=lambda v: f"{int(v)} 🔥 days")

    # ── Tab 3: Daily Practice ─────────────────────────────────────────────────
    with tab3:
        st.markdown("""<div class="info-box">📅 <b>Daily Practice Leaderboard</b> — ranked by total points accumulated from daily_practice sessions only (results.csv, test_type = daily_practice).</div>""", unsafe_allow_html=True)
        if results.empty:
            st.info("No data yet.")
        else:
            daily_r = results[results["test_type"] == "daily_practice"]
            if daily_r.empty:
                st.info("No daily practice sessions yet.")
            else:
                dp_lb = (
                    daily_r.groupby("username")
                    .agg(total_pts=("score", "sum"), sessions=("score", "count"))
                    .reset_index()
                    .sort_values("total_pts", ascending=False)
                    .reset_index(drop=True)
                )
                _lb_rows(dp_lb, "total_pts",
                         val_fmt=lambda v: f"{int(v)} pts",
                         extra_cols=[("sessions", "Sessions")])

    # ── Tab 4: Subject — Physics ──────────────────────────────────────────────
    with tab4:
        st.markdown("""<div class="info-box">🔬 <b>Physics Leaderboard</b> — ranked by total challenge points earned in Physics challenges only (challenge_results.csv where subject = Physics).</div>""", unsafe_allow_html=True)
        if ch_results.empty:
            st.info("No challenge data yet.")
        else:
            phy = ch_results[ch_results["subject"].str.lower().str.contains("physics", na=False)]
            if phy.empty:
                st.info("No Physics challenge results yet.")
            else:
                phy_lb = (
                    phy.groupby("username")["score"]
                    .sum().reset_index()
                    .rename(columns={"score": "total_pts"})
                    .sort_values("total_pts", ascending=False)
                    .reset_index(drop=True)
                )
                _lb_rows(phy_lb, "total_pts", val_fmt=lambda v: f"{int(v)} pts")

    # ── Tab 5: Subject — Chemistry ────────────────────────────────────────────
    with tab5:
        st.markdown("""<div class="info-box">⚗️ <b>Chemistry Leaderboard</b> — ranked by total challenge points earned in Chemistry challenges only (challenge_results.csv where subject = Chemistry).</div>""", unsafe_allow_html=True)
        if ch_results.empty:
            st.info("No challenge data yet.")
        else:
            chem = ch_results[ch_results["subject"].str.lower().str.contains("chemistry", na=False)]
            if chem.empty:
                st.info("No Chemistry challenge results yet.")
            else:
                chem_lb = (
                    chem.groupby("username")["score"]
                    .sum().reset_index()
                    .rename(columns={"score": "total_pts"})
                    .sort_values("total_pts", ascending=False)
                    .reset_index(drop=True)
                )
                _lb_rows(chem_lb, "total_pts", val_fmt=lambda v: f"{int(v)} pts")

# ─────────────────────────────────────────────────────────────
#  PAGE: MISTAKE NOTEBOOK
# ─────────────────────────────────────────────────────────────
def page_mistake_notebook():
    st.markdown("## 📖 Mistake Notebook")
    user = st.session_state.user

    mistakes = load_csv("mistakes.csv")
    questions_df = load_csv("questions.csv")

    if mistakes.empty:
        st.success("🎉 No mistakes recorded yet. Keep up the perfect work!")
        return

    user_mistakes = mistakes[mistakes["username"] == user["username"]].copy()
    if user_mistakes.empty:
        st.success("🎉 No mistakes recorded for you yet!")
        return

    st.markdown(f"""<div class="info-box">📖 You have <strong>{len(user_mistakes)}</strong> recorded mistakes. Review them to improve!</div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        subj_opts = ["All"] + sorted(user_mistakes["subject"].unique().tolist())
        sel_subj = st.selectbox("Filter by Subject", subj_opts, key="mn_subj")
    with c2:
        show_bm = st.checkbox("Show Bookmarked Only", key="mn_bm")

    filtered = user_mistakes.copy()
    if sel_subj != "All":
        filtered = filtered[filtered["subject"] == sel_subj]
    if show_bm:
        filtered = filtered[filtered["bookmarked"].astype(str).str.lower() == "true"]

    if filtered.empty:
        st.info("No mistakes match your filter.")
        return

    for _, mistake in filtered.iterrows():
        try:
            qid = int(mistake["question_id"])
            if questions_df.empty:
                continue
            q_rows = questions_df[questions_df["id"].astype(int) == qid]
            if q_rows.empty:
                continue
            q = q_rows.iloc[0]
        except (ValueError, KeyError):
            continue

        opts = {"A": q["option_a"], "B": q["option_b"], "C": q["option_c"], "D": q["option_d"]}
        bm = str(mistake.get("bookmarked", "False")).lower() == "true"
        bm_icon = "🔖" if bm else "📌"

        with st.expander(f"{bm_icon} [{q['subject']} — {q['chapter']}] {str(q['question'])[:70]}"):
            st.markdown(f"""
            <div class="error-box"><b>Your Answer:</b> {mistake['student_answer']}. {opts.get(str(mistake['student_answer']),'?')}</div>
            <div class="success-box"><b>Correct Answer:</b> {q['correct_answer']}. {opts[q['correct_answer']]}</div>
            <div class="info-box"><b>💡 Explanation:</b> {q['explanation']}</div>
            """, unsafe_allow_html=True)

            ba, bb = st.columns(2)
            with ba:
                if st.button(f"{'🔖 Remove Bookmark' if bm else '📌 Bookmark'}", key=f"bm_{qid}_{user['username']}"):
                    df = load_csv("mistakes.csv")
                    mask = (df["username"] == user["username"]) & (df["question_id"].astype(int) == qid)
                    df.loc[mask, "bookmarked"] = not bm
                    save_csv(df, "mistakes.csv")
                    st.rerun()
            with bb:
                if st.button("🗑️ Remove", key=f"del_{qid}_{user['username']}"):
                    df = load_csv("mistakes.csv")
                    mask = (df["username"] == user["username"]) & (df["question_id"].astype(int) == qid)
                    df = df[~mask]
                    save_csv(df, "mistakes.csv")
                    st.rerun()

# ─────────────────────────────────────────────────────────────
#  PAGE: ADMIN PANEL
# ─────────────────────────────────────────────────────────────
def page_admin():
    if st.session_state.user.get("role") != "admin":
        st.error("⛔ Access Denied — Admins only.")
        return

    st.markdown("## ⚙️ Admin Control Panel")
    tabs = st.tabs(["📊 Overview", "➕ Add Question", "📋 Manage Questions", "👥 Students", "⚔️ Challenges"])

    # ── Overview
    with tabs[0]:
        results = load_csv("results.csv")
        students = load_csv("students.csv")
        questions_df = load_csv("questions.csv")

        c1, c2, c3, c4 = st.columns(4)
        stu_count = int((students["role"] == "student").sum()) if not students.empty else 0
        for col, val, label, clr in [
            (c1, stu_count, "👥 Students", "#6495ed"),
            (c2, len(results) if not results.empty else 0, "📝 Total Tests", "#32cd32"),
            (c3, len(questions_df) if not questions_df.empty else 0, "❓ Questions", "#ffa500"),
            (c4, f"{results['score'].mean():.1f}" if not results.empty else "N/A", "📈 Avg Score", "#9b59b6"),
        ]:
            with col:
                st.markdown(f"""<div class="metric-card"><div class="metric-value" style="color:{clr};">{val}</div><div class="metric-label">{label}</div></div>""", unsafe_allow_html=True)

        if not results.empty:
            CMAP = {"Physics": "#6495ed", "Chemistry": "#32cd32", "Mathematics": "#ffa500"}
            c_l, c_r = st.columns(2)
            with c_l:
                fig = px.histogram(results, x="score", color="subject", template="plotly_dark",
                                   title="Score Distribution", color_discrete_map=CMAP)
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
                st.plotly_chart(fig, use_container_width=True)
            with c_r:
                vc = results["subject"].value_counts().reset_index()
                vc.columns = ["subject", "count"]
                fig2 = px.pie(vc, names="subject", values="count", template="plotly_dark",
                              title="Tests by Subject", color_discrete_map=CMAP)
                fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
                st.plotly_chart(fig2, use_container_width=True)

    # ── Add Question
    with tabs[1]:
        st.markdown("### ➕ Add New Question")
        with st.form("add_q_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                nsubj = st.selectbox("Subject", ["Physics", "Chemistry", "Mathematics"])
            with c2:
                nchap = st.text_input("Chapter")
            nq = st.text_area("Question Text")
            c1, c2 = st.columns(2)
            with c1:
                oa = st.text_input("Option A")
                oc = st.text_input("Option C")
            with c2:
                ob = st.text_input("Option B")
                od = st.text_input("Option D")
            ca = st.selectbox("Correct Answer", ["A", "B", "C", "D"])
            exp = st.text_area("Explanation")
            diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
            submitted = st.form_submit_button("➕ Add Question", type="primary")

        if submitted:
            if all([nq, oa, ob, oc, od, exp, nchap]):
                df = load_csv("questions.csv")
                try:
                    new_id = int(pd.to_numeric(df["id"], errors="coerce").max()) + 1 if not df.empty else 1
                except Exception:
                    new_id = len(df) + 1
                new_row = pd.DataFrame([{
                    "id": new_id, "subject": nsubj, "chapter": nchap, "question": nq,
                    "option_a": oa, "option_b": ob, "option_c": oc, "option_d": od,
                    "correct_answer": ca, "explanation": exp, "difficulty": diff,
                }])
                save_csv(pd.concat([df, new_row], ignore_index=True), "questions.csv")
                st.success(f"✅ Question #{new_id} added successfully!")
            else:
                st.error("Please fill all fields.")

    # ── Manage Questions
    with tabs[2]:
        st.markdown("### 📋 Question Bank")
        df = load_csv("questions.csv")
        if df.empty:
            st.info("No questions yet.")
        else:
            fsubj = st.selectbox("Filter", ["All"] + sorted(df["subject"].unique().tolist()), key="mq_filt")
            disp = df if fsubj == "All" else df[df["subject"] == fsubj]
            st.dataframe(disp[["id","subject","chapter","question","correct_answer","difficulty"]], use_container_width=True, hide_index=True)
            st.markdown(f"**Total: {len(disp)} questions**")

            del_id = st.number_input("Delete question by ID", min_value=1, step=1, value=1, key="del_qid")
            if st.button("🗑️ Delete Question", type="secondary"):
                df2 = load_csv("questions.csv")
                df2 = df2[df2["id"].astype(int) != int(del_id)]
                save_csv(df2, "questions.csv")
                st.success(f"Deleted question #{del_id}.")
                st.rerun()

    # ── Students
    with tabs[3]:
        st.markdown("### 👥 Student Management")
        students = load_csv("students.csv")
        results = load_csv("results.csv")

        if not students.empty:
            stu_only = students[students["role"] == "student"]
            st.dataframe(stu_only[["username","name","email","joined_date"]], use_container_width=True, hide_index=True)

            st.markdown("#### 📊 Individual Student Report")
            stu_list = stu_only["username"].tolist()
            if stu_list:
                sel_stu = st.selectbox("Select student", stu_list, key="stu_sel")
                if not results.empty:
                    sr = results[results["username"] == sel_stu]
                    if not sr.empty:
                        c1, c2, c3 = st.columns(3)
                        total_c = sr["correct"].sum()
                        total_w = sr["incorrect"].sum()
                        acc = (total_c / (total_c + total_w) * 100) if (total_c + total_w) > 0 else 0
                        with c1: st.metric("Tests Taken", len(sr))
                        with c2: st.metric("Avg Score", f"{sr['score'].mean():.1f}")
                        with c3: st.metric("Accuracy", f"{acc:.1f}%")
                        st.dataframe(sr[["test_date","subject","chapter","score","correct","incorrect"]], use_container_width=True, hide_index=True)
                    else:
                        st.info("No test history for this student.")

        st.markdown("#### ➕ Add New Student")
        with st.form("add_stu_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                nu = st.text_input("Username")
                nn = st.text_input("Full Name")
            with c2:
                ne = st.text_input("Email")
                np_ = st.text_input("Password")
            add_stu = st.form_submit_button("➕ Add Student")

        if add_stu:
            if nu and nn and np_:
                df = load_csv("students.csv")
                if not df.empty and nu in df["username"].values:
                    st.error("Username already exists.")
                else:
                    new_row = pd.DataFrame([{
                        "username": nu, "password": np_, "name": nn,
                        "email": ne, "role": "student",
                        "joined_date": datetime.now().strftime("%Y-%m-%d"),
                    }])
                    save_csv(pd.concat([df, new_row], ignore_index=True), "students.csv")
                    st.success(f"✅ Student '{nn}' added!")
            else:
                st.error("Fill all required fields.")

    # ── Challenges
    with tabs[4]:
        st.markdown("### ⚔️ Create Challenge")
        with st.form("create_ch_form", clear_on_submit=True):
            c_title = st.text_input("Challenge Title")
            c1, c2 = st.columns(2)
            with c1:
                c_subj = st.selectbox("Subject", ["Physics", "Chemistry", "Mathematics", "All"])
                c_dur = st.number_input("Duration (minutes)", min_value=5, max_value=180, value=30)
            with c2:
                c_date = st.date_input("Start Date")
                c_time = st.time_input("Start Time")
            create_ch = st.form_submit_button("⚔️ Create Challenge", type="primary")

        if create_ch:
            if c_title:
                df = load_csv("challenges.csv")
                try:
                    new_id = int(pd.to_numeric(df["challenge_id"], errors="coerce").max()) + 1 if not df.empty else 1
                except Exception:
                    new_id = len(df) + 1
                new_ch = pd.DataFrame([{
                    "challenge_id": new_id, "title": c_title, "subject": c_subj,
                    "created_by": "admin", "created_date": datetime.now().strftime("%Y-%m-%d"),
                    "start_time": f"{c_date} {c_time}", "duration_minutes": c_dur,
                    "status": "upcoming", "max_participants": 100,
                }])
                save_csv(pd.concat([df, new_ch], ignore_index=True), "challenges.csv")
                st.success(f"✅ Challenge '{c_title}' created!")
            else:
                st.error("Enter a challenge title.")

        st.markdown("### 📋 Manage Existing Challenges")
        ch_df = load_csv("challenges.csv")
        if not ch_df.empty:
            st.dataframe(ch_df, use_container_width=True, hide_index=True)
            upd_id = st.number_input("Challenge ID to update", min_value=1, step=1, value=1, key="upd_ch_id")
            new_status = st.selectbox("New Status", ["upcoming", "active", "completed"], key="upd_status")
            if st.button("🔄 Update Status"):
                ch_df.loc[ch_df["challenge_id"].astype(int) == int(upd_id), "status"] = new_status
                save_csv(ch_df, "challenges.csv")
                st.success("✅ Status updated!")
                st.rerun()

# ─────────────────────────────────────────────────────────────
#  MAIN ROUTER
# ─────────────────────────────────────────────────────────────
def main():
    if not st.session_state.logged_in:
        render_login()
        return

    render_sidebar()
    page = st.session_state.page

    PAGE_MAP = {
        "Home": page_home,
        "Dashboard": page_dashboard,
        "Materials": page_materials,
        "Daily Practice": page_daily_practice,
        "Take Test": page_take_test,
        "Challenges": page_challenges,
        "Leaderboard": page_leaderboard,
        "Mistake Notebook": page_mistake_notebook,
        "Admin Panel": page_admin,
    }

    handler = PAGE_MAP.get(page, page_home)
    handler()

if __name__ == "__main__":
    main()
