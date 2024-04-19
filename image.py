import streamlit as st
import requests
import webbrowser
from io import BytesIO
from PIL import Image
from base64 import b64encode
import time

def caltime():
    st.session_state.start_time=time.time()
def stptime():
    if 'start_time' in st.session_state:
            elapsed_time = round(time.time() - st.session_state.start_time, 2)
            st.write(f"Results Generated in: {elapsed_time} seconds.")
            del st.session_state.start_time


def generate_image(prompt):
    import webbrowser
    # send query to Stable Diffusion  API and get the image back as a binary file
    response = requests.post(
        "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
        headers={"Authorization": "Bearer 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"},
        json={"inputs": prompt}
    )
    if response:
         stptime()

    
    img_data = response.content

    # Open the image using PIL
    img = Image.open(BytesIO(img_data))

    # to save file  on local machine
    img.save("generated_image.jpg")

    # to open  image in web browser (optional)
    url = "generated_image.jpg"
    webbrowser.open(url)
    

def main():
    st.title("Dynamo AI 🖼️")

    # Get the prompt
    prompt = st.text_input("Enter a prompt:")
    if prompt:
         caltime()
    # Generate an image based on the prompt
    if st.button("Generate Image"):
        generate_image(prompt)

if __name__ == "__main__":
    main()