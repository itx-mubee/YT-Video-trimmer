import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import tkinter as tk
from PIL import ImageTk, Image

# Set up the YouTube API client
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "C:/Python_projects/Python/Video Trimmer/client_secret.json"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
)
creds = flow.run_local_server(port=0)

youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=creds)

# Create the main window
root = tk.Tk()
root.title("YouTube Trimmer")
root.geometry("500x400")

# Load the background image
bg_image = Image.open("C:/Python_projects/Python/Video Trimmer/background.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label with the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=5, y=7, relwidth=1, relheight=1)

# Load the logo image
logo_image = Image.open("C:/Python_projects/Python/Video Trimmer/logo.png")
logo_photo = ImageTk.PhotoImage(logo_image)
'''
# Create a label with the logo image
logo_label = tk.Label(root, image=logo_photo)
logo_label.place(x=20, y=20)
'''
# Create the text input field for the video URL
url_label = tk.Label(root, text="Enter the URL of the video you want to trim:")
url_label.place(x=20, y=100)

url_entry = tk.Entry(root, width=50)
url_entry.place(x=20, y=120)

# Create the text input fields for the start and end times
start_label = tk.Label(root, text="Enter the start time (in seconds):")
start_label.place(x=20, y=150)

start_entry = tk.Entry(root, width=20)
start_entry.place(x=20, y=170)

end_label = tk.Label(root, text="Enter the end time (in seconds):")
end_label.place(x=200, y=150)

end_entry = tk.Entry(root, width=20)
end_entry.place(x=200, y=170)

# Create a function to trim the video
def trim_video():
    try:
        # Get the video ID from the URL
        video_id = url_entry.get().split("=")[-1]

        # Get the start and end times from the input fields
        start_time = start_entry.get()
        end_time = end_entry.get()

        # Create a new playlist
        playlist_title = "Trimmed Videos"
        playlist_request = youtube.playlists().insert(
            part="snippet",
            body={
                "snippet": {
                    "title": playlist_title,
                    "description": "Playlist for trimmed videos"
                }
            }
        )
        playlist_response = playlist_request.execute()

        # Get the ID of the new playlist
        playlist_id = playlist_response["id"]

        # Create the parameters for the API request
        snippet = {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
        content_details = {
            "startAt": start_time + "s",
            "endAt": end_time + "s"
        }
        insert_request = youtube.playlistItems().insert(
            part="snippet,contentDetails",
            body={
                "snippet": snippet,
                "contentDetails": content_details
            }
        )

        # Execute the API request
        response = insert_request.execute()
        print(response)

    except googleapiclient.errors.HttpError as error:
        print(f"An error occurred: {error}")
        response = None

    if response:
        print("Video trimmed successfully.")
trim_button = tk.Button(root, text="Trim Video", padx=20, pady=10, bg="#004C99", fg="white", command=trim_video)
trim_button.place(x=200, y=220)

root.mainloop()