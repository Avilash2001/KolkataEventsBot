from scraper import extract_events_from_devfolio

events = extract_events_from_devfolio()
for event in events:
    print(f"{event['title']} - {event['url']}")

# from scraper import is_in_west_bengal

# test = is_in_west_bengal("Siliguri")
# print(test)