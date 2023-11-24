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



# delta_str_1 = "1 hour 11 mins"
# delta_str_2 = "47 mins"
# delta_str_3 = "2 hours 17 mins"
# delta_str_4 = "1 day 12 hours 37 mins"


# time_delta_1 = duration_to_delta(delta_str_1)
# time_delta_2 = duration_to_delta(delta_str_2)
# time_delta_3 = duration_to_delta(delta_str_3)
# time_delta_4 = duration_to_delta(delta_str_4)

# print("Time Delta 1:", time_delta_1)
# print("Time Delta 2:", time_delta_2)
# print("Time Delta 3:", time_delta_3)
# print("Time Delta 4:", time_delta_4)