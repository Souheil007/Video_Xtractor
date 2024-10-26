from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os
import shutil
import cv2
from pytube import YouTube
from paddleocr import PaddleOCR
from pytube import YouTube
import yt_dlp as youtube_dl
import os
import json
import google.generativeai as genai  # Correct import for the generative AI library
from dotenv import load_dotenv

from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


ydl_opts = {
    'verbose': True
}

# Load environment variables from .env file
load_dotenv()

# Access your API key as an environment variable
api_key = os.getenv("API_KEY")

# Set the API key for authentication
genai.configure(api_key=os.environ["API_KEY"])


app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

# Allow CORS for the specific origin (frontend URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to "*" only for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
)
# Initialize PaddleOCR model
ocr = PaddleOCR(use_angle_cls=True, lang='en')


def extract_frames_cv2(video_path, specific_second=None):
    output_dir = './backend/video_frames'
    os.makedirs(output_dir, exist_ok=True)
    
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    
    if specific_second is not None:
        specific_frame = int(specific_second * fps)
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, specific_frame)
        success, image = vidcap.read()
        if success:
            frame_filename = os.path.join(output_dir, f"frame{specific_frame}.jpg")
            cv2.imwrite(frame_filename, image)
            print(f"Saved frame at {specific_second} seconds as {frame_filename}")
        else:
            print(f"Could not read frame at {specific_second} seconds.")
    else:
        frame_interval = int(fps * 5)  # 5 seconds
        count = 0
        success = True
        while success:
            success, image = vidcap.read()
            if success and count % frame_interval == 0:
                frame_filename = os.path.join(output_dir, f"frame{count}.jpg")
                cv2.imwrite(frame_filename, image)
                print(f"Saved frame {count} as {frame_filename}")
            count += 1

    vidcap.release()
    print("Finished extracting frames.")

def extract_frames_cv2_youtube(video_url, specific_second=None):
    output_dir = './backend/video_frames'
    os.makedirs(output_dir, exist_ok=True)
    
    # Download video information and get the stream URL for 144p
    ydl_opts = {}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            formats = info_dict.get('formats', None)
            
            video_url = None
            for f in formats:
                if f.get('format_note') == '480p':  # Change to desired resolution
                    video_url = f.get('url')
                    break

        if not video_url:
            raise Exception("No suitable video format found.")
        
        # Open the video stream with OpenCV
        vidcap = cv2.VideoCapture(video_url)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        
        if specific_second is not None:
            specific_frame = int(specific_second * fps)
            vidcap.set(cv2.CAP_PROP_POS_FRAMES, specific_frame)
            success, image = vidcap.read()
            if success:
                frame_filename = os.path.join(output_dir, f"frame{specific_frame}.jpg")
                cv2.imwrite(frame_filename, image)
                print(f"Saved frame at {specific_second} seconds as {frame_filename}")
            else:
                print(f"Could not read frame at {specific_second} seconds.")
        else:
            frame_interval = int(fps * 5)  # 5 seconds interval
            count = 0
            success = True
            while success:
                success, image = vidcap.read()
                if success and count % frame_interval == 0:
                    frame_filename = os.path.join(output_dir, f"frame{count}.jpg")
                    cv2.imwrite(frame_filename, image)
                    print(f"Saved frame {count} as {frame_filename}")
                count += 1

        vidcap.release()
        print("Finished extracting frames.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def paddle_OCR():
    # Initialize the PaddleOCR model (specify the language)
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Change 'en' to your desired language code

    # Specify the path to your image
    image_path = '/content/frame_0001.jpg'  # Replace with your image path

    # Perform OCR on the image
    result = ocr.ocr(image_path, cls=True)

    # Process the result
    extracted_text = []
    for line in result:
        for word_info in line:
            extracted_text.append(word_info[1][0])  # Get the text

    # Print the extracted text
    text_extracted=' '.join(extracted_text)
    print(f"Extracted text from {image_path}: {text_extracted}")


#use Gemini-API
def process_line(content):
    #prompt = ("this is a code i extracted from an image of person coding in its pc so make it cleaner and remove undersirable and non sense words so i can see a clean code" + content)
    prompt = (
   "I have extracted the following code from an image of a person coding. "
   "Please refine this code by cleaning it up, removing any unnecessary or nonsensical words, "
   "and ensuring that the result remains true to the original intent and functionality of the code. "
   "if you find in the code some logs generated from terminal just remove them they are not useful"
   "also dont tell me what you did and dont comment the code"
   "Here is the code:\n\n" + content
        )
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
    prompt,)
    #print(response.text)
    # Extract the generated result text
    return response.text  # Adjust according to actual response structure


