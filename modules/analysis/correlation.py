def detect_patterns(events):

    patterns = []

    event_ids = [e.event_id for e in events]

    # brute force detection
    if event_ids.count("4625") > 5:
        patterns.append("Possible brute force attack detected")

    # successful login after failures
    if "4625" in event_ids and "4624" in event_ids:
        patterns.append("Failed logins followed by successful login")

    # privilege escalation
    if "4672" in event_ids:
        patterns.append("Admin privilege usage detected")

    return patterns