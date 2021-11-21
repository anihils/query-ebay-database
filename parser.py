
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

colDelim = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

# TODO: Escape double quotes inside strings, deal with Null values
# Does not include ItemID
def retrieveCategory(item):
    #return str(item.get('Category'))[1:-1].replace('\', u\'', '\n') + '\n'
    return '"' + str(item.get('Category'))[1:-1].replace('"', '""') + '"'

def retrieveUsers(item):
    # Retrieving seller and bidders from item - cannot differentiate using location
    bidders = ""
    seller = '"' + item.get('Seller').get('UserID') + '"|' + item.get('Seller').get('Rating') + '|NULL|none\n'
    #seller = str(item.get('Seller').values()).removeprefix('dict_values([').removesuffix('])') + '\n'
    bids = item.get('Bids') # returns array of bids
    if (not (bids is None)):
        for bid in bids:
            bidder = bid.get('Bid').get('Bidder')
            bidders += '"' + str(bidder.get('UserID')) + '"|' + bidder.get('Rating') + '|"' + str(bidder.get('Location')).replace('"','""') + '"|"' + str(bidder.get('Country')).replace('"','""') + '"\n'
    return seller + bidders
 
def retrieveBids(item):
    bids = ''
    bidslist = item.get('Bids') # returns array of bids
    if (not (bidslist is None)):
        for currentBid in bidslist:
            bid = currentBid.get('Bid')
            bids += '"' + bid.get('Bidder').get('UserID') + '"|' + item.get('ItemID') + '|"' + transformDttm(bid.get('Time')) + '"|' + transformDollar(bid.get('Amount')) + '\n'
    return bids

def retrieveLocation(item):
    return '"' + str(item.get('Location')).replace('"','""') + '"|"' + str(item.get('Country')).replace('"','""') + '"'

def retrieveItem(item):
    currentItem = str(item.get('ItemID') + '|"' + item.get('Name').replace('"','""') + '"|"') + str(item.get('Category'))[1:-1].replace('"', '""') + '"|' + str(len(item.get('Category'))) + '|'

    if not(item.get('Bids') is None): # Null-check for bids
        currentItem += str(item.get('Currently') + '|' + item.get('First_Bid') + '|')
    else:
        currentItem += 'NULL|none|'
    
    currentItem += str(item.get('Number_of_Bids')) + '|' +  str(retrieveLocation(item) + '|"' + transformDttm(item.get('Started')) + '"|"' + transformDttm(item.get('Ends')) + '"|"' + item.get('Seller').get('UserID') + '"|')

    if not(item.get('Buy_Price') is None): # Null-check for buy price
        currentItem += '"' + str(item.get('Buy_Price')) + '"|'
    else:
        currentItem += 'null price|'

    if not(item.get('Description') is None):  # Null-check for description
        currentItem += '"' + item.get('Description').replace('"','""') + '"\n'
    else: 
        currentItem += 'null description\n'
    return currentItem

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file

        # Creating categories.dat file
        catfile = "categories.dat"
        catptr = open(catfile, "a")

        # Creating users.dat file
        userfile = "users.dat"
        userptr = open(userfile, "a")

        # Creating bids.dat file
        bidfile = "bids.dat"
        bidptr = open(bidfile, "a")

        # Creating items.dat file
        itemfile = "items.dat"
        itemptr = open(itemfile, "a")

        for item in items:
            catptr.write(str(item.get('ItemID')) + '|' + retrieveCategory(item) + '\n')
            userptr.write(retrieveUsers(item))
            bidptr.write(retrieveBids(item))
            itemptr.write(retrieveItem(item))

            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            pass
        catptr.close()
        userptr.close()

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)