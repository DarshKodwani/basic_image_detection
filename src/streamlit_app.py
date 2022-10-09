import streamlit as st
from streamlit_image_comparison import image_comparison
from analysis import run_ring_detection
import os
from PIL import Image
import cv2 
import numpy as np
import time

st.set_page_config("Caterpillar ring detector", "⚙️")

st.image(
    os.path.join(os.environ['REPO_ROOT'], "src/cat_acc1.png")
)

st.header("Ring detection")

st.write("")
"This app allows detection of rings for automated manufacturing quality assurance"
st.write("")

st.markdown("Ring vs no ring")
image_comparison(
    img1="src/ring.png",
    img2="src/no_ring.png",
    label1="ring",
    label2="no_ring",
)

uploaded_file = st.file_uploader("Upload Image")
if uploaded_file:
    with st.spinner('Thinking ...'):
        time.sleep(5)
        pil_image = Image.open(uploaded_file)
        rgb_pil_image = pil_image.convert('RGB')
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        st.image(pil_image, caption='Input', use_column_width=True)
        result = run_ring_detection(image)
        st.write("")
        f"{result[0]} :exclamation:"
        st.write("")

        st.markdown("Detected ring")

        image_comparison(
        img1=rgb_pil_image,
        img2="src/detected_circles_ring.png",
        label1="Original",
        label2="Detected circles",
        )
    st.success('Done!')