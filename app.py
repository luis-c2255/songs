import streamlit as st
from data import rankings_data

st.set_page_config(page_title="Music Rankings", layout="wide")

def apply_cyberpunk_style():
    st.markdown('<link href="https://fonts.googleapis.com/css2?family=Stalinist+One&display=swap" rel="stylesheet">', unsafe_allow_html=True)
    st.markdown("""
        <style>
        /* Background */
        .stApp {
            background-color: #0A1A2F;
        }
        

        /* Main title glow */
        h1 {
            color: #00fff9;
            text-shadow: 0 0 10px #00fff9, 0 0 20px #00fff9;
            font-family: 'Stalinist One', sans-serif;
            text-align: center;
        }

        /* Subtitles */
        h2, h3 {
            color: #ff2079;
            text-shadow: 0 0 8px #ff2079;
            font-family: 'Courier New', monospace;
            text-align: center;
        }

        /* Regular text */
        p, div, label {
            color: #c0c0c0;
            font-family: 'Courier New', monospace;
        }

        /* Buttons */
        div.stButton > button {
            background-color: #0a0a0f;
            color: #00fff9;
            border: 2px solid #00fff9;
            box-shadow: 0 0 12px #00fff9;
            font-family: 'Courier New', monospace;
            border-radius: 12px;
            padding: 40px 20px;
            font-size: 30px;
            width: 100%;
        }

        div.stButton > button:hover {
            background-color: rgba(255, 0, 144, 0.6);
            color: #0A1A2A;
        }
        </style>
    """, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_month" not in st.session_state:
    st.session_state.selected_month = None
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

months = [
    "January", "February", "March", "April", "May",
    "June", "July", "August", "September", "October",
    "November", "December"
]
category = ["🎵 Songs", "🎤 Artists", "🎸 Genres"]
category_keys = {"🎵 Songs": "Songs", "🎤 Artists": "Artists", "🎸 Genres": "Genres"}

def show_home():
    st.markdown('<h1 style="font-family: \'Stalinist One\', cursive; font-size: 4rem; text-align: center; color: #00fff9; text-shadow: 0 0 13px #FF0090, 0 0 25px #DF73FF;">🎵 Music Rankings</h1>', unsafe_allow_html=True)
    st.markdown("<h3 style='font-family: \'Courier New\', monospace; text-align: center;'> Select a month to see its rankings:</h3>", unsafe_allow_html=True)
    st.write("---")
    if st.button("📊 Year Summary", width="stretch"):
        st.session_state.page = "summary"
        st.rerun()
    if st.button("➕ Add Month Data", use_container_width=True):
        st.session_state.page = "add_data"
        st.rerun()
    st.write(" ")

    cols = st.columns(4)

    for i, month in enumerate(months):
        col = cols[i % 4]
        with col:
            if st.button(month, key=month, width="stretch"):
                st.session_state.selected_month = month
                st.session_state.page = "month"
                st.rerun()

def show_month():
    month = st.session_state.selected_month
    st.markdown(f'<h1 style="font-family: \'Stalinist One\', cursive; text-align: center; color: #00fff9; text-shadow: 0 0 13px #FF0090, 0 0 25px #DF73FF;">📅 {month}</h1>', unsafe_allow_html=True)
    st.markdown("<h3 style='font-family: \'Courier New\', monospace; text-align: center;'> What would you like to see?</h3>", unsafe_allow_html=True)
    st.write("---")

    st.markdown("""
        <style>
        .category-card {
            background-color: #1e1e2e;
            border: 1px solid #444;
            border-radius: 12px;
            padding: 30px 20px;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="category-card">🎵<br>Songs</div>', unsafe_allow_html=True)
        if st.button("Open Songs", key="btn_songs", use_container_width=True):
            st.session_state.selected_category = "Songs"
            st.session_state.page = "ranking"
            st.rerun()

    with col2:
        st.markdown('<div class="category-card">🎤<br>Artists</div>', unsafe_allow_html=True)
        if st.button("Open Artists", key="btn_artists", use_container_width=True):
            st.session_state.selected_category = "Artists"
            st.session_state.page = "ranking"
            st.rerun()

    with col3:
        st.markdown('<div class="category-card">🎸<br>Genres</div>', unsafe_allow_html=True)
        if st.button("Open Genres", key="btn_genres", use_container_width=True):
            st.session_state.selected_category = "Genres"
            st.session_state.page = "ranking"
            st.rerun()

    st.write("---")
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def show_ranking():
    month = st.session_state.selected_month
    category = st.session_state.selected_category

    st.markdown(f'<h1 style="font-family: \'Stalinist One\', cursive; text-align: center; color: #00fff9; text-shadow: 0 0 13px #FF0090, 0 0 25px #DF73FF;">📊 {month} — {category}</h1>', unsafe_allow_html=True)
    st.write("---")

    if month not in rankings_data:
        st.warning(f"No data available for {month} yet. Use the Add Data page to add it!")
        if st.button("⬅️ Back"):
            st.session_state.page = "month"
            st.rerun()
        return
    items = rankings_data[month][category]

    st.subheader("🏆 Top 3")
    medals = ["🥇", "🥈", "🥉"]
    top3_cols = st.columns(3)

    for i in range(3):
        with top3_cols[i]:
            item = items[i]
            st.image(item["image"], width=200)
            st.markdown(f"### {medals[i]} {item['name']}")
            label = "times listened" if category == "Songs" else "min"
            st.markdown(f"⏱️ **{item['minutes']} {label}**")

    st.write("---")

    # --- POSITIONS 4-10 ---
    st.subheader("📋 Positions 4–10")
    for i in range(3, 10):
        item = items[i]
        col1, col2, col3 = st.columns([0.5, 3, 1.5])
        with col1:
            st.markdown(f"### {i+1}")
        with col2:
            st.image(item["image"], width=90)
            st.markdown(f"**{item['name']}**")
        with col3:
            label = "times listened" if category == "Songs" else "min"
            st.markdown(f"⏱️ {item['minutes']} {label}")
        st.write("---")

    # --- BACK BUTTONS ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Month"):
            st.session_state.page = "month"
            st.rerun()
    with col2:
        if st.button("🏠 Back to Home"):
            st.session_state.page = "home"
            st.rerun()

# --- SUMMARY PAGE ---
def show_summary():
    st.markdown('<h1 style="font-family: \'Stalinist One\', cursive; text-align: center; color: #00fff9; text-shadow: 0 0 13px #FF0090, 0 0 25px #DF73FF;">📊 Year Summary</h1>', unsafe_allow_html=True)
    st.markdown("<h3 style='font-family: \'Courier New\', monospace; text-align: center;'> Your top music across all months combined.</h3>", unsafe_allow_html=True)
    st.write("---")

    # Add up minutes for each item across all months
    totals = {"Songs": {}, "Artists": {}, "Genres": {}}

    for month, categories in rankings_data.items():
        for category, items in categories.items():
            for item in items:
                name = item["name"]
                mins = item["minutes"]
                image = item["image"]
                if name not in totals[category]:
                    totals[category][name] = {"minutes": 0, "image": image}
                totals[category][name]["minutes"] += mins

    # For each category, sort and display
    medals = ["🥇", "🥈", "🥉"]
    category_emojis = {"Songs": "🎵", "Artists": "🎤", "Genres": "🎸"}

    for category in ["Songs", "Artists", "Genres"]:
        st.subheader(f"{category_emojis[category]} Top {category}")

        # Sort by total minutes
        sorted_items = sorted(
            totals[category].items(),
            key=lambda x: x[1]["minutes"],
            reverse=True
        )[:10]

        # Top 3
        top3_cols = st.columns(3)
        for i in range(3):
            name, data = sorted_items[i]
            with top3_cols[i]:
                st.image(data["image"], width=100)
                st.markdown(f"### {medals[i]} {name}")
                label = "times listened" if category == "Songs" else "min"
                st.markdown(f"⏱️ **{data['minutes']} {label}**")

        st.write(" ")

        # Positions 4-10
        for i in range(3, 10):
            name, data = sorted_items[i]
            col1, col2, col3 = st.columns([0.5, 3, 1.5])
            with col1:
                st.markdown(f"### {i+1}")
            with col2:
                st.image(data["image"], width=50)
                st.markdown(f"**{name}**")
            with col3:
                label = "times listened" if category == "Songs" else "min"
                st.markdown(f"⏱️ {data['m']} {label}")
            st.write("---")

        st.write("---")

    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# --- ADD DATA PAGE ---
def show_add_data():
    st.markdown('<h1 style="font-family: \'Stalinist One\', cursive; text-align: center; color: #00fff9; text-shadow: 0 0 13px #FF0090, 0 0 25px #DF73FF;">➕ Add Month Data</h1>', unsafe_allow_html=True)
    st.markdown("<h3 style='font-family: \'Courier New\', monospace; text-align: center;'> Fill in the rankings for a new month.</h3>", unsafe_allow_html=True)
    st.write("---")

    month = st.selectbox("Select a month", months)

    st.write(" ")
    st.subheader("🎵 Songs")
    songs = []
    for i in range(10):
        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            name = st.text_input(f"Song #{i+1} name", key=f"song_name_{i}")
        with col2:
            mins = st.number_input(f"Times listened", min_value=0, key=f"song_mins_{i}")
        with col3:
            uploaded = st.file_uploader(f"Song #{i+1} image", type=["png", "jpg", "jpeg"], key=f"song_img_{i}")
        image = f"https://picsum.photos/seed/ns{i}/100/100"
        songs.append({"name": name, "times": mins, "image": image, "uploaded": uploaded})
    st.write(" ")
    st.subheader("🎤 Artists")
    artists = []
    for i in range(10):
        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            name = st.text_input(f"Artist #{i+1} name", key=f"artist_name_{i}")
        with col2:
            mins = st.number_input(f"Minutes", min_value=0, key=f"artist_mins_{i}")
        with col3:
            uploaded = st.file_uploader(f"Artist #{i+1} image", type=["png", "jpg", "jpeg"], key=f"artist_img_{i}")
        image = f"https://picsum.photos/seed/ns{i}/100/100"
        artists.append({"name": name, "minutes": mins, "image": image, "uploaded": uploaded})
    
    st.write(" ")
    st.subheader("🎸 Genres")
    genres = []
    for i in range(10):
        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            name = st.text_input(f"Genre #{i+1} name", key=f"genre_name_{i}")
        with col2:
            mins = st.number_input(f"Minutes", min_value=0, key=f"genre_mins_{i}")
        with col3:
            uploaded = st.file_uploader(f"Genre #{i+1} image", type=["png", "jpg", "jpeg"], key=f"genre_img_{i}")
        image = f"https://picsum.photos/seed/ns{i}/100/100"
        genres.append({"name": name, "minutes": mins, "image": image, "uploaded": uploaded})
    
    st.write("---")
    if st.button("✅ Submit", use_container_width=True):
        # Process uploaded images for songs
        for item in songs:
            if item["uploaded"] is not None:
                item["image"] = item["uploaded"]
            del item["uploaded"]

        # Process uploaded images for artists
        for item in artists:
            if item["uploaded"] is not None:
                item["image"] = item["uploaded"]
            del item["uploaded"]

        # Process uploaded images for genres
        for item in genres:
            if item["uploaded"] is not None:
                item["image"] = item["uploaded"]
            del item["uploaded"]

        rankings_data[month] = {
            "Songs": songs,
            "Artists": artists,
            "Genres": genres
        }
        st.success(f"✅ {month} data saved successfully!")

    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# --- ROUTER (decides which page to show) ---
apply_cyberpunk_style()
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "month":
    show_month()
elif st.session_state.page == "ranking":
    show_ranking()
elif st.session_state.page == "summary":
    show_summary()
elif st.session_state.page == "add_data":
    show_add_data()