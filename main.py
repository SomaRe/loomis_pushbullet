from pushbullet import Pushbullet
import keys
import requests
import bs4
import time

# Function to check the progress and send a Pushbullet notification if width > 90
def check_progress_and_notify(url_to_track):
    res = requests.get(url_to_track)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Find class progress-bar and check the width
    progress_bar = soup.find('div', class_='progress-bar')
    width = int(progress_bar['style'].split(';')[0].split(':')[1][:-1].strip())

    print(f"Progress Bar Width: {width}%")

    if width > 90:
        pb = Pushbullet(keys.PUSHBULLET_ACCESS_TOKEN)
        pb.push_note("Progress Alert", f"Progress Bar Width: {width}%")
        return 'break'
    
    return 'continue'

# URL to track
url_to_track = 'https://www.loomisexpress.com/loomship/Track/TrackResults?t=WAYBILL&s=LSHP29722611#LSHP29722611'

# Run the loop every 5 minutes
while True:
    p = check_progress_and_notify(url_to_track)
    if p == 'break':
        break
    time.sleep(300)  # Sleep for 5 minutes (300 seconds)
