def get_cron_expression_from_time(time_str):
    hour, minute = time_str.split(":")
    return f"{int(minute)} {int(hour)} * * *"  # daily at selected time
