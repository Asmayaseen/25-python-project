import streamlit as st # type: ignore
import qrcode # type: ignore
from PIL import Image # type: ignore
import cv2 # type: ignore
import numpy as np # type: ignore

st.set_page_config(page_title="QR Code Encoder/Decoder 🧡", page_icon="🧡")
st.title("QR Code Encoder & Decoder 🛠️")

# Sidebar Navigation
menu = st.sidebar.radio("Choose an option", ["Encode QR Code 🖼️", "Decode QR Code 🔎"])

if menu == "Encode QR Code 🖼️":
    st.subheader("Generate Your QR Code 🧾")
    data = st.text_input("Enter the data to encode into QR Code:")

    if st.button("Generate QR Code 🧙‍♂️"):
        if data.strip():
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color="white")
            img.save("qrcode.png")

            # Convert PIL image to bytes for Streamlit
            import io
            img_byte_array = io.BytesIO()
            img.save(img_byte_array, format='PNG')
            img_byte_array = img_byte_array.getvalue()

            st.image(img_byte_array, caption="Your QR Code 🖼️", use_container_width=True)
            st.success("QR Code Generated Successfully! ✅")

            with open("qrcode.png", "rb") as file:
                st.download_button(
                    label="Download QR Code 📥", 
                    data=file, 
                    file_name="qrcode.png", 
                    mime="image/png"
                )
        else:
            st.warning("Please enter data to generate QR Code! ⚠️")

elif menu == "Decode QR Code 🔎":
    st.subheader("Decode a QR Code 📥")
    uploaded_file = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded QR Code 🖼️", use_container_width=True)

        # Convert image to numpy array
        image_np = np.array(image)
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(gray)

        if data:
            st.success(f"Decoded Data: {data} 🥳")
        else:
            st.error("No QR code detected. Please upload a valid image! 🚫")

st.sidebar.info("Developed with 💖 using Streamlit")
