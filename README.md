# Video\_Xtractor

## Overview

**Video\_Xtractor** is a web-based application designed to extract and retrieve code snippets from specific frames of local or YouTube videos. By providing a timestamp or URL, users can seamlessly access relevant code segments, enhancing learning and development workflows.

## Features

* **Frame-specific Code Retrieval**: Extract code from any frame using its timestamp or YouTube URL.
* **Local Video Support**: Upload and process local video files for code extraction.
* **YouTube Integration**: Input YouTube URLs to extract code from online videos.
* **User-friendly Interface**: Built with React.js for the frontend and FastAPI for the backend, ensuring a responsive and intuitive experience.

## Video Demo

You can add a video demo here to showcase the application in action:

[![Video Demo](https://www.google.com/search?sca_esv=827ca067cae54b45&udm=2&fbs=AIIjpHx4nJjfGojPVHhEACUHPiMQ_pbg5bWizQs3A_kIenjtcpTTqBUdyVgzq0c3_k8z34EAuM72an33lMW6RWde9ePJpwNFtZw3UQvFloZy04_0a7Y_s9Q2prhO8GUp_-RabNoWBXexBhzeXMQlUILLh2ARtfR9QNvwqh5uPW0knmdMojKOxWeL4aHHp3t_o5qsNUJAbfMQ&q=code+Extractor&sa=X&ved=2ahUKEwjQjYn714ePAxXGfKQEHYTGE10QtKgLegQIFxAB&biw=1463&bih=780&dpr=1.75#vhid=9JJs2BBCgpwLlM&vssid=mosaic)](https://www.linkedin.com/posts/souheil-bichiou-036079279_coding-project-tech-activity-7244418771249942528-jgOM?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEPRw-oB_ukvBr0H2Jg3zrBbea8305sCDV8)

## Installation

### Prerequisites

Ensure you have the following installed:

* Python 3.8+
* Node.js and npm
* Docker (optional, for containerized setup)

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Souheil007/Video_Xtractor.git
   cd Video_Xtractor/backend
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

   The backend will be accessible at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd ../frontend
   ```

2. Install Node.js dependencies:

   ```bash
   npm install
   ```

3. Start the React development server:

   ```bash
   npm start
   ```

   The frontend will be accessible at `http://localhost:3000`.

### Docker Setup (Optional)

For a containerized setup, use Docker Compose:

1. Ensure Docker is installed and running.
2. From the root directory of the project, run:

   ```bash
   docker-compose up --build
   ```

   This will build and start both the backend and frontend services.

## Usage

1. Open your browser and navigate to `http://localhost:3000`.
2. Upload a local video file or enter a YouTube URL.
3. Provide the timestamp of the frame from which you wish to extract code.
4. Click "Extract Code" to retrieve the relevant code snippet.

## Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License.
