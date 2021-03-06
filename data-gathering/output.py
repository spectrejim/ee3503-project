'''
Output module.

This module handles the output of data to all possible solutions.
It is designed to primarily handle CSV and REST API but can be adapted.
'''
import os
import pathlib

USE_CSV = True
open_files = []


def open_file(file, headers=''):
    '''Open an output file if not open or find the file descriptor.

    This function searches through open_files to see if a file has
    been previously opened. If found, the file descriptor is returned.
    If the file is not found to be open, it is opened and the CSV
    headers are written to the top of the file, then it's added to the
    open_files list.

    Arguments:
        file {[type]} -- The name of the file to be opened

    Keyword Arguments:
        headers {str} -- CSV headers to prepend to a file (default: {''})

    Returns:
        file descriptor -- The function return a file descriptor or None
            if the file cannot be opened.
    '''
    global open_files

    for of in open_files:
        if file in of.name:
            return of

    try:
        f = open(file, "w")
        open_files.append(f)
        if headers:
            f.write(headers)
        return f
    except Exception as e:
        print(e)

    return None


def ratings(id,rating,user_ratings_total):
    '''
    `ratings` formats the function parameters in a way where they
    can be stored in CSV or sent to an API.

    Arguments:
        id {int|string} -- Unique ID for the hotel
        rating {float} -- The average user rating.
        user_ratings_total {int} -- Total ratings given for a hotel.
    '''
    global USE_CSV

    if USE_CSV:
        file = "ratings.csv"
        headers = "ID,Rating,Ratings Total\n"
        f = open_file(file, headers)
        if f == None:
            return


        '''
        Not the best code here, but it's DRY and has a
        single responsibility. See below for more examples.
        '''
        f.write(id + "," + str(rating) +","+ str(user_ratings_total) +"\n")
    else:
        '''The condition used to send the data to a RESTful API'''
        pass


def reviews(id,reviews):
    '''
    `reviews` accepts a dictionary of information and gathers the
    required pieces based on the data model. Data that is not
    required is silently discarded and not stored in CSV or sent
    to the API.

    Arguments:
        id {int|string} -- Unique ID for the hotel
        reviews {dictionary} -- Dictionary of data to process
    '''
    global USE_CSV

    if reviews == None:
        return

    if USE_CSV:
        file = "reviews.csv"
        headers = "ID,Author,Rating,Text,Time\n"
        f = open_file(file, headers)
        if f == None:
            return


        '''
        The following block of code would not be considered
        DRY since the `f.write()` is repeated for each field.
        If the field order changes or new fields are added
        this must be reworked to match.

        Review the `hotels()` function for a better example.
        '''
        for review in reviews:
            f.write(id) # Start with our ID
            f.write(","+review['author_name'])
            f.write(","+str(review['rating']))
            f.write(","+review['text'][:25])
            f.write(","+str(review['time']))
            f.write("\n") # End with a newline character
    else:
        '''The condition used to send the data to a RESTful API'''
        pass


def hotels(id,data):
    '''
    `hotels` accepts a dictionary of information and gathers the
    required pieces based on the data model. Data that is not
    required is silently discarded and not stored in CSV or sent
    to the API.

    Arguments:
        id {int|string} -- Unique ID for the hotel
        data {dictionary} -- Dictionary of data to process
    '''
    global USE_CSV
    fields = ['name', 'formatted_address', 'formatted_phone_number',
        'vicinity', 'types', 'place_id', 'geometry']

    # print(f"DEBUG: hotels()")
    # print(data)

    if USE_CSV:
        file = "hotels.csv"
        headers = "ID,Name,Address,Phone,Vicinity\n"
        f = open_file(file, headers)
        if f is None:
            return

        f.write(data['place_id'])  # Start with our ID
        for field in fields:  # Write each of the other field
            # print(f"hotels() DEBUG: Processing field {field}")
            d = ''
            if field in data:
                d = data[field]
            if field == 'types':
                d = "|".join(data[field]) # pipe separated list
            # print(f"hotels() DEBUG: {field} - d={d}")
            f.write("," + str(d))
        f.write("\n")  # End with a newline character
    else:
        '''The condition used to send the data to a RESTful API'''
        pass
