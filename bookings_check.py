import json

data = None
with open("bookings.json", 'r') as file:
    # Load the JSON data from the file
    data = json.load(file)


bookings = data.get("data").get("bookings")

booking_ids = []

for date in bookings:
    for booking in date['bookings']:
        if booking['id'] in booking_ids:
            print(0)
        else:
            booking_ids.append(booking['id'])


unapproved_bookings = data.get("data").get("unapproved_bookings")
unapproved_booking_ids = []
for booking in unapproved_bookings:
    if booking['id'] in unapproved_booking_ids:
        print(0)
    else:
        booking_ids.append(booking['id'])

print(0)