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
