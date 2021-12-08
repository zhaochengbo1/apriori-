from numpy import *
import pandas as pd

##creat L1 set of candidates 
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))     

##find frequent set from the candidate set
def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:   
        for can in Ck:  
            if can.issubset(tid):  
            #Determines whether the candidates contain items for the dataset
                if not can in ssCnt:
                    ssCnt[can] = 1   
                else:
                    ssCnt[can] += 1  
    numItems = float(len(D))  
    retList = [] 
            #L1 initialize
    supportData = {}  
            #Record the support for each data in the candidate
    for key in ssCnt:
        support = ssCnt[key] / numItems  
        if support >= minSupport:
            retList.insert(0, key)  
            supportData[key] = support  
    return retList, supportData


def calSupport(D, Ck, min_support):
    dict_sup = {}
    for i in D:
        for j in Ck:
            if j.issubset(i):
                if not j in dict_sup:
                    dict_sup[j] = 1
                else:
                    dict_sup[j] += 1
    sumCount = float(len(D))
    supportData = {}
    relist = []
    for i in dict_sup:
        temp_sup = dict_sup[i] / sumCount
        if temp_sup >= min_support:
            relist.append(i)
            supportData[i] = temp_sup
    return relist, supportData


def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):  
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:  
                a  = Lk[i] | Lk[j] 
                a1 = list(a)
                b = []
                for q in range(len(a1)):
                    t = [a1[q]]
                    tt = frozenset(set(a1) - set(t))
                    b.append(tt)
                t = 0
                for w in b:
                    if w in Lk:
                        t += 1
                if t == len(b):
                    retList.append(b[0] | b[1])
    return retList


def apriori(dataSet, minSupport):
    C1 = createC1(dataSet)
    D = list(map(set, dataSet))  
    L1, supportData = calSupport(D, C1, minSupport)
    L = [L1]  
    k = 2
    while (len(L[k - 2]) > 0):  
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minSupport)  # scan DB to get Lk
        supportData.update(supK)  #add supk'(k-v) to supportData
        L.append(Lk)  # L'last item is null
        k += 1
    del L[-1]  # delete the last item
    return L, supportData 


#  Build all subsets of the collection
def getSubset(fromList, toList):
    for i in range(len(fromList)):
        t = [fromList[i]]
        tt = frozenset(set(fromList) - set(t))
        if not tt in toList:
            toList.append(tt)
            tt = list(tt)
            if len(tt) > 1:
                getSubset(tt, toList)


def calcConf(freqSet, H, supportData, ruleList, minConf):
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]  #Calculate the confidence level
        # Calculate lift level,lift = p(a & b) / p(a)*p(b)
        lift = supportData[freqSet] / (supportData[conseq] * supportData[freqSet - conseq])
 
        if conf >= minConf and lift > 1:
            print(freqSet - conseq, '-->', conseq, 'Support:', round(supportData[freqSet], 6), 'Confidence：', round(conf, 6),
                  'lift：', round(lift, 6))
            ruleList.append((freqSet - conseq, conseq, conf))



def gen_rule(L, supportData, minConf):
    bigRuleList = []
    for i in range(1, len(L)): 
        for freqSet in L[i]:  
            H1 = list(freqSet)
            all_subset = []
            getSubset(H1, all_subset)  
            calcConf(freqSet, all_subset, supportData, bigRuleList, minConf)
    return bigRuleList
 
if __name__ == '__main__':
    file_path=open("/home/zephyn/Groceries_dataset.csv") #use your file_path
    data=pd.read_csv(file_path)

    data=data.groupby(['Member_number','Date'])['itemDescription'].apply(lambda x: list(x))

    transactions = data.values.tolist()

    print('\nPrevious five lines contents：\n', transactions[0:5])
    print('\n\n------------------------------------------------------------------------------------')
    dataSet = transactions
    L, supportData = apriori(dataSet, minSupport = 0.003)
    rule = gen_rule(L, supportData, minConf = 0.05)

   

