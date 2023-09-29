import sys
from pushbullet import Pushbullet
import keys
import requests
import bs4
import time

# Function to check the progress and send a Pushbullet notification if width > 90
def check_progress_and_notify(tracking_number):
    url_to_track = f'https://www.loomisexpress.com/loomship/Track/TrackResults?t=WAYBILL&s={tracking_number}#{tracking_number}'
    res = requests.get(url_to_track)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Find class progress-bar and check the width
    progress_bar = soup.find('div', class_='progress-bar')
    width = int(progress_bar['style'].split(';')[0].split(':')[1][:-1].strip())

    print(f"Progress Bar Width: {width}%")

    if width > 90:
        pb = Pushbullet(keys.PUSHBULLET_ACCESS_TOKEN)
        pb.push_note("Progress Alert", f"Progress Bar Width: {width}%")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python track_progress.py <tracking_number>")
        sys.exit(1)

    tracking_number = sys.argv[1]

    # Run the loop every 5 minutes
    while True:
        check_progress_and_notify(tracking_number)
        time.sleep(300)  # Sleep for 5 minutes (300 seconds)
