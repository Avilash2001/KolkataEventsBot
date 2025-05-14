from scraper import get_events_V2

events = get_events_V2()
for event in events:
    print(f"{event['title']} - {event['url']}")