from datetime import timedelta
import re

def duration_to_delta(duration_str):
    pattern = r'(?:(?P<days>\d+)\s*days?)?\s*(?:(?P<hours>\d+)\s*hours?)?\s*(?:(?P<minutes>\d+)\s*mins?)?'
    matches = re.search(pattern, duration_str)
    if not matches:
        return timedelta()  # Return 0 duration if no matches

    duration_parts = matches.groupdict(default='0')
    days = int(duration_parts['days'])
    hours = int(duration_parts['hours'])
    minutes = int(duration_parts['minutes'])

    return timedelta(days=days, hours=hours, minutes=minutes)