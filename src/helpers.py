import datetime, time

def cocoa_readable(timestamp: int):
    return datetime.datetime.fromtimestamp((timestamp / 1_000_000_000) + 978307200)


def cocoa_now():
    # apple's timestamps use nanoseconds since jan 1 2001
    now = datetime.datetime.now()
    now_s = time.mktime(now.timetuple())
    time_in_nanoseconds = (now_s - 978307200) * 1_000_000_000 # subtract 1970 to 2001, then multiply by 10^9 to convert to nanoseconds
    return time_in_nanoseconds