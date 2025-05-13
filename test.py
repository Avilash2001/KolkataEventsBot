from scraper import get_events_V2

events = get_events_V2()
for event in events:
    print(f"{event['title']} - {event['url']}")

# from scraper import is_in_west_bengal

# test = is_in_west_bengal("Siliguri")
# print(test)