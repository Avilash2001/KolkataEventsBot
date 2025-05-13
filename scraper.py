import requests
from bs4 import BeautifulSoup


def get_geolocation_info(place):
    url = f"https://nominatim.openstreetmap.org/search"
    params = {
        'q': place,
        'format': 'json',
        'limit': 1
    }

    response = requests.get(url, params=params, headers={
                            "User-Agent": "Mozilla/5.0"})
    if response.status_code == 200 and response.json():
        result = response.json()[0]
        return {
            "display_name": result.get("display_name"),
        }
    return None


def is_in_west_bengal(location_text):
    location_text = location_text.lower()
    info = get_geolocation_info(location_text)
    if not info:
        return False
    name = info.get("display_name", {})
    return "west bengal" in name.lower()


def extract_events_from_devfolio():
    url = "https://devfolio.co/hackathons"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch page.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    cards = soup.select('div[class*="HackathonCard__StyledCard"]')

    for card in cards:
        try:
            title_tag = card.find("h3")
            if not title_tag:
                continue
            title = title_tag.text.strip()

            info = card.find_all('p')

            mode = None

            for i in info:
                text = i.text.lower()
                if "ended" in text:
                    continue
                elif "online" in text:
                    mode = i.text.strip()
                elif "offline" in text:
                    mode = i.text.strip()

            links = card.find_all('a')

            event_url = None
            for link in links:
                href = link.get('href')
                if href and "devfolio.co" in href:
                    event_url = href
                    break
            if not event_url:
                continue
            event_url = event_url.split("?")[0]  # Remove any query parameters

            eventUrlResponse = requests.get(event_url, headers=headers)
            if eventUrlResponse.status_code != 200:
                print(f"Failed to fetch event URL: {event_url}")
                continue

            eventUrlSoup = BeautifulSoup(eventUrlResponse.text, "html.parser")

            details = eventUrlSoup.select(
                'ul[class*="HackathonCard-style__Info"]')

            date = None
            location = None

            for detail in details:
                date = detail.find_all('li')[0].find_all('p')[1].text.strip()
                location = detail.find_all('li')[1].find_all('p')[
                    1].text.strip()

            if not date or not location or not mode or not title or not event_url:
                continue

            # if mode == "Offline" and not is_in_west_bengal(location):
            if not is_in_west_bengal(location):
                continue
            else:
                print(f"Event {title} is in West Bengal: {location}")

            events.append({
                "title": title,
                "start_date": date,
                "location": location,
                "mode": mode,
                "url": event_url
            })
        except Exception as e:
            print("Skipping a card due to error:", e)

    return events
