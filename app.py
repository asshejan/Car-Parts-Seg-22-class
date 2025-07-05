import streamlit as st
from PIL import Image
import numpy as np
import cv2
from ultralytics import YOLO

# Load YOLO model once
@st.cache_resource
def load_model():
    model = YOLO("best.pt")  # path to your fine-tuned model
    return model

model = load_model()

st.title("Car Parts Segmentation")

uploaded_file = st.file_uploader("Upload a car image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)

    # Run prediction
    results = model.predict(source=np.array(image), save=False)

    # Visualize segmentation result
    result = results[0]

    # Get image with masks overlaid
    im_array = result.plot()      # This returns a numpy array image

    # Convert to RGB for display
    im_rgb = cv2.cvtColor(im_array, cv2.COLOR_BGR2RGB)
    st.image(im_rgb, caption="Segmented Image", use_column_width=True)

    # Optional: Display classes and confidence scores
    st.subheader("Detected Classes")
    for box in result.boxes:
        class_id = int(box.cls[0])
        conf = float(box.conf[0])
        st.write(f"Class {class_id}: Confidence {conf:.2f}")
