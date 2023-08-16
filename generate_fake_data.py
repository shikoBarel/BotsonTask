from faker import Faker
import json
import sys

fake = Faker()

sys.stdout.write("Sending fake events to Logstash...\n")
for _ in range(1000):
    user_geo = fake.country()
    botName = fake.name()
    event_rate = fake.random_number(digits=4)
    event = {
        "user_geo": user_geo,
        "botName": botName,
        "event_rate": event_rate,
    }
    sys.stdout.write(json.dumps(event) + "\n")
