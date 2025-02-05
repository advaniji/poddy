import os
import feedparser
import yt_dlp
from datetime import datetime, timedelta
import glob
from tqdm import tqdm
from termcolor import colored

def print_welcome_message():
    """Prints a welcome message and program name in a stylish way."""
    print(colored("======================================", 'cyan'))
    print(colored("   Poddy Podcast Downloader", 'magenta', attrs=['bold']))
    print(colored("======================================", 'cyan'))
    print("\nWelcome to the Poddy Podcast Downloader!")
    print("A simple way to download your favorite podcasts.\n")
    print("Tip: Enter '0' for the number of years to download all episodes.\n")

def format_date(date_string):
    """Formats date into a more readable format."""
    formats = [
        '%a, %d %b %Y %H:%M:%S %z',
        '%a, %d %b %Y %H:%M:%S GMT',
        '%Y-%m-%dT%H:%M:%SZ',
    ]
    for fmt in formats:
        try:
            pub_date = datetime.strptime(date_string, fmt)
            if pub_date.tzinfo is None:
                pub_date = pub_date.replace(tzinfo=datetime.now().astimezone().tzinfo)
            return pub_date.strftime('%d-%B-%Y'), pub_date
        except ValueError:
            continue
    print(f"Error parsing date: {date_string}")
    return date_string, None

def sanitize_filename(filename):
    """Sanitizes the filename to remove invalid characters."""
    return filename.replace("/", "-").replace("\\", "-").replace(":", "-")

def download_episode(url, podcast_title, title, date, quality):
    """Downloads a podcast episode with a progress bar."""
    filename = f'{sanitize_filename(title)} ({date}).%(ext)s'
    filepath = os.path.join(podcast_title, filename)
    base_name = os.path.join(podcast_title, f'{sanitize_filename(title)} ({date})')

    if not glob.glob(f"{base_name}.*"):  # Check if file already exists
        options = {
            'outtmpl': filepath,
            'progress_hooks': [progress_hook]
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                info_dict = ydl.extract_info(url, download=False)
                formats = [f for f in info_dict.get('formats', []) if f.get('vcodec') == 'none']
            except Exception as e:
                print(f"Error fetching formats for {title}: {e}")
                return

        # Quality levels
        quality_levels = [32, 64, 96, 128, 192, 256, 320]
        quality_found = False

        # Try to match requested quality
        for q in quality_levels:
            if int(quality) <= q:
                for fmt in formats:
                    if fmt.get('abr') and int(fmt['abr']) <= q:
                        selected_format = fmt['format_id']
                        options['format'] = selected_format
                        quality_found = True
                        break
            if quality_found:
                break

        # If no quality found, select the best available
        if not quality_found:
            print(f"Requested quality {quality} not available, selecting the best available...")
            selected_format = formats[-1]['format_id']
            options['format'] = selected_format

        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                ydl.download([url])
            except Exception as e:
                print(f"Error downloading episode {title}: {e}")
    else:
        print(f"File already exists: {glob.glob(f'{base_name}.*')[0]}")

def progress_hook(d):
    """Progress hook to track download progress."""
    if d['status'] == 'downloading':
        # Updates the progress bar
        tqdm.write(f"{colored(d['filename'], 'yellow')} - {d['_percent_str']} - {d['_eta_str']} remaining")
    elif d['status'] == 'finished':
        tqdm.write(colored(f"Download completed: {d['filename']}", 'green'))

def download_podcasts(rss_url, years, quality):
    """Downloads all podcasts from the RSS feed."""
    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
        return

    if not feed.entries:
        print("No episodes found in this feed.")
        return

    podcast_title = sanitize_filename(feed.feed.title if hasattr(feed.feed, 'title') else "Podcast")
    os.makedirs(podcast_title, exist_ok=True)

    cutoff_date = datetime.now().astimezone() - timedelta(days=365 * years) if years else None
    episodes = [entry for entry in feed.entries if hasattr(entry, 'published') and hasattr(entry, 'link') and hasattr(entry, 'title')]

    if not episodes:
        print("No episodes to download.")
        return

    for episode in episodes:
        date_str, pub_date = format_date(episode.published)
        if pub_date and (cutoff_date is None or pub_date >= cutoff_date):
            print(f"Downloading: {episode.title} ({date_str})")
            download_episode(episode.link, podcast_title, episode.title, date_str, quality)

def get_valid_quality():
    """Prompt user for a valid quality input."""
    valid_quality_levels = [32, 64, 96, 128, 192, 256, 320]
    while True:
        try:
            quality = int(input(f"Enter quality ({', '.join(map(str, valid_quality_levels))}): "))
            if quality in valid_quality_levels:
                return quality
            else:
                print("Invalid quality! Please enter a valid quality from the list.")
        except ValueError:
            print("Invalid input! Please enter a number corresponding to the quality levels.")

if __name__ == "__main__":
    print_welcome_message()

    rss_url = input("Enter RSS URL: ")
    years = int(input("Enter number of years (Enter 0 to download all episodes): "))
    quality = get_valid_quality()

    download_podcasts(rss_url, years, quality)
