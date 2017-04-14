import random
responses = ["As I See It Yes.", "Ask Again Later.", "Better Not Tell You Now.", "Cannot Predict Now.", "Concentrate",
             "Ask Again.", "Don't Count On It.", "It Is Certain.", "It Is So.", "Most Likely.", "My Reply Is No.",
             "My Sources Say No.", "Outlook Good.", "Outlook Not So Good.", "Try Again.", "Signs Point to Yes.",
             "Very Doubtful.", "Without A Doubt.", "Yes.", "Yes - Definitely.", "You May Rely On It "]


def main():
    return [["text", "**" + random.choice(responses) + "**"]]
