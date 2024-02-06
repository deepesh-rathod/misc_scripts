from win10toast import ToastNotifier
import requests
import time

while(True):
    toast = ToastNotifier()
    try:
        resp = requests.get("https://chroneinternal.com/api/health_check")
        if resp.status_code==200:
            toast.show_toast(
                "Success",
                "Server is up",
                duration = 5,
                icon_path = "icon.ico",
                threaded = True,
            )
        else:
            toast.show_toast(
                "Fail",
                "Server is down",
                duration = 5,
                icon_path = "icon.ico",
                threaded = True,
            )
            time.sleep(10)
    except Exception as e:
        toast.show_toast(
            "Not Reachable",
            "Server Not Reachable",
            duration = 5,
            icon_path = "icon.ico",
            threaded = True,
        )
        time.sleep(10)
    