# motivation_quotes.py

import random

def morning_boost():
    """Generate a quote to boost your morning motivation."""
    quotes = [
        'The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt',
        'Believe you can and you\'re halfway there. - Theodore Roosevelt',
        'Don\'t watch the clock; do what it does. Keep going. - Sam Levenson'
    ]
    return random.choice(quotes)

def daily_grind():
    """Generate a quote to help you push through the daily grind."""
    quotes = [
        'The only way to do great work is to love what you do. - Steve Jobs',
        'Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill',
        'Strive not to be a success, but rather to be of value. - Albert Einstein'
    ]
    return random.choice(quotes)

def persistence():
    """Generate a quote about perseverance."""
    quotes = [
        'Our greatest weakness lies in giving up. The most certain way to succeed is always to try just one more time. - Thomas Edison',
        'It does not matter how slowly you go as long as you do not stop. - Confucius',
        'If you can\'t fly, then run. If you can\'t run, then walk. If you can\'t walk, then crawl. But whatever you do, you have to keep moving forward. - Martin Luther King Jr.'
    ]
    return random.choice(quotes)

def generate_motivation_quote(request):
    """Generate a quote based on the given request."""
    if request == 'morning_boost':
        return morning_boost()
    elif request == 'daily_grind':
        return daily_grind()
    elif request == 'persistence':
        return persistence()
    else:
        return "Sorry, I don't have a quote for that."

if __name__ == "__main__":
    # Test the script with given request
    motivation = ["morning_boost", "daily_grind", "persistence"]
    for item in motivation:
        print(generate_motivation_quote(item))