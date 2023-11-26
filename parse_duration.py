from datetime import timedelta


def duration_to_delta(duration:str):
    # split the string by space
    component_duration = duration.split()

    days, hours, mins = 0, 0, 0
    for i, e in enumerate(component_duration):
        if e == 'day' or e =='days':
            days = int(component_duration[i-1])
        elif e == 'hour' or e== 'hours':
            hours = int(component_duration[i-1])
        elif e == 'min' or e== 'mins':
            mins = int(component_duration[i-1])

    return timedelta(days=days, hours=hours, minutes=mins )
