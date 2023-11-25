import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import openai
import os
import math
import json


# Initialize session state variables if not already set
if 'final_output_text' not in st.session_state:
    st.session_state.final_output_text = None

# response = openai.chat.completions.create(
#     model="gpt-4",
#     messages=[
#         {"role": "system", "content": "You are a 5 year old"},
#         {"role": "user", "content": "what is pi"},
#     ] 
# )

def load_LLM(openai_api_key):
    openai.api_key = openai_api_key


def load_LLM2(openai_api_key):
    openai.api_key = openai_api_key
    # return llm3
def load_LLM3(openai_api_key):
    openai.api_key = openai_api_key
def load_LLM4(openai_api_key):
    openai.api_key = openai_api_key
    
#JSON file
json_file_path = 'convo.json'

def read_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)


# Function to generate prompt for Bot 1 (Alice)
def SPRCompressorGenerator(user_input):
    prompt = f""" # MISSION
You are a Sparse Priming Representation (SPR) writer. You will be given information by the USER here: {user_input},  which you are to render as an SPR.
Create a Sparse Primitive Representation of this technical document, which is a code walkthrough. Focus on summarizing the key functions of each code block, explaining the main algorithms, and their practical applications. Aim for a concise yet comprehensive overview that captures the essence of the document's coding content, suitable for readers with basic coding knowledge.
If not a coding or technical topic, Render the input as a distilled list of succinct statements, assertions, associations, concepts, analogies, and metaphors. The idea is to capture as much, conceptually, as possible but with as few words as possible. Write it in a way that makes sense to you, as the future audience will be another language model, not a human. Use complete sentences.

    In Op only provide the SPR output.
"""
    messages=[]
    messages.append({"role": "user", "content": prompt})
        # Make the API call
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages
    )

    # Extract the response
    SPRCompressor = response.choices[0].message["content"]
    return SPRCompressor

    
# Define details for each category
category_details = {
    'Case Study': 'Purpose: Generate a comprehensive case study on a specified topic. Structure: Introduction, background, solutions, results, key takeaways. Data: Include data points, graphs, citations. Process: Outline, contextualize, detail issues, explain solutions, present results, summarize takeaways, add citations.',
    'Onboarding': 'Purpose: Create an onboarding guide for a specific role or department. Elements: Company culture, job functions, key contacts, tools, platforms. Process: Structure guide, introduce company, enumerate job functions, list contacts, discuss tools.',
    'Standard Procedures': 'Purpose: Outline standard procedures for a specific task or process. Content: Objectives, prerequisites, step-by-step actions, warnings, precautions. Process: List objectives, prerequisites, detail steps, insert warnings.',
    'Code Walkthrough': 'Purpose: Conduct a code walkthrough for a specific programming task or project. Content: Code snippets, explanations, best practices. Process: Overview of project, include code snippets, explain functionality, discuss best practices.',
    'How-To Videos': 'Purpose: Script a how-to video for a particular task, skill, or process. Structure: Introduction, materials, step-by-step guide, key takeaways. Process: Write introduction, list materials, create narrative, conclude with takeaways.',
    'Cheat Sheets': 'Purpose: Create a cheat sheet for a skill, tool, or process. Content: Tips, shortcuts, essential commands. Process: Compile tips and shortcuts, add commands, organize for quick reference.',
    'Masterclass': 'Purpose: Structure a masterclass on a specific topic or area of expertise. Elements: Learning objectives, in-depth modules, practical exercises, further learning resources. Process: Outline objectives, develop modules, include exercises, list additional resources.',
    'Story': 'Purpose: Write a compelling story. Elements: Engaging plot, character development, setting, climax, resolution. Process: Establish setting, introduce characters, develop plot, build to climax, resolve story.'
}

   
def SprDecompressorGenerator(SPRCompressor, video_length, working_title, category, category_details):
    category_info = category_details.get(category, "")
    prompt = f""" # MISSION
You are a Sparse Priming Representation (SPR) decompressor. You will be given an SPR compressed {SPRCompressor} content which has been written in such a way that makes sense to you.
# METHODOLOGY
Use the input given to you to fully understand and articulate the concept as a plan for the script for a {video_length} minute long video. Topic: {working_title}. Category: {category} which should be written with these details {category_info}
provided Instructions:
Section Breakdown: Divide the video into sections, providing a timestamp for each section. Ensure that the total duration aligns with the {video_length} minute length of the video.
Content Details: For each section, specify the subtopics or key points that should be discussed. This should align with the topic and the associative nature of the topic.
Impute Missing Information: Use inference and reasoning to fill in any gaps in information, ensuring a comprehensive coverage of the topic.
Focus on Plan, Not Script: The output should be a structured plan, not a full script. It should outline what will be discussed in each section, without writing the actual dialogue or narration.
Your plan should serve as a blueprint for creating an informative and engaging video on the complexities and capabilities of content."
    """
    messages2=[]
    messages2.append({"role": "user", "content": prompt})
        # Make the API call
    response2 = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages2
    )

    # Extract the response
    SPRDecompressor = response2.choices[0].message["content"]
    return SPRDecompressor

