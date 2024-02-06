from ast import Name
import boto3

# Initialize the Boto3 client for EventBridge
client = boto3.client("scheduler")


def fetch_and_update_schedule(schedule_name):
    # Fetch the schedule by its name
    try:
        response = client.get_schedule(Name=schedule_name)
    except client.exceptions.ResourceNotFoundException:
        print(f"Schedule not found : {schedule_name}")
        return

    response["Target"]["Input"] = response["Target"]["Input"].replace(
        "10829, Bloomingdale Avenue, Riverview, Hillsborough County",
        "9321 Goldenrod rd. Unit A Thonotosassa, fl 33592",
    )

    updated_schedule = {
        "Name": response["Name"],
        "GroupName": response["GroupName"],
        "ScheduleExpression": response["ScheduleExpression"],
        "Target": response["Target"],
        "FlexibleTimeWindow": {
            "Mode": "OFF",
        },
        "ActionAfterCompletion": "DELETE",
    }

    try:
        updated_response = client.update_schedule(
            Name=response["Name"],
            GroupName=response["GroupName"],
            ScheduleExpression=response["ScheduleExpression"],
            Target=response["Target"],
            FlexibleTimeWindow={
                "Mode": "OFF",
            },
            ActionAfterCompletion="DELETE",
        )
        print(f"SUCCESSFULLY UPDATED FOR : {schedule_name}")
    except Exception as e:
        print(f"ERROR UPDATING : {schedule_name}")


# Example usage


uuid_list = [
    "1e03590a-739c-4004-b16f-31e008ecdabf",
    "dd45975f-5b12-4626-8735-c1d4445670b8",
    "92a54308-7fad-45e3-9cf2-9f8635625111",
    "acce4709-c212-4b20-ad6e-81f249656827",
    "79f1eb85-fdcf-4e18-b359-8a9fd4086c46",
    "6c2cec16-2bf2-4227-a2a4-9471e7ec7678",
]

# schedule_name = 'a0373d0e-a956-48fb-9977-51e173cd3a61'
for uid in uuid_list:
    fetch_and_update_schedule(uid)


# Schedule not found : fe60a7f9-fd44-432a-a99b-9cd59a0b4eae
# Schedule not found : 0ce186c3-84db-4b18-9ada-1006cf8a7a34
# SUCCESSFULLY UPDATED FOR : a0373d0e-a956-48fb-9977-51e173cd3a61
# SUCCESSFULLY UPDATED FOR : 9cfe439b-3253-4eb1-a40e-7123440c3859
# Schedule not found : 3f891950-d6f5-4bfa-9e57-864e637c3633
# Schedule not found : 9d8df1d3-cb24-4c82-8688-1300c9a6aebb
# Schedule not found : b866f536-a5df-4da2-a954-0db5fe5ce1f1
# Schedule not found : d18baa60-01fc-402a-8e68-f6b1363f03e4
# Schedule not found : 98ebd277-8ed7-40cf-a437-5856b8d3c919
# Schedule not found : 84c043ae-3789-4cf5-aedb-13f7bce84d3a
# SUCCESSFULLY UPDATED FOR : 32b47f49-7776-4451-81ea-9747964c42e0
# SUCCESSFULLY UPDATED FOR : 40d56e35-a221-424d-b54d-139a607754d5
# SUCCESSFULLY UPDATED FOR : dcc92cce-ddf0-4ea8-826c-c8e5d9e55eab
# SUCCESSFULLY UPDATED FOR : 281ed52b-e1c6-48bb-aa92-afc11091db40
# SUCCESSFULLY UPDATED FOR : 05940881-6cdd-4b6b-a510-0c0a4483117a
# SUCCESSFULLY UPDATED FOR : b417e77b-117e-4927-aa4a-529d80f6b5fc
# SUCCESSFULLY UPDATED FOR : 7bb23576-1f9e-4bb2-953f-1f1bfb68899d
# SUCCESSFULLY UPDATED FOR : 4fe67db4-4eb9-4aed-b55c-18723c110330
# SUCCESSFULLY UPDATED FOR : 7ceee412-a4f1-4e0b-ae4a-410a76c6e8e3
# SUCCESSFULLY UPDATED FOR : 267949bd-0d91-4417-9e6e-7bd84c68ed37
# SUCCESSFULLY UPDATED FOR : f4c41066-0cc0-4144-a37e-ff380688768e
# SUCCESSFULLY UPDATED FOR : 50ffe389-3c51-4d47-b8f5-709e7d31c532
# Schedule not found : 7a2a0085-61ac-4a41-be9b-51f4ab565b3c
# SUCCESSFULLY UPDATED FOR : b980dc22-f834-4c15-ae4f-5339cccb15b1
# SUCCESSFULLY UPDATED FOR : 71001f1a-bf95-4969-ab35-02a00535053a
# Schedule not found : 9952bbc5-cf7f-41a3-8c17-8a73e53db5b5
# Schedule not found : 27caa602-a3de-40c3-b4d0-9f09fa0388b4
# Schedule not found : aae23248-ce5e-44db-913a-218a44537a0d
# Schedule not found : 44028b38-c092-46ae-af27-e59f73da0027
# Schedule not found : 3f17dcad-65f7-4478-a482-7a803875ba4b
# Schedule not found : fda4e964-7ce8-4bc5-b9dd-8114834a5869
# Schedule not found : 442d80f9-3a22-4f8f-aee1-0ee133bdcd86
# Schedule not found : b159a053-2628-496a-8964-fa0775507695
# Schedule not found : 74dcb6cb-40d0-4341-8c5f-f3b25f8d8dde

# SUCCESSFULLY UPDATED FOR : 1e03590a-739c-4004-b16f-31e008ecdabf
# SUCCESSFULLY UPDATED FOR : dd45975f-5b12-4626-8735-c1d4445670b8
# SUCCESSFULLY UPDATED FOR : 92a54308-7fad-45e3-9cf2-9f8635625111
# SUCCESSFULLY UPDATED FOR : acce4709-c212-4b20-ad6e-81f249656827
# SUCCESSFULLY UPDATED FOR : 79f1eb85-fdcf-4e18-b359-8a9fd4086c46
# SUCCESSFULLY UPDATED FOR : 6c2cec16-2bf2-4227-a2a4-9471e7ec7678
