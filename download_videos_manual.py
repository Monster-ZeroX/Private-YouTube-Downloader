import os
import subprocess
from tkinter import Tk, filedialog
from tqdm import tqdm
import threading
from queue import Queue


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


# Function to download a single video
def download_video(video_url, cookies_file, download_location, progress_queue):
    cmd = [
        "yt-dlp",
        "--cookies",
        cookies_file,
        "-f",
        "bestvideo+bestaudio/best",
        "-o",
        os.path.join(download_location, "%(title)s.%(ext)s"),
        video_url,
    ]

    try:
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        for line in process.stdout:
            if "%" in line:
                try:
                    percent = int(line.split("%")[0].split()[-1])
                    progress_queue.put((video_url, percent))
                except (ValueError, IndexError):
                    pass

        process.wait()
        if process.returncode == 0:
            progress_queue.put((video_url, 100))
        else:
            raise subprocess.CalledProcessError(process.returncode, cmd)

    except subprocess.CalledProcessError as e:
        print(f"Failed to download {video_url}. Error: {e}\n")
        progress_queue.put((video_url, -1))


# Function to retry failed downloads
def retry_failed_downloads(failed_videos, cookies_file, download_location, retries, log_file):
    for attempt in range(1, retries + 1):
        if not failed_videos:
            break

        print(f"\nRetry attempt {attempt}/{retries} for failed downloads...\n")
        progress_queue = Queue()
        threads = []

        for video_url in failed_videos:
            thread = threading.Thread(
                target=download_video,
                args=(video_url, cookies_file, download_location, progress_queue),
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        results = collect_results(progress_queue)
        failed_videos = [url for url, status in results.items() if status != 100]

        with open(log_file, "a") as log:
            log.write(f"\nRetry attempt {attempt} results:\n")
            for url, status in results.items():
                log.write(f"{url} - {'Success' if status == 100 else 'Failed'}\n")

    return failed_videos


# Function to collect results from the progress queue
def collect_results(progress_queue):
    results = {}
    while not progress_queue.empty():
        video_url, status = progress_queue.get()
        results[video_url] = status
    return results


# Main function
def main():
    root = Tk()
    root.withdraw()

    # Configuration defaults
    default_cookies = "cookies.txt"

    # Always select video_links.txt using a file dialog
    cookies_file = select_file("cookies.txt")
    video_links_file = select_file("video_links.txt")

    # Always use the file dialog to select the download location
    download_location = select_directory()

    # Ask for retry limit
    retries = input("Enter the number of retry attempts for failed downloads (default is 3): ").strip()
    retries = int(retries) if retries.isdigit() else 3
    log_file = os.path.join(download_location, "download_log.txt")

    # Read video links
    if not os.path.exists(video_links_file):
        print(f"Error: File '{video_links_file}' not found.")
        exit(1)

    with open(video_links_file, "r") as file:
        video_links = [line.strip() for line in file if line.strip()]

    if not video_links:
        print("Error: No valid video links found in the file.")
        exit(1)

    print(f"Found {len(video_links)} video(s) to download.\n")

    # Start downloads
    progress_queue = Queue()
    threads = []

    for video_url in video_links:
        thread = threading.Thread(
            target=download_video,
            args=(video_url, cookies_file, download_location, progress_queue),
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Collect and retry failed downloads
    results = collect_results(progress_queue)
    failed_videos = [url for url, status in results.items() if status != 100]

    if failed_videos:
        failed_videos = retry_failed_downloads(
            failed_videos, cookies_file, download_location, retries, log_file
        )

    # Summarize results
    print("\nDownload Summary:")
    success_count = sum(1 for status in results.values() if status == 100)
    print(f"Successfully downloaded {success_count}/{len(video_links)} videos.")

    if failed_videos:
        print(f"Failed to download {len(failed_videos)} video(s):")
        for video in failed_videos:
            print(f"  - {video}")

    # Log final results
    with open(log_file, "a") as log:
        log.write("\nFinal Download Summary:\n")
        for video_url, status in results.items():
            log.write(f"{video_url} - {'Success' if status == 100 else 'Failed'}\n")
        if failed_videos:
            log.write("\nFailed Videos:\n")
            for video in failed_videos:
                log.write(f"{video}\n")
    print(f"\nLog saved at {log_file}")


if __name__ == "__main__":
    main()
