from flask import Flask, request, jsonify
import whisper, boto3, os, time
import matplotlib.pyplot as plt
import pandas as pd
from textblob import TextBlob

app = Flask(__name__)

# Initialize Whisper model and S3 client
whisper_model = whisper.load_model("base")
s3 = boto3.client("s3")
BUCKET = "cs14-2-nlp"
PREFIX = "videos_with_high_info/"

# Supported audio and video file extensions
AUDIO_EXTS = [".wav", ".mp3", ".m4a", ".flac"]
VIDEO_EXTS = [".mp4", ".mkv", ".mov"]

# Extract audio from video using ffmpeg
def extract_audio(video_path, audio_path):
    os.system(f'ffmpeg -i "{video_path}" -ac 1 -ar 16000 -vn -loglevel error -y "{audio_path}"')

@app.route("/s3-audio", methods=["POST"])
def analyze_all_in_prefix():
    """
    Automatically list and process all supported audio/video files 
    under the videos_with_high_info/ prefix in S3.
    """
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX)
    if "Contents" not in response:
        return jsonify({"error": "No files found in the specified S3 prefix."}), 404

    all_keys = [
        obj["Key"] for obj in response["Contents"]
        if not obj["Key"].endswith("/")
    ]

    records = []

    for key in all_keys:
        try:
            base, ext = os.path.splitext(os.path.basename(key))
            ext = ext.lower()
            local_input = f"/tmp/{base}{ext}"
            local_audio = f"/tmp/{base}.wav"

            if ext not in AUDIO_EXTS + VIDEO_EXTS:
                records.append({"file": key, "error": f"Unsupported file type: {ext}"})
                continue

            # Download from S3
            s3.download_file(BUCKET, key, local_input)

            # Audio or video handling
            if ext in AUDIO_EXTS:
                local_audio = local_input
            else:
                extract_audio(local_input, local_audio)

            # Transcribe and analyze
            text = whisper_model.transcribe(local_audio)["text"]
            tb = TextBlob(text)
            polarity = tb.sentiment.polarity
            subjectivity = tb.sentiment.subjectivity

            records.append({
                "file": base,
                "polarity": polarity,
                "subjectivity": subjectivity
            })

            # Clean up temp files
            if os.path.exists(local_input): os.remove(local_input)
            if os.path.exists(local_audio) and local_audio != local_input:
                os.remove(local_audio)

        except Exception as e:
            records.append({"file": key, "error": str(e)})

    df = pd.DataFrame([r for r in records if "error" not in r])
    if df.empty:
        return jsonify({"error": "No valid files processed", "details": records}), 500

    # Generate sentiment charts
    ts = int(time.time())
    pol_png = f"/tmp/polarity_{ts}.png"
    sub_png = f"/tmp/subjectivity_{ts}.png"

    def _bar(col, title, path, ylim):
        plt.figure(figsize=(12, 6))
        plt.bar(df["file"], df[col], color="skyblue")
        plt.xticks(rotation=45, ha="right")
        plt.title(title)
        plt.ylim(*ylim)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()

    _bar("polarity", "Sentiment Polarity", pol_png, (-1, 1))
    _bar("subjectivity", "Subjectivity", sub_png, (0, 1))

    # Upload images to S3
    pol_key = f"output/polarity_{ts}.png"
    sub_key = f"output/subjectivity_{ts}.png"
    s3.upload_file(pol_png, BUCKET, pol_key)
    s3.upload_file(sub_png, BUCKET, sub_key)

    # Clean up generated images
    os.remove(pol_png)
    os.remove(sub_png)

    return jsonify({
        "status": "ok",
        "processed": len(df),
        "png_urls": [
            f"s3://{BUCKET}/{pol_key}",
            f"s3://{BUCKET}/{sub_key}"
        ],
        "details": records
    })

# Health check endpoint
@app.route("/health")
def health():
    return jsonify({"status": "running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
