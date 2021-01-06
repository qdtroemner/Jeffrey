import requests

def getFact():
    r = requests.get('https://uselessfacts.jsph.pl/random.html?language=en')

    data = r.text
    data = r.text.split('</blockquote>')
    data = data[0]
    data = data.split('facts.htm">')
    data = data[1]
    data = data.replace("  ", "")

    return(data)