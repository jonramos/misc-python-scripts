import yt_dlp

def download_video(url):
    try:
        # Options for the downloader
        ydl_opts = {
            'format': 'best',
            # If you need to convert to mp3, enable the postprocessors.
            #'postprocessors': [{
            #    'key': 'FFmpegExtractAudio',
            #    'preferredcodec': 'mp3',}]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Starting download: {url}")
            ydl.download([url])
            print("Download complete!")

    except Exception as e:
        print(f"An error occurred: {e}")

download_video(input("Enter video url: "))
print("done")
