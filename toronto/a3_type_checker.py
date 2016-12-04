import builtins

# Check for use of functions print and input.

# IMPORTANT!
# If you are getting this error message here:
# line 11, in <module>
#     our_print = print
# invalid syntax: <string>, line 11, pos 21
# Then you are using the wrong version of Python! Make sure you have Python 3!
our_print = print
our_input = input


def disable_print(*args):
    raise Exception("You must not call print anywhere in your code!")


def disable_input(*args):
    raise Exception("You must not call input anywhere in your code!")


builtins.print = disable_print
builtins.input = disable_input


import tweets

# tweets.extract_mentions
result = tweets.extract_mentions('@AndreaTantaros Statement Regarding British Referendum on E.U. Membership')
assert isinstance(result, list), \
    '''tweets.extract_mentions should return a list, but returned {0}\n'''.format(type(result))
try:
    assert isinstance(result[0], str), \
        '''tweets.extract_mentions should return a list of strings, but the first item of the list returned was a {0}
        '''.format(type(result[0]))
except IndexError:
    assert False, \
      '''The list returned by extract_mentions was empty and should have contained data.\n'''

# tweets.extract_hashtags
result = tweets.extract_hashtags('Statement Regarding British Referendum on E.U. Membership #DemsInPhilly')
assert isinstance(result, list), \
    '''tweets.extract_hashtags should return a list, but returned {0}\n'''.format(type(result))
try:
    assert isinstance(result[0], str), \
        '''tweets.extract_hashtags should return a list of strings, but the first item of the list returned was a {0}
        '''.format(type(result[0]))
except IndexError:
    assert False, \
        '''The list returned by extract_hashtags was empty and should have contained data.\n'''

# tweets.count_words
word_d = {'statement': 1, 'regarding': 1}
result = tweets.count_words('Statement Regarding British Referendum', word_d)
assert isinstance(result, type(None)), \
    '''tweets.count_words should return None, but returned {0}\n'''.format(type(result))
assert len(word_d) == 4, \
    '''tweets.count_words should modify the argument dictionary\n'''

# tweets.common_words
word_d = {'statement': 10, 'regarding': 1}
result = tweets.common_words(word_d, 1)
assert isinstance(result, type(None)), \
    '''tweets.common_words should return None, but returned {0}\n'''.format(type(result))
assert len(word_d) == 1, \
    '''tweets.common_words should modify the argument dictionary'''

# tweets.read_tweets
try:
    result = tweets.read_tweets('short_data.txt')
    assert isinstance(result, dict), \
        '''tweets.read_tweets should return a dict, but returned {0}\n'''.format(type(result))
    key = list(result.keys())[0]
    assert isinstance(key, str), \
        '''tweets.read_tweets should contains strings as keys, but the key we checked was a {0}
        '''.format(type(key))
    assert isinstance(result[key], list), \
        '''tweets.read_tweets should contains lists as values, but the value we checked was a {0}
        '''.format(type(result[key]))
except FileNotFoundError:
    assert False, \
        '''The typechecker uses the data file 'short_data.txt'. Please make sure it is in the same directory as
        your 'tweets.py' file and the typechecker.'''
except IndexError:
    assert False, \
        '''The dictionary returned by read_tweets was empty and should have contained data.\n'''

# tweets.most_popular
tweet_d = {
  'Secretary Hillary Clinton':
    [('Secretary Hillary Clinton', '"Folks marched &amp; protested for our right to vote. They endured beatings and jail time. They sacrificed their lives for this right." --@FLOTUS\n', 1477610322, 'TweetDeck', 545, 226),
     ('Secretary Hillary Clinton', '"We urge voters to dump Trump and choose the clearly qualified candidate in this race: Hillary Clinton" --@DenverPost https://t.co/x62lrGm1MB\n', 1476205194, 'TweetDeck', 7165, 2225)],
  'Governor Gary Johnson':
    [('Governor Gary Johnson', 'Join me in #Atlanta November 2. Details- https://t.co/PsOd3PZrOc #YouIn? #JohnsonWeld\n', 1478034098, 'Hootsuite', 108, 51)]
}
result = tweets.most_popular(tweet_d, 1476000000, 1479000000)
assert isinstance(result, list), \
    '''tweets.read_tweets should return a list, but returned {0}\n'''.format(type(result))
assert isinstance(result[0], str), \
    '''tweets.read_tweets should return a list of strings, but returned a list of {0}\n'''.format(type(result[0]))

# tweets.detect_author
tweet_d = {
  'Secretary Hillary Clinton':
    [('Secretary Hillary Clinton', '"Folks marched &amp; protested for our right to vote. They endured beatings and jail time. They sacrificed their lives for this right." --@FLOTUS\n', 1477610322, 'TweetDeck', 545, 226),
     ('Secretary Hillary Clinton', '"We urge voters to dump Trump and choose the clearly qualified candidate in this race: Hillary Clinton" --@DenverPost https://t.co/x62lrGm1MB\n', 1476205194, 'TweetDeck', 7165, 2225)],
  'Governor Gary Johnson':
    [('Governor Gary Johnson', 'Join me in #Atlanta November 2. Details- https://t.co/PsOd3PZrOc #YouIn? #JohnsonWeld\n', 1478034098, 'Hootsuite', 108, 51)]
}
result = tweets.detect_author(tweet_d, 'Join me! #YouIn?')
assert isinstance(result, str), \
    '''tweets.detect_author should return a str, but returned {0}\n'''.format(type(result))


our_print("""
Hooray! The type checker passed!
This does NOT necessarily mean that your functions are correct!

It does mean that the functions in tweets.py:
- are named correctly,
- take the correct number of arguments, and
- return the correct types.

Be sure to thoroughly test your functions yourself before submitting.""")

builtins.print = our_print
builtins.input = our_input