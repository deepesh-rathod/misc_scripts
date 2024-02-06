import re


def extract_offer(text):
    # Regular expression for finding percentage (e.g., 20%)
    percentage_pattern = r"\d+%"
    # Regular expression for finding dollar amount (e.g., $20)
    dollar_pattern = r"\$\d+"

    # Search for percentage offer
    percentage_match = re.search(percentage_pattern, text)
    if percentage_match:
        return percentage_match.group()

    # Search for dollar amount offer
    dollar_match = re.search(dollar_pattern, text)
    if dollar_match:
        return dollar_match.group()

    # Default return if no offer is found
    return "<n>%"
