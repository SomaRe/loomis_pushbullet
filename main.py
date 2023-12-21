import sys
from pushbullet import Pushbullet
import keys
import requests
import bs4
import time

last_date = None

# Function to check the progress and send a Pushbullet notification if width > 90
def check_progress_and_notify(tracking_number):
    global last_date

    url_to_track = f'https://www.loomisexpress.com/loomship/Track/TrackResults?t=WAYBILL&s={tracking_number}#{tracking_number}'
    res = requests.get(url_to_track)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Find class progress-bar and check the width
    progress_bar = soup.find('div', class_='progress-bar')

    # Find the last 'tracking-detail' row
    last_tracking_detail = soup.find_all('div', class_='tracking-detail')[1]
    width = int(progress_bar['style'].split(';')[0].split(':')[1][:-1].strip())

    # Extract the date, status, and location from the last 'tracking-detail'
    details = [div.get_text(strip=True) for div in last_tracking_detail.find_all('div', class_='col-md-4')]

    # details now contains the date, status, and location
    date, status, location = details

    if last_date != date:
        last_date = date
        print(f"Date: {date}\nStatus: {status}\nLocation: {location}\nProgress Bar Width: {width}%")
        pb = Pushbullet(keys.PUSHBULLET_ACCESS_TOKEN)
        pb.push_note("Progress Alert", f"Date: {date}\nStatus: {status}\nLocation: {location}\nProgress Bar Width: {width}%\nLink: {url_to_track}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python track_progress.py <tracking_number>")
        sys.exit(1)

    tracking_number = sys.argv[1]

    # Run the loop every 5 minutes
    while True:
        check_progress_and_notify(tracking_number)
        time.sleep(300)  # Sleep for 5 minutes (300 seconds)
