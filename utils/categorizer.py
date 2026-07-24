def categorize_complaint(text):

    text = text.lower()

    if any(word in text for word in [
        "token",
        "recharge",
        "credit"
    ]):
        return "Token Issue"

    elif any(word in text for word in [
        "burn",
        "fire",
        "smoke",
        "fault"
    ]):
        return "Meter Fault"

    elif any(word in text for word in [
        "bill",
        "billing",
        "charge"
    ]):
        return "Billing"

    elif any(word in text for word in [
        "install",
        "installation",
        "meter"
    ]):
        return "Installation"

    elif any(word in text for word in [
        "light",
        "power",
        "electricity",
        "supply"
    ]):
        return "Power Supply"

    return "Others"