def ScriptGenerator(SPRDecompressor, user_input, video_length, category):
    prompt = f"""
You are designed to write scripts for {video_length} minute corporate training video for the category {category}. Users will provide a detailed plan {SPRDecompressor} with timestamps and a source text{user_input}, which is typically extensive. as a Script Generator, you will thoroughly scan the source text to align content with each section of the video plan.
For each minute of the video, the script should contain around 150 words, within a tolerance range of 140-160 words. This is essential for maintaining the pacing and flow of the video.
SPRScriptGenerator will prioritize technical accuracy and relevance, catering to a corporate employee audience. It will avoid informal language, humor, and personal opinions, maintaining a professional tone throughout. If encountering ambiguous requests, SPRScriptGenerator will independently seek information online to fill knowledge gaps, rather than asking the user for clarifications.
The output will be clear, concise, and strictly relevant to the video plan's topics, ensuring the script is content-rich and effectively communicates the intended message.
Please follow these instructions:
Content Extraction: Carefully read and extract relevant information from the source file for each section of the video plan.
Incorporate Examples: Wherever possible, include examples from the source file to illustrate points more clearly.
Word Count Adherence: Ensure each minute of the script has the required word count. If the initial draft falls short, please revise it to meet the 140-160 words per minute range.
Clarity and Relevance: While focusing on the word count, also ensure the script remains clear, concise, and closely related to the video plan's topics.
This approach will guarantee the script is rich in content, adheres to the specified word count, and effectively communicates the intended message.
    """

    messages3=[]
    messages3.append({"role": "user", "content": prompt})
        # Make the API call
    response3 = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages3
    )

    # Extract the response
    ScriptOP = response3.choices[0].message["content"]
    return ScriptOP


def ScreenplayDir(ScriptOP, category):
    # Logic to generate the screenplay script based on the final script
    # This is a placeholder for the actual implementation
    prompt = f"""    
    Objective: Transform script: {ScriptOP} into a detailed visual screenplay for a {category} video for corporate training video.
Scene Description: Detail setting and ambiance for each script section.
Character Dynamics: Describe positioning, movements, and interactions of characters or presenters.
Camera Work: Suggest appropriate camera angles and movements (close-ups, wide shots, pans, zooms).
Visual Elements: Propose visual effects, graphics, and text overlays to clarify concepts and emphasize key points.
Transitions: Outline smooth transitions between scenes or sections.
Timing Alignment: Ensure visual elements align with script timing for coherent pacing.
Audience & Category Adaptation: Customize visual style to audience and category (e.g., technical for 'Code Walkthrough', narrative for 'Masterclass')."""


    messages4=[]
    messages4.append({"role": "system", "content": prompt})
        # Make the API call
    response4 = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages4
    )

    # Extract the response
    screenplay_script = response4.choices[0].message["content"]
    return screenplay_script


# # Streamlit app UI
st.title('VIDEO SCRIPT GENERATOR')

# openai_api_key = st.text_input("OpenAI API Key", placeholder="Ex: sk-2twmA8tfCb8un4...")

