from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from PIL import Image
import os
import io
import base64
import google.generativeai as genai
import pdf2image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel("gemini-2.0-flash-lite")
    response=model.generate_content([prompt,pdf_content[0],input])
    return response.text
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


#strealit app
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking system")
input_text=st.text_area("Job description",key="input")
uploaded_file=st.file_uploader("Upload your Resume in PDF",type=["pdf"])

if uploaded_file is not None:
    print("File Uploaded sucesfuly")

submit1=st.button("Tell me about my resume")
submit2=st.button("How can I improvise my skills")
submit3=st.button("What are the keywords that are missing")
submit4=st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt4 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt2 = """
 You are an experienced data scientist having deep understanding of data science, machine larming, deep learning, computer vision, genai, llm, web development. 
 your task is to share your professional evaluation for the provided resume against the given job description and 
 guide the candidate how to  improvise the required skils mentioned in job description.
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to highlight the missing keywords in the provided resume  against the provided job description and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
elif submit4:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")