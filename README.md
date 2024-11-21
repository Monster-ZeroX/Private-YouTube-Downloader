# **Private YouTube Downloader**

A powerful and efficient tool to download private YouTube videos using `yt-dlp`, complete with file selection dialogs for cookies, video links, and the download location. The script is designed to help users download videos from private YouTube accounts that they have access to, with ease and reliability.

---

## **Features**

- **Flexible Authentication**:
  - Select the `cookies.txt` file for seamless authentication.
- **Batch Video Downloads**:
  - Input a `video_links.txt` file containing YouTube video URLs.
- **Custom Download Location**:
  - Choose a directory to save your videos.
- **Progress Visualization**:
  - Displays a real-time progress bar for each download using `tqdm`.
- **Reliable Downloads**:
  - Utilizes `yt-dlp` for fast and dependable video downloads.
- **Error Handling**:
  - Automatically retries failed downloads.

---

## **Quick Start**

### **Option 1: Use the Executable (No Dependencies Needed!)**
If you want to skip the trouble of installing Python or dependencies, simply download the prebuilt executable file (`video_downloader.exe`) from the [Releases](../../releases) section.

1. Download the `.exe` file.
2. Place your `cookies.txt` and `video_links.txt` in the same directory as the executable.
3. Double-click the `.exe` file and follow the prompts to start downloading.

**Antivirus Note**:  
Some antivirus programs might flag the `.exe` file as suspicious because it bundles Python and dependencies into a single package. If this happens:
- Whitelist the `.exe` file in your antivirus settings.
- Alternatively, you can verify the source code in this repository and build the executable yourself.

---

### **Option 2: Use the Python Script**
If you prefer to run the script directly, follow these steps:

#### **Requirements**
Before running the script, ensure you have the following installed:
- Python 3.6+  
- `yt-dlp`, `tqdm`, and `tkinter` (included in `requirements.txt`)

---

## **Installation**

## Step 1: Clone the Repository

1. Clone the repository to your local machine by running:
   ```bash
   git clone https://github.com/YourUsername/Private-YT-Downloader.git
   cd Private-YT-Downloader
   pip install -r requirements.txt
## Step 2: Install Dependencies
##### 1. Install the required dependencies using ```pip```:
```
pip install -r requirements.txt
```
##### 2. Make sure you have yt-dlp installed:
```
pip install yt-dlp
```
##### 3. Check for Tkinter:
- ```tkinter``` is used for GUI components. It should come pre-installed with Python. To check if it's installed, run:
```
python -m tkinter
```
If this opens a window with a simple interface, you're good to go! If not, you can install tkinter based on your operating system:
- On Debian/Ubuntu
```
sudo apt-get install python3-tk
```
- On Windows and macOS, ```tkinter``` is usually included with Python, so you shouldn't need to install it manually.

# Usage
## Step 1: Export Cookies from Your Browser
To authenticate and download private YouTube videos, you need to provide a ```cookies.txt``` file, which stores your browser session information. Here’s how to export it from Google Chrome (instructions are similar for other browsers):

### For Google Chrome:
##### 1. Install the Get cookies.txt LOCALLY Chrome extension:

- Go to the Chrome Web Store: [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc?hl=en) Extension
- Click "Add to Chrome" and confirm the installation.
##### 2. Export your cookies:

- Navigate to YouTube and log in to your account (make sure you can access the private videos you want to download).
- Click the EditThisCookie icon in the toolbar.
- Click on the "Export" button.
- Save the cookies as a .txt file on your system.
#### Important: Ensure that the cookies.txt file contains Netscape format cookies, which is the required format for yt-dlp.


## Step 2: Create video_links.txt
Create a plain text file named ```video_links.txt``` that contains one YouTube video URL per line. For example:

```
https://www.youtube.com/watch?v=XXXXXXXXXXX
https://www.youtube.com/watch?v=YYYYYYYYYYY
```
## Step 3: Run the Script
Once you have your ```cookies.txt``` and ```video_links.txt``` files ready, you can run the script to start downloading videos.

Open a terminal or command prompt, and navigate to the directory where the script is located.
-Execute the script by running:
```bash
python download_videos_manual.py
```
## Step 4: Select Files and Download Location
- A file dialog will open asking you to select the cookies.txt file you exported from your browser.
- A file dialog will also prompt you to select the video_links.txt file containing the YouTube video URLs.
- Lastly, you will be prompted to choose the directory where you want to save the downloaded videos.
## Step 5: Download Progress
The script will download each video and display a progress bar showing the download status, including the download speed and percentage completed.

**Example Output:**
```
Found 1 video(s) to download.

Downloading video 1/1: https://www.youtube.com/watch?v=VVEYA2kObV0
Downloading https://www.youtube.com/watch?v=VVEYA2kObV0:  50%|█████     | 50/100 [00:10<00:10, 5MB/s]
Successfully downloaded: https://www.youtube.com/watch?v=VVEYA2kObV0\

All done!
```
## License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

## Contributing

Feel free to fork this repository and submit pull requests for improvements and bug fixes. Contributions are welcome!

## Disclaimer

This tool is for educational purposes only. Please ensure you have the necessary permissions to download the videos.
