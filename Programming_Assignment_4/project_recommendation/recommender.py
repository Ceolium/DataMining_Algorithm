from math import sqrt
import sys



def Readtofavors(file_path):

    favors = {}
    for line in open(file_path):
        (user, movie, rating, ts) = line.split('\t')
        favors.setdefault(user, {})
        favors[user][movie] = float(rating)
    return favors


def FileReader(file_path):
    df = []
    for row in open(file_path):
        (user, movie, rating, ts) = row.split('\t')
        df.append((user, movie, rating, ts))
    return df


# Returns the Pearson correlation coefficient for a pair
def sim_pearson(favors, p1, p2):
    # Get the list of mutually rated items
    share = {}
    for item in favors[p1]:
        if item in favors[p2]: share[item] = 1

    # When there is no ratings in common
    if len(share) == 0: 
        return 0

    n = len(share)

    # Sums of all the preferences
    sum1 = sum([favors[p1][it] for it in share])
    sum2 = sum([favors[p2][it] for it in share])

    # Sums of the squares
    sum1Sq = sum([pow(favors[p1][it], 2) for it in share])
    sum2Sq = sum([pow(favors[p2][it], 2) for it in share])

    # Sum of the products
    pSum = sum([favors[p1][it] * favors[p2][it] for it in share])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0

    pr = num / den

    return pr


# Gets recommendations for a person by using a weighted average
# of every other user's ratings
def User_GetRec(favors, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for not_me in favors:
        # don't compare me to myself
        if not_me == person: continue
        sim = similarity(favors, person, not_me)

        # ignore scores of zero or lower
        if sim <= 0: continue
        for item in favors[not_me]:

            # only need to evaluate movies I haven't seen yet
            if item not in favors[person] or favors[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += favors[not_me][item] * sim
                
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # Make weighted average based on the correlation information
    SimSet = [(total / simSums[item], item) for item, total in totals.items()]

    # Return the sorted list
    SimSet.sort()
    SimSet.reverse()
    return SimSet


# Read each row in u#.test data and
# Make user-based recommendation to each user-item combination
def make_user_prediction(train, test):

    user_Total = []
    check = set()

    for (user, movie, rating, ts) in test:
        # The test file is sorted by user
        # Therefore we only have to make user_recommendation set
        # when each user appears for the first time
        if user not in check:
            Res = User_GetRec(train, user)

        # Make a check set to avoid repeated recommendation for same user
        check.add(user)

        # Compare the test movie in recommendation set
        get_rate = [rating for (rating, p_movie) in Res if p_movie == movie]
        if len(get_rate) == 0: get_rate = [5]
        row = [user, movie, get_rate[0]]
        user_Total.append(row)


    return user_Total




def write_file(res, f):
    # Loop through each element
    # and write a row in a given format
    attr_len = len(res)
    row_len = len(res[0])
    for i in xrange(attr_len):
        row = ""
        for j in xrange(row_len):
            row += "%s\t" % (res[i][j])
        row = row[:-1]
        row += "\n"

        f.write(row)

    return f


if __name__ == "__main__":

    input = sys.argv[1]
    compare = sys.argv[2]

    train = Readtofavors(input)
    test = FileReader(compare)



    # User-based approach
    u_Res = make_user_prediction(train, test)
    file_name = input + "_prediction.txt"
    out_file = open(file_name, 'w')
    Result = write_file(u_Res, out_file)
    out_file.close()

