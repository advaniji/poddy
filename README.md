# Poddy Podcast Downloader

Poddy is a simple Python script that allows you to download podcast episodes from any RSS feed. The script allows you to filter episodes by year and download them at various quality levels. It leverages `yt-dlp`, `feedparser`, and other libraries to streamline the downloading process.

## Features
- Download podcast episodes from any RSS feed.
- Filter episodes by date (select how many years of episodes you want to download).
- Choose the download quality (e.g., 32kbps, 128kbps, etc.).
- Automatic handling of existing files (skips already downloaded episodes).
- Displays a progress bar for downloads with `tqdm`.

## Installation

### Prerequisites

Make sure you have Python 3.x installed. You can check by running:

```bash
python --version
Installing Dependencies

Clone this repository and install the required dependencies using the requirements.txt file:
git clone https://github.com/advaniji/poddy.git
cd poddy
pip install -r requirements.txt
Usage

## Run the script by executing the following command in your terminal:
python poddy.py
Follow the prompts:

    Enter the RSS feed URL of the podcast (eg from podcastindex.org).
    Specify the number of years of episodes to download (enter 0 to download all episodes).
    Select the quality for the downloads (e.g., 32, 128, 192 kbps).

The podcast episodes will be downloaded in the current directory, organized by the podcast name ( or will update if folder exists already)
## 🚀 To-Do List

### 1. ✨ Polish the Script
   - Refactor code for better readability and efficiency. 🧹
   - Improve error handling and logging. 📜
   - Add more detailed comments and documentation. ✍️

### 2. 🖥️ Add a GUI Version
   - Create a user-friendly graphical interface. 🎨
   - Make it intuitive for non-technical users. 🧑‍💻

### 3. 🌐 Allow Adding PodcastIndex.org URL
   - Integrate PodcastIndex.org's API for more podcast sources. 🌍
   - Allow users to search for podcasts directly from the platform. 🔍

### 4. 🎧 Improve Download Options
   - Allow the user to choose between different audio codecs (MP3, AAC, etc.). 🎶

### 5. 🔄 Support for Automatic Updates
   - Automatically check for and download only new episodes. ⏳
   - Avoid re-downloading already saved episodes. 🗂️

### 6. 📊 Enhance Progress Bar & UI Feedback
   - Improve progress bar with download counts and ETA. ⏱️
   - Show more detailed feedback during downloads. 📈
