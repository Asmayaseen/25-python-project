import os
import streamlit as st

def rename_files(folder_path, prefix, suffix, extension):
    if not os.path.isdir(folder_path):
        st.error("Invalid folder path. Please enter a valid directory.")
        return

    files = os.listdir(folder_path)
    if not files:
        st.warning("No files found in the directory.")
        return

    renamed_count = 0

    for index, file in enumerate(files, start=1):
        file_path = os.path.join(folder_path, file)

        if os.path.isfile(file_path):
            new_name = f"{prefix}{index}{suffix}.{extension}"
            new_path = os.path.join(folder_path, new_name)
            os.rename(file_path, new_path)
            renamed_count += 1

    st.success(f"Successfully renamed {renamed_count} files.")

# Streamlit UI
st.title("📝 Bulk File Renamer")
st.write("Easily rename all files in a folder based on your preferences.")

folder_path = st.text_input("📁 Enter the folder path:")
prefix = st.text_input("🔤 Enter filename prefix (optional):", "File_")
suffix = st.text_input("🖋️ Enter filename suffix (optional):", "")
extension = st.text_input("📄 Enter file extension (e.g., txt, jpg, png):")

if st.button("🔎 Preview Files"):
    if os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        st.write("### Files in Directory:")
        st.write(files if files else "No files found.")
    else:
        st.error("Invalid folder path. Please enter a valid directory.")

if st.button("🚀 Rename Files"):
    if extension.strip() == "":
        st.error("Please provide a file extension.")
    else:
        rename_files(folder_path, prefix, suffix, extension)

st.markdown("---")
st.markdown("Made with ❤️ by Asma Yaseen")
