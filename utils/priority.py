def assign_priority(text):

    text = text.lower()

    if any(word in text for word in [
        "fire",
        "explosion",
        "shock",
        "danger"
    ]):
        return "Critical"

    elif any(word in text for word in [
        "fault",
        "burn",
        "token",
        "offline"
    ]):
        return "High"

    elif any(word in text for word in [
        "billing",
        "reading"
    ]):
        return "Medium"

    return "Low"