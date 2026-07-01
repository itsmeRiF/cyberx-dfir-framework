def get_severity(event_id):

    critical = ["4625", "4624", "1102", "7045"]
    warning = ["4634", "4647"]

    if event_id in critical:
        return "high"

    if event_id in warning:
        return "medium"

    return "low"