def format_text(text):
    # Remove unnecessary newlines and extra spaces
    formatted_text = " ".join(text.split())

    return formatted_text

def single_frame(extracted_text):
    #with paddleOCR
    x=' '.join(extracted_text)
    formatted_text = format_text(x)
    print(formatted_text)
    result = process_line(formatted_text)
    print(result)
    
def wrap_up():
    directory = './backend/video_frames/'
    d = {}
    all_text = ""
    global extract_code
    jpeg_files = sorted([f for f in os.listdir(directory) if f.endswith('.jpg') or f.endswith('.jpeg')])

    for filename in jpeg_files:
        image_path = os.path.join(directory, filename)

        result = ocr.ocr(image_path, cls=True)
        
        # Check if the result is None
        if result is None:
            print(f"Warning: OCR returned None for {image_path}")
            continue  # Skip to the next image

        extracted_text = []
        for line in result:
            if line is not(None):
                for word_info in line:
                    extracted_text.append(word_info[1][0])

        text_extracted = ' '.join(extracted_text)

        formatted_text = format_text(text_extracted)
        print(f"Formatted text: {formatted_text}")  # Debugging statement

        processed_result = process_line(formatted_text)
        if processed_result is None:
            print(f"Warning: process_line returned None for {formatted_text}")
            continue  # Or handle this case as appropriate

        all_text += processed_result
        print(f"Extracted text from {image_path}: {processed_result}")
        print("Newline")
        d[filename] = processed_result
    extract_code = list(d.values())    
    print(d)
    return d


# Upload local video and process
@app.post("/upload-video/")
async def upload_video(video: UploadFile = File(...), second: int = Form(None)):  # Form() to receive 'second'
    print(f"Received second: {second}")  # Debugging line
    video_path = f"./{video.filename}"
    with open(video_path, "wb") as f:
        shutil.copyfileobj(video.file, f)
    
    # Extract frames using OpenCV
    extract_frames_cv2(video_path, specific_second=second)
    dictionnaire=wrap_up()
    #extract_code=list(dictionnaire.values())
    print(f"The extracted code is : {extract_code}")
    # Clean up the video frames directory after processing
    output_dir = './backend/video_frames'
    if os.path.exists(output_dir):
        # Optionally, remove files within the directory before removing the directory itself
        shutil.rmtree(output_dir)  # This removes the directory and all its contents
    return JSONResponse(list(dictionnaire.values()))

@app.post("/process-youtube/")
async def process_youtube(video_url: str = Form(...), second: int = Form(None)):
    print(f"Received video_url: {video_url}, second: {second}")
    # Call the function to extract the frame at the specified second
    extract_frames_cv2_youtube(video_url, specific_second=second)
    dictionnaire=wrap_up()
    #extract_code=list(dictionnaire.values())
    print(f"The extracted code is : {extract_code}")
    # Clean up the video frames directory after processing
    output_dir = './backend/video_frames'
    if os.path.exists(output_dir):
        # Optionally, remove files within the directory before removing the directory itself
        shutil.rmtree(output_dir)  # This removes the directory and all its contents
    return JSONResponse(list(dictionnaire.values()))

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyC9Sda5-DuB2sDAlyPnUQ-n4mTPlNyeuHc")

# Setup the LangChain with the prompt
code_prompt = PromptTemplate.from_template("""
You are a highly skilled AI code assistant. You have the following code:
{code}
Answer the following question about the code:
{question}
""")
code_chain = LLMChain(llm=llm, prompt=code_prompt, verbose=True)


# Request model for handling the incoming JSON from React (now only question)
class QuestionQuery(BaseModel):
    question: str

@app.post("/ask_code_question/")
async def ask_code_question(request: QuestionQuery):
    """Endpoint to answer questions about the extracted code."""
  
    # Get the chatbot response
    response = code_chain.run(code=' '.join(extract_code), question=request.question)
    return {"response": response}
