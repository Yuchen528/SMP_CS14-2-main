README.txt

Project Title: S3 Audio/Video Sentiment Analysis Service

---

📌 Project Description:
This project is a Flask-based web API that performs automatic sentiment analysis on audio or video files stored in an AWS S3 bucket.

The system:
1. Downloads audio/video files from the specified S3 folder.
2. Uses the Whisper model to transcribe audio into text.
3. Performs sentiment analysis using TextBlob to calculate polarity and subjectivity.
4. Generates two bar chart images (for polarity and subjectivity) using matplotlib.
5. Uploads the output images back to a designated folder in the same S3 bucket.

---

📂 Project Structure:

- `app.py`              — Main Flask app with `/s3-audio` API endpoint.
- `requirements.txt`    — Python dependencies (not provided here, but includes: flask, boto3, matplotlib, pandas, textblob, whisper).
- S3 Folder Structure:
  - `videos_with_high_info/` — Input folder for audio/video files.
  - `output/`                — Output folder where chart images are uploaded.

---

🚀 Quick Start Instructions:

1. **Set up virtual environment and install dependencies:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Run the Flask server: python app.py


Send a test POST request: curl -X POST http://localhost:5000/s3-audio


