import yt_dlp
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Allow CORS for all origins (you can restrict it for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

downloads_folder = 'downloads'
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)

@app.post("/download")
async def download_video(request: Request):
    # Read the plain text body from the request
    link = await request.body()
    link_str = link.decode("utf-8")  # Decode bytes to string
    print(f"Received URL: {link_str}")

    info_options = {
        'format': 'best',
    }

    try:
        # Download the video using yt-dlp
        with yt_dlp.YoutubeDL(info_options) as ydl:
            info_dict = ydl.extract_info(link_str,download=False)
            video_title = info_dict.get('title', 'Unknown Title')
            video_extension = info_dict.get('ext','mp4')
            download_options = {
                'format': 'best',
                'outtmpl': f'{downloads_folder}/{video_title}.{video_extension}'  # Save using video title and extension
            }
            with yt_dlp.YoutubeDL(download_options) as ydl:
                ydl.download([link_str])  # Download the video from the URL
            return {
                "message": "Video downloaded successfully!",
                "title": video_title,
                "extension": video_extension,
                "path": f"{downloads_folder}/{video_title}.{video_extension}"
            }
    except Exception as e:
        # Handle exceptions that occur during video download
        return {"detail": f"Error downloading video: {str(e)}"}

@app.get("/")
def fun():
    return {"mes":"Hi"}