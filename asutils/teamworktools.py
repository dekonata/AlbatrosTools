import datetime, json, sys
import requests
from pprint import pprint

install = 'https://albatrosgolf.teamwork.com'
key = 'F4iqOn3xrqZmsQ5tW1IHX9nXH5y44rvSGR2MQGM5xSQAZVXe6A'


# Helper methods so we don't have to add the installation & authentication
def _get(u, **p):
    return requests.get(install + u, auth=(key, ''), **p)


def _post(u, **p):  # noqa: W291
    return requests.post(install + u, auth=(key, ''), **p)


def _delete(u, **p):
    return requests.delete(install + u, auth=(key, ''), **p)


def _put(u, **p):
    return requests.put(install + u, auth=(key, ''), **p)


def get_ticket_search(clubname):
    ''' Searches for all ticket by club name via Teamworks desk API
    '''

    r = _get(f'/desk/v1/tickets/search.json', params={
        'search': clubname
        })  # noqa: E123
    if r.status_code != 200:
        print('error: status code is', r.status_code)
    return r.json()


def get_max_ticket_id(clubname):
    '''
    Runs get_ticket_search function on Teamworks API to return JSON type dictionary
    Adds all ticket_id in ticket id list and finds created date for highest ticket id
    Returns dictionary with highest ticket id and creation date for club'''
    club_tickets = get_ticket_search(clubname)
    ticket_ids = []
    for tickets in club_tickets['tickets']:
         ticket_ids.append(tickets['id'])
    for tickets in club_tickets['tickets']:
        if tickets['id']==max(ticket_ids):
            created = tickets['createdAt']
            subject = tickets['subject']
    return {"ticket_id" : max(ticket_ids), "created": created, "subject": subject}


if __name__ == "__main__":
    ticket_id = get_max_ticket_id('Barberton')
    print(ticket_id["ticket_id"])
    print(ticket_id["created"])
    print(ticket_id["subject"])



