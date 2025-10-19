import streamlit as st
import gemini_api

st.title("AI Fashion Styler")


# UI Components

# Top Garment
st.header("Top Garment")
top_garment_type = st.selectbox(
    "Top Garment Type",
    ["blouse", "t-shirt", "shirt", "crop-top", "tank-top", "kurti"]
)
top_fabric_image = st.file_uploader("Upload Top Fabric", type=["png", "jpg", "jpeg"])

# Lower Garment
st.header("Lower Garment")
lower_garment_type = st.selectbox(
    "Lower Garment Type",
    ["saree", "lehenga", "jeans", "skirt", "pants", "shorts"]
)
lower_fabric_image = st.file_uploader("Upload Lower Fabric", type=["png", "jpg", "jpeg"])


# 2. Model Upload
model_image = st.file_uploader("Upload Model/Mannequin Image", type=["png", "jpg", "jpeg"])

# 3. Styling Prompt
prompt = st.text_area("Enter a detailed description of the outfit you want to create.")


# Generate Button
if st.button("Generate Style"):
    if top_fabric_image and lower_fabric_image and model_image and prompt:
        st.write("Generating your styled outfit...")
        
        full_prompt = f"Create a high-resolution, photorealistic image of a model wearing a {top_garment_type} and {lower_garment_type}. The {top_garment_type} should be made from the provided top fabric image, and the {lower_garment_type} should be made from the provided lower fabric image. {prompt}. The model's face in the output image must be the same as in the provided model image. The final image should be clear, professionally lit, and look like a fashion photograph."

        # Call the Gemini API function
        generated_image = gemini_api.generate_image(
            fabric_image=top_fabric_image,
            model_image=model_image,
            prompt=full_prompt,
            fabric_image_2=lower_fabric_image
        )

        

        if generated_image:

            st.image(generated_image, caption="Your AI Styled Outfit", use_column_width=True)

            generated_image.seek(0)
            st.download_button(
                label="Download Image",
                data=generated_image,
                file_name="styled_outfit.png",
                mime="image/png"
            )

        else:

            st.error("Failed to generate image. Please check the console for errors.")

    else:

        st.warning("Please upload a top fabric image, a lower fabric image, a model image, and enter a prompt.")
