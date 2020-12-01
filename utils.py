def get_input(prompt, valids):
    """ Prompts the user for some input, and repeats the question if the response is not within the list of valid responses"""
    t = ''
    while t not in valids:
        t = input(prompt + '\n>>> ').title()
        if t in valids:
            return t
        else:
            print('Please make a valid selection')

def mode_text(desc, vals):
    """ Returns a boilerplate description of the mode, or modes if the data has more than one mode"""
    if len(vals) == 1:
        text = 'The most common {} is {}'.format(desc, vals[0])
    else:
        ans = ' and '.join(vals)
        text = 'The most common {} is a tie between {}'.format(desc, ans)
    
    return text

def format_time(delta):
    """Formats a timedelta into '_ days, _ hours, _ minutes, _ seconds' with the first two omitted if they are zero
    Honour code: based on a combination of solutions from here:
    https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds"""
    days = delta.days
    tot_s = delta.seconds
    
    hours = tot_s // (60 * 60)
    rem_s = tot_s % (60*60)
    
    mins = rem_s // 60
    secs = rem_s % 60
    
    text = ''
    if days > 0:
        text += str(days) + ' days, '
    if hours > 0:
        text += str(hours) + ' hours, '
    text += str(mins) + ' minutes, ' + str(secs) + ' seconds'
    
    return text


def table_builder(headers, rows):
    """ Takes a dictionary (=rows) and returns it in the form of a table, with headers"""
    width1 = max(len(headers[0]),max(len(str(x)) for x in rows.keys()))
    width2 = max(len(headers[1]),max(len(str(x)) for x in rows.values()))
    """ Honour code: the two lines above are based on the third solution in 
    https://stackoverflow.com/questions/10895567/find-longest-string-key-in-dictionary"""
    
    text = ''
    underscores = '-' * (2 + width1 + 3 + width2 + 2) 
    text += underscores
    text += '\n| ' + headers[0].ljust(width1,' ') + ' | ' + headers[1].ljust(width2,' ') + ' |' 
    text += '\n' + underscores

    for x, y in rows.items():
        text += '\n| ' + str(x).ljust(width1, ' ') + ' | ' + str(y).rjust(width2,' ') + ' |'

    text += '\n' + underscores
    
    return text

def get_int(prompt, min=None, max=None):
    """Prompts the user to input an integer, and asks the question again if the response is not a number, or (optionally)
    is not within the min and/or max values provided."""
    while True:
        val = input(prompt + '\n >>> ')
        try:
            val = int(val)
        except:
            val = input('Invalid response - please input your answer as a whole number.')
            continue
        if min:
            if val < min:
                print('Response is lower than expected.')
                continue
        if max:
            if val > max:
                print('Response is greater than expected.')
                
        return val

def main():
    print('This file contains a number of functions for use with bikeshare.py')

if __name__ == "__main__":
    main()
