import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import requests
from io import BytesIO

# Load the trained model
model = tf.keras.models.load_model('ava_fooddrink_prediction.h5')

# Define the preprocessing function
def preprocess_image(image):
    # Resize the image to the required input shape
    image = image.resize((299, 299))
    # Convert the image to a numpy array
    image = np.array(image)
    # Scale the pixel values to be between 0 and 1
    image = image / 255.0
    # Convert the image to RGB format
    if image.shape[-1] == 4:
        image = image[..., :3]
    return image

# Define the predict function
def predict_aesthetic_score(image):
    # Preprocess the image
    preprocessed_image = preprocess_image(image)
    # Make the prediction
    score = model.predict(np.expand_dims(preprocessed_image, axis=0))[0][0]
    return score

st.set_page_config(
    page_title = "Aesthetic Score Predictor",
    page_icon = "unicorn_face",
    layout = "wide"
    )
header = st.container()
with header:
    st.title('Measure Aesthetic Score of Your Image')
st.sidebar.image("/Users/user/Desktop/Projects/CMSE890 - AML/image/streamlit_image.png", use_column_width=True) ## replace
st.sidebar.subheader("**_Welcome to the Aesthetic Score Predictor!_**")
st.sidebar.markdown("""This app that tells you how gorgeous your images really are!
                    Our AI-powered model can predict the aesthetic score of any image you throw at it.   
                    With scores ranging from `0` to `10`, it's like having your very own personal art critic.  
                    **_:orange[So why not give it a try?]_** Upload your images or use an image URL 
                    and see just how beautiful your shots really are.  
                    Get ready to unleash your inner artist and have a blast with our app!""")
st.sidebar.info("Read[Github]().", icon="ℹ️") #icon = "")
st.sidebar.info("Contact: [celine.yim95@gmail.com]", icon="✉️") # icon = ":email:")

tab_predictor, tab_url = st.tabs(["Uploader", "Using Image URL"])
    
with tab_predictor:
    uploaded_file = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        # Load the image from the uploaded file
        try: 
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            score = predict_aesthetic_score(image)
            # Display the predicted score to the user
            st.write('Aesthetic score:', score)
            st.balloons()
        except: 
            st.error("The file you uploaded does not seem to be a valid image. Try uploading a png or jpg file (Limit 200MB).")
        
        if st.session_state.get("image_url") not in ["", None]:
            st.warning("To use the file uploader, remove the image URL first.")


with tab_url:
    url = st.empty().text_input("Image URL", key="image_url")
    if url is not None:
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption='Uploaded Image', use_column_width=True)
            score = predict_aesthetic_score(image)
            # Display the predicted score to the user
            st.write('Aesthetic score:', score)
            st.balloons() 
        except:
            st.error("The URL does not seem to be valid.")