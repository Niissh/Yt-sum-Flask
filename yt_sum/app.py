from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

app = Flask(__name__)

@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    try:
        summary = get_summary(get_transcript(video_id))
        return summary, 200
    except Exception as e:
            return f"Error: {str(e)}", 500

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([d['text'] for d in transcript_list])
        return transcript
    except Exception as e:
        raise ValueError("Could not retrieve transcript for the video. Subtitles may be disabled.")

def get_summary(transcript):
    summariser = pipeline('summarization')
    summary = []
    # for i in range(0, (len(transcript)//1000)+1):
    for i in range(0, len(transcript), 1000):
        summary = summariser(transcript[i:i+1000])[0]['summary_text']
        summary.append(summary)
        # summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary= ' '.join(summary)
        # summary = summary + summary_text + ' '
    return summary
    

if __name__ == '__main__':
    app.run()