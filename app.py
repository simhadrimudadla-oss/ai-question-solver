import os
import base64
import streamlit as st
import openai
from PIL import Image
import io
import numpy as np
import cv2
import pytesseract


# ---------------- API KEY ----------------
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

if not api_key:
    st.error("OPENAI_API_KEY not found. Please set it in Command Prompt.")
    st.stop()


# ---------------- UI ----------------
st.set_page_config(page_title="AI Question Solver Bot", page_icon="🤖")
st.title("AI Question Solver Bot 🤖")
st.write("Ask a question or upload an image containing a question.")

option = st.radio("Choose input type:", ["Text Question", "Image Upload"])

user_question = ""
uploaded_image = None

# ---------------- TEXT INPUT ----------------
if option == "Text Question":
    user_question = st.text_input("Enter your question")

# ---------------- IMAGE INPUT (VISION) ----------------
elif option == "Image Upload":
    uploaded_image = st.file_uploader(
        "Upload an image (JPG / PNG)",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_container_width=True)

# ---------------- SOLVE BUTTON ----------------
if st.button("Solve"):
    if option == "Text Question" and not user_question.strip():
        st.warning("Please enter a question.")
        st.stop()

    if option == "Image Upload" and uploaded_image is None:
        st.warning("Please upload an image.")
        st.stop()

    try:
        with st.spinner("Thinking... 🤔"):

            # ---------- TEXT MODE ----------
            if option == "Text Question":
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "Explain answers step by step for grade 3 students using simple language."
                        },
                        {
                            "role": "user",
                            "content": user_question
                        }
                    ]
                )

            # ---------- IMAGE MODE (VISION) ----------
            else:
                image_bytes = uploaded_image.getvalue()
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "Explain the answer step by step for a grade 3 student."
                        },
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Please solve the question shown in this image."},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{image_base64}"
                                    }
                                }
                            ]
                        }
                    ]
                )

        answer = response.choices[0].message["content"]
        st.subheader("AI Answer")
        st.write(answer)

    except Exception as e:
        st.error("❌ Unable to get response from AI.")
        st.info("This may happen if billing is not enabled or quota is exhausted.")
        st.code(str(e))





