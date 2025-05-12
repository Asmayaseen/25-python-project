import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- Config ---
st.set_page_config(page_title="GitHub Profile Scraper", page_icon="🕵️")

# --- CSS Styling ---
st.markdown("""
<style>
    .stTextInput>div>div>input {
        background-color: #f8f9fa;
        border: 1px solid #ced4da;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6e5494, #4078c0);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
    }
    .profile-card {
        border-radius: 15px;
        padding: 2rem;
        background: #f8f9fa;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- App ---
st.title("🕵️ GitHub Profile Scraper Pro")
st.markdown("Fetch profile images **AND** metadata using GitHub API + Web Scraping")

with st.expander("ℹ️ How to use"):
    st.write("""
    1. Enter any GitHub username
    2. Choose API or Web Scraping method
    3. Get profile image + extra details!
    """)

# Input
username = st.text_input("🔎 Enter GitHub Username", "Asmayaseen")
method = st.radio("Select Method:", ("API (Faster)", "Web Scraping (More Data)"))

if st.button("🚀 Fetch Profile"):
    if not username.strip():
        st.error("Please enter a valid username")
    else:
        with st.spinner(f"Fetching {username}'s data..."):
            try:
                if method == "API (Faster)":
                    # API Method
                    api_url = f"https://api.github.com/users/{username}"
                    response = requests.get(api_url, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        with st.container():
                            st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
                            
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                st.image(data['avatar_url'], width=200)
                            with col2:
                                st.subheader(data['name'] or username)
                                st.write(f"📌 {data['bio'] or 'No bio'}")
                                st.write(f"📍 {data['location'] or 'Unknown'}")
                                st.write(f"👥 Followers: {data['followers']} | Following: {data['following']}")
                                st.write(f"📦 Repos: {data['public_repos']}")
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.error(f"API Error: {response.status_code} - User not found")

                else:
                    # Web Scraping Method
                    url = f"https://github.com/{username}"
                    response = requests.get(url, timeout=10)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract data
                    avatar = soup.find("img", {"alt": "Avatar"})['src']
                    name = soup.find("span", {"itemprop": "name"}).text.strip() if soup.find("span", {"itemprop": "name"}) else username
                    bio = soup.find("div", {"class": "p-note"}).text.strip() if soup.find("div", {"class": "p-note"}) else "No bio"
                    
                    with st.container():
                        st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
                        
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.image(avatar, width=200)
                        with col2:
                            st.subheader(name)
                            st.write(f"📌 {bio}")
                            st.write(f"🔗 [View Full Profile]({url})")
                        
                        st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
    Made with ❤️ by [Asma Yaseen](https://github.com/Asmayaseen) | 
    [Report Issues](https://github.com/Asmayaseen/25-python-project/issues)
""")