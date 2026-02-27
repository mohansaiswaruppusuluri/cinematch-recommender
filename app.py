import streamlit as st
import pickle
import pandas as pd
import os
import gdown

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMaexittch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e0d5;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(220,80,40,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(180,40,80,0.14) 0%, transparent 60%),
        #0a0a0f;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }
footer { display: none; }
#MainMenu { display: none; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #dc5028;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4rem, 10vw, 9rem);
    line-height: 0.92;
    letter-spacing: 0.04em;
    background: linear-gradient(135deg, #fff 30%, #dc5028 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1rem;
    color: rgba(232,224,213,0.5);
    margin-top: 1rem;
    font-weight: 300;
    letter-spacing: 0.02em;
}

/* ── Divider ── */
.divider {
    width: 60px; height: 2px;
    background: linear-gradient(90deg, #dc5028, transparent);
    margin: 2rem auto;
}

/* ── Select box override ── */
[data-testid="stSelectbox"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
    color: rgba(232,224,213,0.45) !important;
    font-weight: 500 !important;
}

[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 4px !important;
    color: #e8e0d5 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stSelectbox"] > div > div:hover {
    border-color: rgba(220,80,40,0.5) !important;
}
[data-testid="stSelectbox"] svg { fill: #dc5028 !important; }

/* ── Button ── */
[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #dc5028 0%, #b83060 100%) !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 24px rgba(220,80,40,0.25) !important;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Movie cards ── */
.cards-heading {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: rgba(232,224,213,0.4);
    text-align: center;
    margin-bottom: 1.5rem;
}

.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 1.6rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.25s, border-color 0.25s, background 0.25s;
    height: 100%;
}
.card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(220,80,40,0.06) 0%, transparent 60%);
    opacity: 0;
    transition: opacity 0.25s;
}
.card:hover {
    transform: translateY(-4px);
    border-color: rgba(220,80,40,0.35);
    background: rgba(255,255,255,0.07);
}
.card:hover::before { opacity: 1; }

.card-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    line-height: 1;
    color: rgba(220,80,40,0.2);
    position: absolute;
    top: 0.8rem;
    right: 1rem;
    letter-spacing: 0.04em;
}
.card-label {
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #dc5028;
    font-weight: 500;
    margin-bottom: 0.5rem;
}
.card-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 500;
    color: #e8e0d5;
    line-height: 1.35;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #dc5028 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: rgba(220,80,40,0.4); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Model loading ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_data():
    if not os.path.exists("similarity.pkl"):
        url = "https://drive.google.com/uc?id=1dC4PDTs-3qEE_mRU15EXrR_MHktgfqKH"
        gdown.download(url, "similarity.pkl", quiet=False)

    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()


# ── Recommend function (unchanged) ─────────────────────────────────────────────
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies


# ── Hero section ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ AI-Powered Discovery</div>
    <div class="hero-title">CineMatch</div>
    <div class="hero-sub">Tell us one movie. We'll find your next five.</div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Controls ────────────────────────────────────────────────────────────────────
col_l, col_mid, col_r = st.columns([1, 2, 1])
with col_mid:
    selected_movie_name = st.selectbox(
        "Choose a movie you love",
        movies['title'].values,
        index=None,
        placeholder="Search for a movie..."
    )
    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    find_btn = st.button("Find Recommendations ›")


# ── Results ─────────────────────────────────────────────────────────────────────
if find_btn:
    if not selected_movie_name:
        st.markdown("""
        <div style='text-align:center; color:rgba(220,80,40,0.8); font-size:0.85rem;
                    letter-spacing:0.1em; padding:1rem;'>
            ↑ Please select a movie first
        </div>""", unsafe_allow_html=True)
    else:
        with st.spinner("Finding your matches..."):
            recommendations = recommend(selected_movie_name)

        st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="cards-heading">
            Recommended because you liked &nbsp;<span style='color:#dc5028'>{selected_movie_name}</span>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(5, gap="small")
        for idx, (col, title) in enumerate(zip(cols, recommendations)):
            with col:
                st.markdown(f"""
                <div class="card">
                    <div class="card-number">{str(idx+1).zfill(2)}</div>
                    <div class="card-label">Pick #{idx+1}</div>
                    <div class="card-title">{title}</div>
                </div>
                """, unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 4rem 1rem 2rem;
            color: rgba(232,224,213,0.2); font-size:0.7rem; letter-spacing:0.15em;'>
    CINEMATCH &nbsp;·&nbsp; CONTENT-BASED FILTERING &nbsp;·&nbsp; TMDB DATASET
</div>
""", unsafe_allow_html=True)