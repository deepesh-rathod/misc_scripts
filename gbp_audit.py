import psycopg2
from psycopg2.extras import RealDictCursor
import secrets_helper
from datetime import datetime, timedelta


def sql():
    global conn, cur
    try:
        db_creds = secrets_helper.get_secrets(prefix="DB_")
        conn = psycopg2.connect(
            host=db_creds["DB_HOST"],
            port=db_creds["DB_PORT"],
            database=db_creds["DB_NAME"],
            user=db_creds["DB_USER"],
            password=db_creds["DB_PASS"],
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        print("Loaded creds from secret manager")
    except Exception as e:
        print("New sql ERROR", e)


def sql_query(query):
    global cur
    try:
        cur.execute(query)
    except:
        sql()
        cur.execute(query)
    conn.commit()


def get_nap_details(uid):
    query = f"""
    SELECT
        title as biz_name,
        phone as phone_number,
        address as street,
        zipcode as zipcode,
        city,
        state
    FROM
        gmb_retool_profile_completion
    WHERE
        uid = '{uid}'
    """
    sql_query(query)
    res = cur.fetchall()
    return dict(res[0]) if len(res) > 0 else None


def get_review_raw_data(uid):
    query = f"SELECT * FROM review_data WHERE uid='{uid}'"
    sql_query(query)
    res = cur.fetchall()
    data = [dict(r) for r in res]
    return data


def get_time_diff_in_hours(datetime_1, datetime_2):

    datetime_format = "%Y-%m-%d %H:%M:%S"

    # datetime1 = datetime.strptime(datetime_1, datetime_format)
    # datetime2 = datetime.strptime(datetime_2, datetime_format)

    difference = datetime_2 - datetime_1

    difference_in_hours = difference.total_seconds() / 3600

    return difference_in_hours


def get_weeks_list(num_weeks):
    today = datetime.today()
    start_of_current_week = today - timedelta(days=today.weekday())
    end_of_current_week = start_of_current_week + timedelta(days=6)
    weeks_list = []
    last_start_date = None

    for week_num in range(num_weeks):
        start_date = start_of_current_week - timedelta(weeks=week_num)
        end_date = end_of_current_week - timedelta(weeks=week_num)
        weeks_list.append((start_date, end_date))

        if week_num == num_weeks - 1:
            last_start_date = start_date

    return weeks_list, last_start_date


def check_date(date, start_date):
    # datetime_format = "%Y-%m-%d %H:%M:%S"
    # datetime1 = datetime.strptime(start_date, datetime_format)
    print(start_date, " | ", date, " || ", start_date > date)
    return start_date > date


def calculate_flat_weeks(data, number_of_weeks):
    weeks, start_date = get_weeks_list(number_of_weeks)
    weeks_count = number_of_weeks - 1
    flat_week_data = []
    for d in data:
        if check_date(start_date, d["date"]):
            while weeks_count > 0:
                print(str(weeks[weeks_count][0]), str(d["date"]))
                print(str(d["date"]), str(weeks[weeks_count][1]))
                print(weeks_count, len(weeks))
                if (
                    check_date(weeks[weeks_count][0], d["date"])
                    and check_date(d["date"], weeks[weeks_count][1])
                    and weeks_count < len(weeks)
                ):
                    weeks_count = weeks_count - 1
                    flat_week_data.append(
                        {"week_start_date": weeks[weeks_count][0], "flatweek": False}
                    )
                    continue

                if check_date(d["date"], weeks[weeks_count][1]):
                    weeks_count = weeks_count - 1
                    print("weeks_count : ", weeks_count)
                    flat_week_data.append(
                        {"week_start_date": weeks[weeks_count][0], "flatweek": True}
                    )

                else:
                    weeks_count = weeks_count - 1

    return flat_week_data


def get_keywords(uid):
    query = f"""
    SELECT
	    name
    FROM
        scheduling.categories
    WHERE
        business_id = '{uid}'
    LIMIT 5
"""
    sql_query(query)
    res = cur.fetchall()
    return [r["name"] for r in res]


def check_keyword_in_review(keywords, raw_review_data):
    keywords_present = []
    for review in raw_review_data:
        if review["comment"] is not None:
            keywords_data = []
            for keyword in keywords:
                if keyword.lower() in review["comment"].lower():
                    keywords_data.append({"keyword": keyword, "present": True})
                else:
                    keywords_data.append({"keyword": keyword, "present": False})

            keywords_present.append(
                {
                    "review_id": review["review_id"],
                    "review": review["comment"],
                    "keywords": keywords_data,
                }
            )
        else:
            keywords_present.append(
                {
                    "review_id": review["review_id"],
                    "review": review["comment"],
                    "keywords": [],
                }
            )

    return keywords_present


def get_reviews_data(uid):
    raw_review_data = get_review_raw_data(uid)
    number_of_reviews = len(raw_review_data)
    avergae_rating = sum([x["rating"] for x in raw_review_data]) / number_of_reviews
    review_reply_count = 0
    review_reply_time_diff = []
    for data in raw_review_data:
        if (
            data.get("review_reply_comment") is not None
            and data.get("review_reply_comment") != ""
        ):
            review_reply_count += 1
            review_reply_time_diff.append(
                get_time_diff_in_hours(
                    data.get("date"), data.get("review_reply_comment_date")
                )
            )
            print(0)
    flat_weeks = calculate_flat_weeks(raw_review_data, 8)
    keywords = get_keywords(uid)
    keywords_in_reviews = check_keyword_in_review(keywords, raw_review_data)

    return {
        "number_of_reviews": number_of_reviews,
        "avergae_rating": avergae_rating,
        "review_reply_count": review_reply_count,
        "review_reply_time_diff": review_reply_time_diff,
        "flat_weeks": flat_weeks,
        "keywords_in_reviews": keywords_in_reviews,
    }


sql()

reviews_data = get_reviews_data("8ec21ca6-33ee-4a4e-ba1c-06264ef1c3eb")

# nap_details = get_nap_details("8ec21ca6-33ee-4a4e-ba1c-06264ef1c3eb")

print(0)