openai_api_key = "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"
# New input fields
working_title = st.text_input('Working Title', placeholder='Enter the working title for the video')



col1, col2, col5 = st.columns([2, 2, 1])  # Adjust column width ratio as needed

with col1:
    audience = st.selectbox(
        'Audience',
        ('Developers', 'Product Manager', 'Executives', 'Sales'),
        index=0,  # Default selection (Developers)
        help="Select the intended audience for the video")

with col5:
    video_length = st.number_input(
        'Video Length (min)',
        min_value=1, max_value=10, value=5,  # Set range and default value
        help="Specify the intended video length in minutes")
    
with col2:
    category = st.selectbox(
    'Category',
    ('Case Study', 'Onboarding', 'Standard Procedures', 'Code Walkthrough', 
     'How-To Videos', 'Cheat Sheets', 'Masterclass', 'Story'),
    index=0,  # Default selection (Case Study)
    help="Select the category of the video")
        

# File upload and text input for user source
col3, col4 = st.columns([4, 2])  # 80%-20% column width ratio

with col3:
    user_input = st.text_area('Enter your text here', height=200)

with col4:
    uploaded_file = st.file_uploader("Upload file", type=["txt", "pdf"])
# Process the file or text input
content = ""
if uploaded_file is not None:
    # Read the file based on its type
    if uploaded_file.type == "text/plain":
        # Read text file
        content = str(uploaded_file.read(), "utf-8")
    elif uploaded_file.type == "application/pdf":
        # Handle PDF file
        try:
            with io.BytesIO(uploaded_file.read()) as open_pdf_file:
                read_pdf = PyPDF2.PdfFileReader(open_pdf_file)
                for page in range(read_pdf.numPages):
                    content += read_pdf.getPage(page).extractText()
        except Exception as e:
            st.error("Error reading PDF file")
elif user_input:
    content = user_input

if st.button("Generate"):
        # Flush the previous conversation history
    llm=load_LLM(openai_api_key=openai_api_key)
    llm2=load_LLM2(openai_api_key=openai_api_key)
    llm3=load_LLM3(openai_api_key=openai_api_key)
    llm4=load_LLM4(openai_api_key=openai_api_key)

    
    # llm = openai.OpenAI(openai_api_key=openai_api_key)
    # llm2 = openai.OpenAI(openai_api_key=openai_api_key)
    # llm3 = openai.OpenAI(openai_api_key=openai_api_key)

    if user_input:
        # Pass the input text through the first model
        with st.spinner(f"Processing to create summary..."):
            output_text1 = SPRCompressorGenerator(user_input)
        st.title("Summary:")
        st.write(output_text1)


        # Pass Model 1's output to the second model
        with st.spinner(f"Processing to generate content plan..."):
            output_text2 = SprDecompressorGenerator(output_text1 , video_length, working_title, category, category_details)
        st.title("PLAN:")
        st.write(output_text2)

        # Pass Model 2's output to the third model
        with st.spinner(f"Generating Script..."):
            final_output_text = ScriptGenerator(output_text2, user_input, video_length, category)
        st.title("Your FinalScript is:")
        st.write(final_output_text)
        
        st.session_state.final_output_text = final_output_text

        # Display the download button for the script
        if final_output_text:
            st.download_button(
                label="Download Script",
                data=final_output_text,
                file_name="script.txt",
                mime="text/plain"
            )

# Separate button for generating the screenplay script
if st.button("Generate Screenplay Script"):
        # Only proceed if there is a final script stored in session state
    if st.session_state.final_output_text:
        with st.spinner("Generating Screenplay..."):
            screenplay_script = ScreenplayDir(st.session_state.final_output_text, category)
        st.write("Your Screenplay Script is:")
        st.text(screenplay_script)

        # Download button for the screenplay script
        st.download_button(
            label="Download Screenplay Script",
            data=screenplay_script,
            file_name="screenplay_script.txt",
            mime="text/plain"
        )
    else:
        st.warning("Please generate the final script first.")
else:
    st.warning("Please enter some text to start the processing.")    

    

        