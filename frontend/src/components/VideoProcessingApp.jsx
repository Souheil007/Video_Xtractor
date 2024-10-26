import React, { useState } from 'react';
import ReactPlayer from 'react-player';
import axios from 'axios';
import './videoProcessingApp.css'; // Import your CSS styles
import './Chatbot.css'; // To style the logo and modal
import chatbotLogo from './chatbott.jpg';

function VideoProcessingApp() {
  const [videoFile, setVideoFile] = useState(null);
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [outputText, setOutputText] = useState('');
  const [isYoutube, setIsYoutube] = useState(false);
  const [specificSecond, setSpecificSecond] = useState(''); // State for specific second

  // Handle local video upload
  const handleVideoUpload = (e) => {
    setVideoFile(e.target.files[0]);
    setIsYoutube(false);
    setYoutubeUrl('')
  };

  // Handle YouTube URL input
  const handleYoutubeUrlChange = (e) => {
    setYoutubeUrl(e.target.value);
    setIsYoutube(true);
    setVideoFile(null)
    console.log("youtube vid uploaded")
    console.log(e.target.value)
  };

  // Handle specific second input change
  const handleSpecificSecondChange = (e) => {
    const value = e.target.value;
    // Ensure the input is a valid number or empty
    if (value === '' || (!isNaN(value) && value >= 0)) {
      setSpecificSecond(value);
    }
  };

  // Process video or YouTube link
  const processVideo = async () => {
    if (isYoutube && youtubeUrl) {
      try {
        const response = await axios.post('http://localhost:8000/process-youtube/', {
          video_url: youtubeUrl, // Adjusted to match FastAPI expected parameter name
          second: specificSecond ? parseInt(specificSecond, 10) : null, // Convert to number or pass null
        },{
          headers: {
            'Content-Type': 'multipart/form-data',
          },});
        console.log("processing youtube")
        setOutputText(response.data);
      } catch (error) {
        console.error('Error processing YouTube video', error);
        setOutputText('Error processing YouTube video. Please try again.');
      }
    } else if (videoFile) {
      const formData = new FormData();
      formData.append('video', videoFile);
      if (specificSecond) {
        formData.append('second', parseInt(specificSecond, 10)); // Include specific second as an integer
      }

      try {
        const response = await axios.post('http://localhost:8000/upload-video/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        setOutputText(response.data);
      } catch (error) {
        console.error('Error processing uploaded video', error);
        setOutputText('Error processing uploaded video. Please try again.');
      }
    } else {
      alert('Please upload a video or provide a YouTube URL.');
    }
  };



  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [isOpen, setIsOpen] = useState(false); // Controls whether the chatbot modal is open

  // Function to toggle the chatbot modal
  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  const handleAskQuestion = async () => {
    const res = await fetch("http://localhost:8000/ask_code_question/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: question,
      }),
    });

    const data = await res.json();
    setResponse(data.response);
  };
  

  return (
    <div className="app-container">
      <h1 className="app-title">Video Processing App</h1>

      <div className="input-container">
        <h2>Upload Local Video</h2>
        <input type="file" accept="video/*" onChange={handleVideoUpload} className="file-input" />
      </div>

      <div className="input-container">
        <h2>Or Enter YouTube URL</h2>
        <input
          type="text"
          placeholder="Enter YouTube URL"
          value={youtubeUrl}
          onChange={handleYoutubeUrlChange}
          className="url-input"
        />
      </div>

      <div className="input-container">
        <h2>Extract Frame at Specific Second (optional)</h2>
        <input
          type="number"
          placeholder="Enter second (e.g., 10)"
          value={specificSecond}
          onChange={handleSpecificSecondChange}
          className="second-input"
          min="0"
        />
      </div>

      <div className="video-player">
        {isYoutube && youtubeUrl ? (
          <ReactPlayer url={youtubeUrl} controls />
        ) : (
          videoFile && (
            <ReactPlayer
              url={URL.createObjectURL(videoFile)}
              controls
              width="100%"
              height="auto"
            />
          )
        )}
      </div>

      <button className="process-button" onClick={processVideo}>
        Run
      </button>

      <div className="output-container">
        <h2>Output</h2>
        <pre className="output-text">{outputText}</pre>
      </div>

      <div>
      {/* Floating logo/button to open chatbot */}
      <div className="chatbot-logo" onClick={toggleChatbot}>
        {/* You can replace this with an actual logo */}
        <img src={chatbotLogo} alt="Chatbot Logo" />

      </div>

      {/* Chatbot Modal */}
      {isOpen && (
        <div className="chatbot-modal">
          <div className="chatbot-header">
            <h2>Souheil's Chatbot</h2>
            <button onClick={toggleChatbot} className="close-btn">X</button>
          </div>
          <div className="chatbot-body">
            {/* Input field for user question */}
            <input
              type="text"
              placeholder="Ask a question about the code"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              style={{
                width: "100%",
                marginBottom: "10px",
                padding: "15px",
                borderRadius: "25px",  // Rounded corners
                border: "2px solid #ddd",
                outline: "none",
                fontSize: "16px",
                transition: "border-color 0.3s, box-shadow 0.3s",
                backgroundColor: "#fafafa", // Light background for a clean look
                boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)", // Subtle shadow for depth
            }}
            />
            {/* Button to submit the question */}
            <button onClick={handleAskQuestion} 
            style={{
              width: "100%",
              padding: "15px",
              borderRadius: "25px",  // Rounded corners for the button
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              fontSize: "18px",
              fontWeight: "bold",
              cursor: "pointer",
              transition: "background-color 0.3s, box-shadow 0.3s",
              boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)", // Soft shadow for a floating effect
          }}>
              Ask
            </button>
            {/* Display the response */}
            {response && (
              <div style={{ marginTop: "20px", padding: "10px", background: "#f0f0f0" }}>
                <strong>Response:</strong> <br />
                {response}
              </div>
            )}
          </div>
        </div>
      )}
    </div>


    </div>

    
        





  );
}

export default VideoProcessingApp;
