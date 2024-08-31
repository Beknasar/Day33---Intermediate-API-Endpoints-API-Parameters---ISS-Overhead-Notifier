import requests
from datetime import datetime
import smtplib, time

MY_LAT = 42.874622
MY_LONG = 74.569763

my_email = "beknazar.ulanbekuuluu@mail.ru"
password = "x77Nw33zDCX3bGzkYtih"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT -5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    #If the ISS is close to my current position
    if time_now >= sunset or time_now <= sunrise:
        # It's dark.
        return True
# and it is currently dark
# Then send me an email to tell me to look up.


# BONUS: run the code every 60 seconds.
while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.mail.ru") as connection:
            # secure our connection to email server
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="680633@gmail.com",
                msg=f"Subject:Look Up ☝\n\n The ISS is above you in the sky."
            )


