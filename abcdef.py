from collections import defaultdict

# Your first list
first_list = [
    {"openDay": "MONDAY", "openTime": {"hours": 10}, "closeDay": "MONDAY", "closeTime": {"hours": 16}},
    {"openDay": "TUESDAY", "openTime": {"hours": 9}, "closeDay": "TUESDAY", "closeTime": {"hours": 18}},
    {"openDay": "WEDNESDAY", "openTime": {"hours": 9}, "closeDay": "WEDNESDAY", "closeTime": {"hours": 18}},
    {"openDay": "THURSDAY", "openTime": {"hours": 9}, "closeDay": "THURSDAY", "closeTime": {"hours": 19}},
    {"openDay": "FRIDAY", "openTime": {"hours": 9}, "closeDay": "FRIDAY", "closeTime": {"hours": 19}},
    {"openDay": "SATURDAY", "openTime": {"hours": 8}, "closeDay": "SATURDAY", "closeTime": {"hours": 17}}
]

# Your second format
second_format = {
    "MONDAY": [{"open_time": "9:00:00", "close_time": "17:00:00"}],
    "SUNDAY": [{"open_time": "9:00:00", "close_time": "17:00:00"}],
    "TUESDAY": [{"open_time": "9:00:00", "close_time": "12:00:00"}, {"open_time": "14:00:00", "close_time": "17:00:00"}],
    "SATURDAY": [{"open_time": "9:00:00", "close_time": "17:00:00"}],
    "THURSDAY": [{"open_time": "9:00:00", "close_time": "17:00:00"}],
    "WEDNESDAY": [{"open_time": "9:00:00", "close_time": "17:00:00"}]
}

# Convert the first format to the second format
result = defaultdict(list)

for entry in first_list:
    day = entry["openDay"]
    open_time = entry["openTime"]["hours"]
    close_time = entry["closeTime"]["hours"]
    result[day].append({"open_time": f"{open_time}:00:00", "close_time": f"{close_time}:00:00"})

# Ensure the order of days is the same as in the second format
final_result = {day: result[day] for day in second_format.keys()}

# Print the result
print(final_result)
