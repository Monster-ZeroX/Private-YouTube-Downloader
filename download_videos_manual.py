import os
import subprocess
from tkinter import Tk, filedialog
from tqdm import tqdm


# Function to select a file using a file dialog
def select_file(file_description):
    print(f"Please select the {file_description}...")
    file_path = filedialog.askopenfilename(title=f"Select {file_description}")
    if not file_path:
        print(f"Error: No {file_description} selected.")
        exit(1)
    print(f"Selected {file_description}: {file_path}\n")
    return file_path


# Function to select a directory for download location
def select_directory():
    print("Please select the download location...")
    dir_path = filedialog.askdirectory(title="Select Download Location")
    if not dir_path:
        print("Error: No download location selected.")
        exit(1)
    print(f"Selected download location: {dir_path}\n")
    return dir_path


# Main function
def main():
    # Initialize Tkinter and hide the main window
    root = Tk()
    root.withdraw()

    # Select the cookies file
    cookies_file = select_file("cookies.txt")

    # Select the video links file
    video_links_file = select_file("video_links.txt")

    # Select the download location
    download_location = select_directory()

    # Read the video links from the file
    if not os.path.exists(video_links_file):
        print(f"Error: File '{video_links_file}' not found.")
        exit(1)

    with open(video_links_file, "r") as file:
        video_links = [line.strip() for line in file if line.strip()]

    if not video_links:
        print("Error: No valid video links found in the file.")
        exit(1)

    print(f"Found {len(video_links)} video(s) to download.\n")

    for idx, video_url in enumerate(video_links, start=1):
        print(f"Downloading video {idx}/{len(video_links)}: {video_url}")
        try:
            with tqdm(total=100, desc=f"Downloading {video_url}", unit="%", ncols=80) as pbar:
                # yt-dlp command
                cmd = [
                    "yt-dlp",
                    "--cookies",
                    cookies_file,
                    "-f",
                    "bestvideo+bestaudio/best",
                    "-o",
                    f"{download_location}/%(title)s.%(ext)s",
                    video_url,
                ]

                # Run yt-dlp as a subprocess and capture output
                process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )

                # Read yt-dlp output to update progress
                for line in process.stdout:
                    if "%" in line:
                        try:
                            # Extract percentage from yt-dlp output
                            percent = int(line.split("%")[0].split()[-1])
                            pbar.n = percent
                            pbar.last_print_n = percent  # Avoid overcounting
                            pbar.refresh()
                        except (ValueError, IndexError):
                            pass

                process.wait()

                # Check if the process completed successfully
                if process.returncode == 0:
                    print(f"\nSuccessfully downloaded: {video_url}\n")
                else:
                    raise subprocess.CalledProcessError(process.returncode, cmd)

        except subprocess.CalledProcessError as e:
            print(f"Failed to download {video_url}. Error: {e}\n")

    print("All done!")


# Run the main function
if __name__ == "__main__":
    main()
