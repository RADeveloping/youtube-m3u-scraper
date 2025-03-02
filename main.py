import os
import yt_dlp

# Constants
INPUT_FILE = "youtube_links.txt"
OUTPUT_FILE = "output.m3u"

def fetch_m3u8(youtube_url):
    """
    Uses yt-dlp to extract the .m3u8 link from a public YouTube livestream.
    """
    ydl_opts = {
        "quiet": True,
        "simulate": True,
        "format": "best",  # Get the best available format
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(youtube_url, download=False)
            if "url" in info:
                return info["url"]
        except Exception as e:
            print(f"Error extracting {youtube_url}: {e}")

    return None

def process_links(input_file, output_file):
    """
    Processes YouTube livestream links and writes .m3u8 links to an .m3u file.
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
    print("Starting processing...")
    process_links(INPUT_FILE, OUTPUT_FILE)
    print("Processing complete.")
