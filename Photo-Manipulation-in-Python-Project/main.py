import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter

st.set_page_config(page_title="Photo Manipulation 🖼️", page_icon="🖼️")
st.title("Photo Manipulation App by Asma Yaseen 🖼️✨")
st.write("Upload your image and apply filters like brightness, contrast, and blur!")

# Upload Image
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Original Image", use_container_width=True)

    # Operation Selection
    st.subheader("🎨 Choose an Operation")
    operation = st.radio(
        "Select an operation:",
        ("None", "Blur", "Brighten", "Darken", "Increase Contrast", "Decrease Contrast", "Edge Detection"),
        index=0
    )

    if operation == "Blur":
        blur_radius = st.slider("Blur Intensity", 0.0, 10.0, 1.0)
        image = image.filter(ImageFilter.GaussianBlur(blur_radius))

    elif operation == "Brighten":
        brightness_factor = st.slider("☀️ Brightness Factor", 1.0, 3.0, 1.5)
        image = ImageEnhance.Brightness(image).enhance(brightness_factor)

    elif operation == "Darken":
        brightness_factor = st.slider("🌑 Darkness Factor", 0.1, 1.0, 0.5)
        image = ImageEnhance.Brightness(image).enhance(brightness_factor)

    elif operation == "Increase Contrast":
        contrast_factor = st.slider("📈 Contrast Factor", 1.0, 3.0, 1.5)
        image = ImageEnhance.Contrast(image).enhance(contrast_factor)

    elif operation == "Decrease Contrast":
        contrast_factor = st.slider("📉 Contrast Factor", 0.1, 1.0, 0.5)
        image = ImageEnhance.Contrast(image).enhance(contrast_factor)

    elif operation == "Edge Detection":
        image = image.convert("L").filter(ImageFilter.FIND_EDGES)

    # Display Processed Image
    st.subheader("🛠️ Processed Image")
    st.image(image, caption="Enhanced Image", use_container_width=True)

    # Download Option
    img_byte_arr = image.tobytes()
    st.sidebar.download_button(
        label="Download Enhanced Image 📥",
        data=img_byte_arr,
        file_name="enhanced_image.png",
        mime="image/png"
    )

st.sidebar.info("Developed with 💖 by Asma Yaseen using Streamlit and PIL")