import os
import requests
import re
from time import sleep

# Constants
INPUT_FILE = "youtube_links.txt"
OUTPUT_FILE = "output.m3u"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

def fetch_m3u8(youtube_url):
    """
    Extracts the .m3u8 link from a YouTube video or livestream.
    """
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(youtube_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch YouTube URL: {youtube_url}")
        return None

    # Regex to extract .m3u8 link
    m3u8_match = re.search(r'(https?://[^\s]+\.m3u8)', response.text)
    if m3u8_match:
        return m3u8_match.group(1)
    print(f"No .m3u8 link found for: {youtube_url}")
    return None

def process_links(input_file, output_file):
    """
    Processes YouTube links and writes .m3u8 links to an .m3u file.
    """
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found.")
        return

    with open(input_file, "r") as file:
        links = [line.strip() for line in file if line.strip()]

    m3u8_links = []
    for link in links:
        print(f"Processing: {link}")
        m3u8_link = fetch_m3u8(link)
        if m3u8_link:
            m3u8_links.append(m3u8_link)

    if m3u8_links:
        with open(output_file, "w") as m3u_file:
            for m3u8 in m3u8_links:
                m3u_file.write(m3u8 + "\n")
        print(f"Saved .m3u8 links to {output_file}")
    else:
        print("No valid .m3u8 links found.")

if __name__ == "__main__":
    while True:
        print("Starting processing...")
        process_links(INPUT_FILE, OUTPUT_FILE)
        print("Processing complete. Waiting for refresh...")
        # Adjust this delay based on YouTube's expiration policy
        sleep(3600)
