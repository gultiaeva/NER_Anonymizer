'''
Если ничего не будет работать, это нас спасет
'''
from natasha import NamesExtractor
from natasha import LocationExtractor
from natasha import OrganisationExtractor
from natasha import DatesExtractor
from natasha import AddressExtractor


names_extr = NamesExtractor()
locs_extr = LocationExtractor()
org_extr = OrganisationExtractor()
dates_extr = DatesExtractor()
address_extr = AddressExtractor()


def recognize_names(text):
    tmp = text
    matches = names_extr(text)
    for match in matches:
        start, finish = match.span
        tmp = tmp.replace(text[start:finish], "[NAME]")
    return tmp


def recognize_locs(text):
    tmp = text
    matches = locs_extr(text)
    for match in matches:
        start, finish = match.span
        tmp = tmp.replace(text[start:finish], "[LOC]")
    return tmp


def recognize_org(text):
    tmp = text
    matches = org_extr(text)
    for match in matches:
        start, finish = match.span
        tmp = tmp.replace(text[start:finish], "[ORG]")
    return tmp


def recognize_dates(text):
    tmp = text
    matches = dates_extr(text)
    for match in matches:
        start, finish = match.span
        tmp = tmp.replace(text[start:finish], "[DATE]")
    return tmp


def recognize_address(text):
    tmp = text
    matches = address_extr(text)
    for match in matches:
        start, finish = match.span
        tmp = tmp.replace(text[start:finish], "[ADDRESS]")
    return tmp


def recognize_all(text):
    processed_text = recognize_names(
        recognize_address(
            recognize_dates(
                recognize_locs(
                    recognize_org(text)))))
    return processed_text
