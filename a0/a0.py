# coding: utf-8

"""
CS579: Assignment 0
Collecting a political social network

In this assignment, I've given you a list of Twitter accounts of 4
U.S. presedential candidates.

The goal is to use the Twitter API to construct a social network of these
accounts. We will then use the [networkx](http://networkx.github.io/) library
to plot these links, as well as print some statistics of the resulting graph.

1. Create an account on [twitter.com](http://twitter.com).
2. Generate authentication tokens by following the instructions [here](https://dev.twitter.com/docs/auth/tokens-devtwittercom).
3. Add your tokens to the key/token variables below. (API Key == Consumer Key)
4. Be sure you've installed the Python modules
[networkx](http://networkx.github.io/) and
[TwitterAPI](https://github.com/geduldig/TwitterAPI). Assuming you've already
installed [pip](http://pip.readthedocs.org/en/latest/installing.html), you can
do this with `pip install networkx TwitterAPI`.

OK, now you're ready to start collecting some data!

I've provided a partial implementation below. Your job is to complete the
code where indicated.  You need to modify the 10 methods indicated by
#TODO.

Your output should match the sample provided in Log.txt.
"""

# Imports you'll need.
from collections import Counter
from TwitterAPI import TwitterAPI
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
import itertools




consumer_key = 'XOpcDRPwTAnpVBOZtsHZrlgxF'
consumer_secret = 'rXITfXsDxlQlTpWcETnUT09zcwVQhquQ1BBy3wQ2aevBhf6DTD'
access_token = '1389546229-2ZPMSkYlxLue2sWPtX2km4izxJSRKfWRtnoHibo'
access_token_secret = 'XNUr0jl1eNuHfGvfX96tjdrddrgwHr9AvBp8lKUDrANXR'


# This method is done for you.
def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)


def read_screen_names(filename):
    """
    Read a text file containing Twitter screen_names, one per line.

    Params:
        filename....Name of the file to read.
    Returns:
        A list of strings, one per screen_name, in the order they are listed
        in the file.

    Here's a doctest to confirm your implementation is correct.
    >>> read_screen_names('candidates.txt')
    ['DrJillStein', 'GovGaryJohnson', 'HillaryClinton', 'realDonaldTrump']
    """
    ###TODO
    pass

    content = []
    with open(filename) as file:
        content = file.readlines()

    file.close()

    # To remove extra spaces from beginning and ending
    result = [name.strip() for name in content]

    return result


# I've provided the method below to handle Twitter's rate limiting.
# You should call this method whenever you need to access the Twitter API.
def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request; e.g., "friends/ids"
      params ..... A parameter dict for the request, e.g., to specify
                   parameters like screen_name or count.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print(request.status_code)
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)



def get_users(twitter, screen_names):
    """Retrieve the Twitter user objects for each screen_name.
    Params:
        twitter........The TwitterAPI object.
        screen_names...A list of strings, one per screen_name
    Returns:
        A list of dicts, one per user, containing all the user information
        (e.g., screen_name, id, location, etc)

    See the API documentation here: https://dev.twitter.com/rest/reference/get/users/lookup

    In this example, I test retrieving two users: twitterapi and twitter.

    >>> twitter = get_twitter()
    >>> users = get_users(twitter, ['twitterapi', 'twitter'])
    >>> [u['id'] for u in users]
    [6253282, 783214]
    """
    ###TODO
    pass

    names_string = str(screen_names).replace("'","").strip('[]')
    # print(names_string)

    # rsp_obj=twitter.request('users/lookup', {'screen_name' : names_string })
    rsp_obj = robust_request(twitter,'users/lookup',{'screen_name' : names_string })

    list_dict = []

    for user_json in rsp_obj:
        list_dict.append(user_json)

    return list_dict


