
import sys
from itertools import chain, combinations
from collections import defaultdict


def Generator(file_path):
    file_iter = open(file_path, 'rU')
    for trID in file_iter:
        trID = trID.strip().rstrip('\t')  # Remove disturbing tab
        tr = frozenset(trID.split('\t'))
        yield tr


def MinSupportCheck(itemSet, trList, minSupport, FreqSet):

        SurvivedSet = set()
        temp = defaultdict(int) #As we use FreqSet out of function, we need same temporary data

        for item in itemSet:
                for transaction in trList:
                        if item.issubset(transaction):
                                FreqSet[item] += 1
                                temp[item] += 1

        for item, cnt in temp.items(): #Use temp instead of FreqSet
                support = float(cnt)/len(trList)

                if support >= minSupport:
                        SurvivedSet.add(item) #Add item whose support over minSupport

        return SurvivedSet


def ClassifyInput(data):
    trList = list()
    itemSet = set()
    for tr in data:
        transaction = frozenset(tr)
        trList.append(transaction)

        # Make non-overlapping set
        for item in transaction:
            itemSet.add(frozenset([item]))   #characteristics of 'add' function
    return itemSet, trList


def ProcessApriori(data_iter, minSupport):

    # Extract non-overlapping 1-itemset(itemSet) and transaction list(trList)
    itemSet, trList = ClassifyInput(data_iter)

    # Make default dictionary to count the frequency of each transaction
    FreqSet = defaultdict(int)

    # To store whole L set
    wholeSet = dict()

    # Find frequent 1-itemsets
    Freq_One = MinSupportCheck(itemSet,trList,minSupport,FreqSet)

    # Set Freq_One as L1
    LSet_K = Freq_One

    # Starting with L2 and so on until there is no element in L(k-1) set
    K = 2
    while(LSet_K != set([])):
        # record L(k-1) in whole set with index
        wholeSet[K-1] = LSet_K

        #Generate Candidate Set by using union function
        CandSet_K = set([i.union(j) for i in LSet_K for j in LSet_K if len(i.union(j)) == K])

        #Filter Candidate Set which has lower support than minSupport
        LSet_K = MinSupportCheck(CandSet_K, trList, minSupport, FreqSet)

        K += 1

    #local function that makes subset of given set
    def makeSubset(Set):
        return chain(*[combinations(Set, i + 1) for i, a in enumerate(Set)])

    RuleResult = []
    for key, SurvSet in wholeSet.items()[1:]: #Total set of survived transactions index: number of element
        for item in SurvSet:

            #Gernerate subsets
            Subsets = map(frozenset, [x for x in makeSubset(item)])

            for element in Subsets: #pick arbitrary element from Subsets

                left = item.difference(element) #complementary set of element with respect to subset
                if len(left) > 0:

                    #Calculate rule support
                    ruleSupport = float(FreqSet[item])/len(trList)

                    #Calculate rule confidence
                    itemSupport = float(FreqSet[item])/len(trList)
                    elementSupport = float(FreqSet[element])/len(trList)
                    ruleConfidence = itemSupport/elementSupport

                    #As there is restriction about the minimum confidence we don't check that
                    #Save as list according in accordance with output requirement
                    RuleResult.append(((tuple(element), tuple(left)), ruleSupport, ruleConfidence))

    return RuleResult


def WriteFile(Asso_rules, f):

    #Pick each row by the value of rule confidence (Descending)
    for rule, support, confidence in sorted(Asso_rules, key=lambda (rule, support, confidence): confidence, reverse=True):
        base_item, asso_item = rule

        #As the data format is 'set' in python, we should extract the value only
        base_item = [int(list(base_item)[i]) for i in xrange(len(list(base_item)))]
        asso_item = [int(list(asso_item)[i]) for i in xrange(len(list(asso_item)))]
        base_item_str = str(base_item[0])
        asso_item_str = str(asso_item[0])

        #To meet the output file format, unlist the item set and make as string instance

        for i in xrange(len(base_item)-1):
            base_item_str += ','
            base_item_str += str(base_item[i+1])

        for j in xrange(len(asso_item)-1):
            asso_item_str += ','
            asso_item_str += str(asso_item[j+1])

        #Change support and confidence unit to percent and round to two decimal point
        data= "{%s}\t{%s}\t%.2f\t%.2f\n" % (base_item_str, asso_item_str, support*100, confidence*100)
        f.write(data)
           
    return f



if __name__ == "__main__":
    
    arg_minSupport = float(sys.argv[1])
    input_name = sys.argv[2]
    output_name = sys.argv[3]

    Data = Generator(input_name)
    minSupport = arg_minSupport * 0.01


    Asso_rules = ProcessApriori(Data, minSupport)

    #Make output.txt file
    out_file = open(output_name, 'w')

    #Write obtained association rules into the output file
    Result = WriteFile(Asso_rules, out_file)
    out_file.close() #Close file



