import streamlit as st
import requests

st.title("🕵️ GitHub Profile Image Scraper")
st.write("Enter a GitHub username to fetch the profile image using GitHub API.")

# Input for GitHub Username
username = st.text_input("🔎 Enter GitHub Username", "Asmayaseen")

if st.button("Fetch Profile Image"):
    try:
        # Validate username
        if not username:
            st.error("❗ Please enter a valid GitHub username.")
        else:
            # GitHub API URL
            api_url = f"https://api.github.com/users/{username}"
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                image_url = data.get("avatar_url")
                
                if image_url:
                    st.success("✅ Profile Image Found!")
                    st.image(image_url, caption=f"{username}'s GitHub Profile Picture", width=300)
                    st.write(f"📸 [View Image Directly]({image_url})")
                else:
                    st.error("❗ Profile image not found.")
            else:
                st.error(f"❗ Failed to fetch data. Status Code: {response.status_code}")
    except Exception as e:
        st.error(f"❗ An error occurred: {e}")

st.write("Made with ❤️ by Asma Yaseen")