def get_friends(twitter, screen_name):
    """ Return a list of Twitter IDs for users that this person follows, up to 5000.
    See https://dev.twitter.com/rest/reference/get/friends/ids

    Note, because of rate limits, it's best to test this method for one candidate before trying
    on all candidates.

    Args:
        twitter.......The TwitterAPI object
        screen_name... a string of a Twitter screen name
    Returns:
        A list of ints, one per friend ID, sorted in ascending order.

    Note: If a user follows more than 5000 accounts, we will limit ourselves to
    the first 5000 accounts returned.

    In this test case, I return the first 5 accounts that I follow.
    >>> twitter = get_twitter()
    >>> get_friends(twitter, 'aronwc')[:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO
    pass

    ID = []

    # response = twitter.request('friends/ids', {'screen_name' : screen_name})
    response = robust_request(twitter,'friends/ids',{'screen_name' : screen_name})

    for item in response.get_iterator():
        ID.append(item)

    return sorted(ID)

def add_all_friends(twitter, users):
    """ Get the list of accounts each user follows.
    I.e., call the get_friends method for all 4 candidates.

    Store the result in each user's dict using a new key called 'friends'.

    Args:
        twitter...The TwitterAPI object.
        users.....The list of user dicts.
    Returns:
        Nothing

    >>> twitter = get_twitter()
    >>> users = [{'screen_name': 'aronwc'}]
    >>> add_all_friends(twitter, users)
    >>> users[0]['friends'][:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO
    pass

    for user in users:
        name = user['screen_name']
        user['friends'] = get_friends(twitter,name)


def print_num_friends(users):
    """Print the number of friends per candidate, sorted by candidate name.
    See Log.txt for an example.
    Args:
        users....The list of user dicts.
    Returns:
        Nothing
    """
    ###TODO
    pass

    temp_tup_list = []
    for user in users:
        temp_tup_list.append((user['screen_name'],len(user['friends'])))

    # print("Friends per candidate:\n")
    temp_tup_list.sort(key=lambda tup: tup[0])
    for tup in temp_tup_list:
        print(str(tup[0]) + " " + str(tup[1]))



def count_friends(users):
    """ Count how often each friend is followed.
    Args:
        users: a list of user dicts
    Returns:
        a Counter object mapping each friend to the number of candidates who follow them.
        Counter documentation: https://docs.python.org/dev/library/collections.html#collections.Counter

    In this example, friend '2' is followed by three different users.
    >>> c = count_friends([{'friends': [1,2]}, {'friends': [2,3]}, {'friends': [2,3]}])
    >>> c.most_common()
    [(2, 3), (3, 2), (1, 1)]
    """
    ###TODO
    pass

    counts = Counter()
    for user in users:
        counts.update(user['friends'])

    return counts


def friend_overlap(users):
    """
    Compute the number of shared accounts followed by each pair of users.

    Args:
        users...The list of user dicts.

    Return: A list of tuples containing (user1, user2, N), where N is the
        number of accounts that both user1 and user2 follow.  This list should
        be sorted in descending order of N. Ties are broken first by user1's
        screen_name, then by user2's screen_name (sorted in ascending
        alphabetical order). See Python's builtin sorted method.

    In this example, users 'a' and 'c' follow the same 3 accounts:
    >>> friend_overlap([
    ...     {'screen_name': 'a', 'friends': ['1', '2', '3']},
    ...     {'screen_name': 'b', 'friends': ['2', '3', '4']},
    ...     {'screen_name': 'c', 'friends': ['1', '2', '3']},
    ...     ])
    [('a', 'c', 3), ('a', 'b', 2), ('b', 'c', 2)]
    """
    ###TODO
    pass
    screen_names = []
    for user in users:
        screen_names.append(user['screen_name'])

    name_combinations = list(itertools.combinations(screen_names,2))

    temp_tup_dict = {}
    for name_tup in name_combinations:
        for user in users:
            if name_tup[0] == user['screen_name'] or name_tup[1] == user['screen_name']:
                if name_tup not in temp_tup_dict:
                    temp_tup_dict[name_tup] = user['friends']
                else:
                    temp_tup_dict[name_tup] = set(user['friends']).intersection(temp_tup_dict[name_tup])


    result_overlap = []
    for name_tup in name_combinations:
        # temp_counter = Counter(temp_tup_dict[name_tup])
        # count_overlap = 0
        # for element in temp_counter:
        #     if temp_counter[element] > 1:
        #         count_overlap += 1

        result_overlap.append((name_tup[0],name_tup[1],len(temp_tup_dict[name_tup])))

    sorted_result = sorted(tuple(result_overlap), key=lambda t: (-t[2],t[0],t[1]))

    return sorted_result


def followed_by_hillary_and_donald(users, twitter):
    """
    Find and return the screen_name of the one Twitter user followed by both Hillary
    Clinton and Donald Trump. You will need to use the TwitterAPI to convert
    the Twitter ID to a screen_name. See:
    https://dev.twitter.com/rest/reference/get/users/lookup

    Params:
        users.....The list of user dicts
        twitter...The Twitter API object
    Returns:
        A string containing the single Twitter screen_name of the user
        that is followed by both Hillary Clinton and Donald Trump.
    """
    ###TODO
    pass

    # response = robust_request(twitter,"users/lookup",{"screen_name" : 'HillaryClinton, realDonaldTrump'})
    # for item in response.get_iterator():
    #     temp = item['id']
    #
    # print(response.text)

    followed_by_hillary = get_friends(twitter,'HillaryClinton')
    followed_by_trump = get_friends(twitter,'realDonaldTrump')

    followed_by_both = set(followed_by_hillary).intersection(followed_by_trump)

    result = 'No one followed by both Hillary and Donald'

    if len(followed_by_both) >= 1:
       temp = followed_by_both.pop()
       response = robust_request(twitter,"users/lookup",{'user_id': temp})
       for item in response.get_iterator():
           result = item['screen_name']

    return result


def create_graph(users, friend_counts):
    """ Create a networkx undirected Graph, adding each candidate and friend
        as a node.  Note: while all candidates should be added to the graph,
        only add friends to the graph if they are followed by more than one
        candidate. (This is to reduce clutter.)

        Each candidate in the Graph will be represented by their screen_name,
        while each friend will be represented by their user id.

    Args:
      users...........The list of user dicts.
      friend_counts...The Counter dict mapping each friend to the number of candidates that follow them.
    Returns:
      A networkx Graph
    """
    ###TODO
    pass
    g = nx.Graph()

    friend_added_graph = []

    for friend in friend_counts:
        if friend_counts[friend] >1:
            friend_added_graph.append(friend)

    for user in users:
        g.add_node(user['screen_name'])
        for f in friend_added_graph:
            g.add_node(f)
            if f in user['friends']:
                g.add_edge(f,user['screen_name'])

    return g




def draw_network(graph, users, filename):
    """
    Draw the network to a file. Only label the candidate nodes; the friend
    nodes should have no labels (to reduce clutter).

    Methods you'll need include networkx.draw_networkx, plt.figure, and plt.savefig.

    Your figure does not have to look exactly the same as mine, but try to
    make it look presentable.
    """
    ###TODO
    pass

    labels = {}
    for user in users:
        labels[user['screen_name']] = user['screen_name']

    pos = nx.spring_layout(graph,scale = 5)
    plt.axis("off")
    # nx.draw_networkx(graph,pos=spring_pos,with_labels= False,node_size = 35)
    # nx.draw_spectral(graph,with_labels= False,node_size = 35)
    # nx.draw_networkx_edges(graph, width=1, edge_color='blue')
    # nx.draw(graph,labels)

    nx.draw_networkx_nodes(graph, pos, alpha=0.5, node_size=22, node_color='red')
    nx.draw_networkx_edges(graph, pos, alpha=0.3, width=0.15)
    nx.draw_networkx_labels(graph, labels=labels, pos=pos,font_size=7)

    plt.savefig(filename,dpi=100)


def main():
    """ Main method. You should not modify this. """
    twitter = get_twitter()
    screen_names = read_screen_names('candidates.txt')
    print('Established Twitter connection.')
    print('Read screen names: %s' % screen_names)
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    print('found %d users with screen_names %s' %
          (len(users), str([u['screen_name'] for u in users])))
    add_all_friends(twitter, users)
    print('Friends per candidate:')
    print_num_friends(users)
    friend_counts = count_friends(users)
    print('Most common friends:\n%s' % str(friend_counts.most_common(5)))
    print('Friend Overlap:\n%s' % str(friend_overlap(users)))
    print('User followed by Hillary and Donald: %s' % followed_by_hillary_and_donald(users, twitter))

    graph = create_graph(users, friend_counts)
    print('graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    draw_network(graph, users, 'network.png')
    print('network drawn to network.png')


if __name__ == '__main__':
    main()

# That's it for now! This should give you an introduction to some of the data we'll study in this course.


