import requests
from icalendar import Calendar
import urllib2

API_KEY = "a61fa4b1ad81a9631d01009359b04f37"
OAUTH_TOKEN = "854d2704a2a50f3beb389837c8e9025b5ce265c925a2ca6246b4e0cab1276a51"

def findBoard():

    get_boards_url = "https://api.trello.com/1/members/me/boards?key=" + API_KEY + "&token=" + OAUTH_TOKEN + "&response_type=token"

    r = requests.get(get_boards_url)

    board = False

    for boards in r.json():

        board_id = ""
        board_name = ""

        for key, value in boards.items():

            if key == "id":

                board_id = value

            elif key == "name":

                board_name = value

        if board_name == "Talks":

            print("Found board.")

            return board_id

        else:

            print("Didn't find board.")

            return False

def findList(board_id):

    get_lists_url = "https://api.trello.com/1/boards/" + board_id + "/lists?key=" + API_KEY + "&token=" + OAUTH_TOKEN + "&response_type=token"

    r = requests.get(get_lists_url)

    for lists in r.json():

        list_id = ""
        list_name = ""

        for key, value in lists.items():

            if key == "id":

                list_id = value

            elif key == "name":

                list_name = value

        if list_name == "Upcoming talks":

            print("Found list.")

            return list_id

        else:

            print("Didn't find list.")

            return False

def findCards(list_id):

    get_cards_url = "https://api.trello.com/1/lists/" + list_id + "/cards?key=" + API_KEY + "&token=" + OAUTH_TOKEN + "&response_type=token"

    list_of_cards = []

    r = requests.get(get_cards_url)

    for cards in r.json():

        card_id = ""
        card_name = ""
        card_due = ""
        card_desc = ""

        for key, value in cards.items():

            if key == "id":

                card_id = value

            elif key == "name":

                card_name = value

            elif key == "due":

                card_due = value

            elif key == "desc":

                card_desc = value

        list_of_cards.append([card_id, card_name, card_due, card_desc])

    if len(list_of_cards) > 0:
        return list_of_cards

    else:

        return False

def getEMBLTalks(list_id, list_of_cards):

    get_embl_events = "https://www-db.embl.de/jss/servlet/de.embl.bk.seminarlist.ServeSeminarAsICal?dutystationID=1&seminarTypeID=0&timeFrame=0"

    req = urllib2.Request(get_embl_events)
    response = urllib2.urlopen(req)
    data = response.read()

    cal = Calendar.from_ical(data)

    for event in cal.walk('vevent'):

        try:

            date = event.get('dtstart').dt

        except:

            pass

        try:

            summery = event.get('summary')

        except:

            pass

        try:

            description = event.get('description')

        except:

            pass

        event_name = summery + " @ EMBL"

        if not "To be announced" in event_name:

            if not any(card[1] == event_name for card in list_of_cards):

                r = requests.post("https://api.trello.com/1/cards?key=" + API_KEY + "&token=" + OAUTH_TOKEN + "&name=" + event_name + "&idList=" + list_id + "&due=" + str(date) + "&desc=" + description)
                print("Added card.")

if __name__ == '__main__':

    board_id = findBoard()

    if board_id:

        list_id = findList(board_id)

        list_of_cards = findCards(list_id)

        if list_of_cards:

            getEMBLTalks(list_id, list_of_cards)
