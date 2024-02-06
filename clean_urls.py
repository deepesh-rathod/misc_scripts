import re

data = """
          .get(`${base_url}/get_app_square_oauth_url?place_id=${place_id}&uid=${uid}`)
      .post(`${base_url}/app_square_gmb_mapping`, 
        `${base_url}/send_slack_notification_pics?place_id=${place_id}&email=${email}&biz_name=${biz_name}&uid=${uid}`,
      const response = await axios.get(`${base_url}/chrone_app/get-ec-data-consent?place_id=${placeID}&uid=${uid}`);
      await axios.post(`${base_url}/chrone_app/send-review-data`, payload);
  const response = await axios.get(`${base_url}/google/get-user-details?${key}=${token}`);
      .post(`${base_url}/register-notification-device`,
        const url = `${messageBaseUrl}/review/${location}`;
      .post(`${node_url}/tags/services`,
        .post(`${node_url}/tags/services`,
            .get(`${base_url}/review_reply?name=${data.name}&reply=${replyText}&email=${email}&uid=${uid}`)
            .get(`${base_url}/review_reply_delete?name=${data.name}&email=${email}&uid=${uid}`)
    .get(`${base_url}/google/gmb-profile-images?email=${email}&place_id=${place_id}&uid=${uid}&all=true`)
    .post(`${base_url}/get-reviews`,
    const res = await axios.get(`${internalToolBaseUrl}/api/website-feedback?uid=${uid}`);
      url: `${internalToolBaseUrl}/api/website-feedback?uid=${uid}`,
      url: `${internalToolBaseUrl}/api/website-feedback?uid=${data?.uid}`,
      url: `${internalToolBaseUrl}/api/website-feedback?uid=${uid}`,
    const res = await axios.get(`${base_url}/website-url?uid=${uid}`);
    .get(`${base_url}/chrone_app/check-oauth?email=${email}&uid=${uid}`)
      .get(`${internalToolBaseUrl}/sendbird/unread_message?user_id=${channel?.uid}`)
      .post(`${internalToolBaseUrl}/sendbird/get_channel_mapping`, payload)
    const res = await axios.post(`${base_url}/account-verification-status`, { uid });
  const response = await axios.get(`${base_url}/google/get-user-details?${key}=${token}`);
      .post(`${base_url}/chrone/app-login-save`, {
      .post(`${base_url}/register-notification-device`
  const profile_views_resp = await axios.get(`${base_url}/chrone/profile-metrics?place_id=${place_id}&uid=${uid}`);
  const total_leads_resp = await axios.get(`${base_url}/chrone/leads-metrics?place_id=${place_id}&uid=${uid}`);
    `${base_url}/chrone/website-visits-metrics?place_id=${place_id}&uid=${uid}`
  const refer_url_resp = await axios.get(`${base_url}/chrone/referral-link?place_id=${place_id}&uid=${uid}`);
  let url = `${node_url}/schedule/bookings/list?id=${uid}&start_date=${startDate}`;
    const response = await axios.get(`${node_url}/schedule/customer/retrieve-all?id=${customerId}`);
    const response = await axios.get(`${node_url}/schedule/customer/business/all?business_id=${uid}`);
  const url = `${node_url}/schedule/notes/create-note`;
  const url = `${node_url}/schedule/customer/create-customer`;
  const url = `${node_url}/schedule/${status}?id=${id}`;
  const url = `${node_url}/schedule/bookings/create-booking`;
  const url = `${node_url}/schedule/bookings/retrieve?id=${bookingId}`;
  const url = `${node_url}/schedule/bookings/update-booking`;
  const url = `${node_url}/schedule/business/update-business?id=${id}`;
  const url = `${node_url}/schedule/customer/create-customer/bulk?business_id=${uid}`;
  const url = `${node_url}/schedule/customer/update-customer?id=${id}`;
  const url = `${node_url}/schedule/notes/update-note?id=${noteId}`;
    const response = await axios.get(`${node_url}/schedule/service/list/all?business_id=${uid}`);
    const response = await axios.get(`${node_url}/schedule/status?id=${uid}`);
    .put(`${base_url}/leads/update-leads`, data)
    .get(`${base_url}/chrone_app/get-leads-count?place_id=${place_id}&uid=${uid}`)
    .post(`${base_url}/leads/table`,
    .post(`${node_url}/tags/services`, { data: payload })
    .get(`${node_url}/banner/website-publish-data?uid=${uid}`)
    .get(`${node_url}/banner/banner-details?uid=${uid}`)
    .post(`${node_url}/banner/update-banner-details`, { data: payload })
    .put(`${base_url}/chrone_app/add-ec-data`, data)
    .get(`${base_url}/chrone_app/get-review-sp-preferences?uid=${uid}`)
    .post(`${base_url}/chrone_app/update-review-preferences`, data)
    .get(`${base_url}/chrone_app/get-ec-data-consent?uid=${uid}`)
    .post(`${base_url}/chrone_app/send-review-data?uid=${uid}`, data)
"""

# Extract all URLs between the backticks
urls = re.findall(r"`(.*?)`", data)

# Clean up the URLs (you can enhance this as per your need)
cleaned_urls = set()  # Using a set to keep distinct URLs
for url in urls:
    # Replacing all placeholders with a generic placeholder
    cleaned_urls.add(url.replace("{","|").replace("}","|"))

# Print cleaned URLs

urls = """"""
for url in cleaned_urls:
    urls += url + "\n"

print(cleaned_urls)
