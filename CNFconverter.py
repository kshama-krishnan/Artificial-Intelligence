from timeit import itertools

count = 0
ips = []
result =[]


def getInputFileHandle(fileName):
    """Get the input filename,open in readable format ,count the number of lines"""
    fileHandle = open(fileName, "r")
    global count
    count = int(fileHandle.readline())
    print "Input count: ", count
    return fileHandle

def getInput(fileName):
    """append each of the lines in the input file to a list called ips"""
    fileHandle = getInputFileHandle(fileName)
    for i in range(count):
        ips.append(eval(fileHandle.readline()))

    fileHandle.close()
    

def getPrintListString(output):
    """method to print a list"""
    output = str(output) + "\n"
    output = output.replace("'", "\"")
    return output


def getPrintString(output):
    """If a string is to be printed, then output the string
    Eg:- A is printed as "A" """
    output = '"' + output + '"\n'
    return output


def getPrintStr(output):
    """check if the output is instance of list or string, and print accordingly"""
    if isinstance(output, list):
        output = getPrintListString(output)
    else:
        output = getPrintString(output)
    return output

def putoutput(fileName):
    """open the output file in writable format and write the result to the file"""
    fileHandle = open(fileName, "w")
    
    for ind in range(count):
        fileHandle.write(getPrintStr(result[ind]))
        
    fileHandle.close()


def checkBiConditional(listElement, others):
    """if the list element is iff, then take the change the remaining list 
    Example:-[iff,A,B] is replaced by ["and",[implies,A,B],[implies,B,A]]
    
    """
    if listElement == "iff":
        listElement = "and"
        first = others[0]
        second = others[1]
        list1 = []
        list1.append("implies")
        list1.append(first)
        list1.append(second)
        others[0] = list1
        list2 = []
        list2.append("implies")
        list2.append(second)
        list2.append(first)
        others[1] = list2
    return listElement


def populateBiconditional(prop, listElement, others, ind, innerLen):
    """append the changes biconditional list to the main proposition """
    prop = []
    innerLen = len(others)
    prop.append(listElement)
    for ind in range(innerLen):
        prop.append(others[ind])
    
    return prop


def biConditionRecursion(len, others, ind, range):
    """used to perform biconditional recursion """
    innerLen = len(others)
    for ind in range(innerLen):
        other = others[ind]
        if isinstance(other, list):
            other = biConditional(other)
            others[ind] = other
    
    return ind, innerLen

def biConditional(propSentence):
    """used to remove biConditional elements in the propositional sentence
    consists of 3 steps 
    Firstly,the list is traversed by recursion,
    Secondly,the biconditional statements are being checked,
    Thirdly, the biconditional statements are being replaced."""

    length = len(propSentence)
    listElement = propSentence[0]
    others = []
    
    for ind in range(1,length):
        others.append(propSentence[ind])
    
    ind, innerLen = biConditionRecursion(len, others, ind, range)
            
    listElement = checkBiConditional(listElement, others)
    propSentence = populateBiconditional(propSentence, listElement, others, ind, innerLen)
    
    return propSentence


def checkImplictions(listElement, others):
    """if the list element is iff, then take the change the remaining list 
    Example:-[implies,A,B] is replaced by ["and",[not,A],[B]]
    
    """
    if listElement == "implies":
        listElement = "or"
        first = others[0]
        list1 = []
        list1.append("not")
        list1.append(first)
        others[0] = list1
    return listElement


def populateImplications(propSentence, len, listElement, remElements, ind, range, innerLen):
    """append the changes biconditional list to the main proposition """
    propSentence = []
    innerLen = len(remElements)
    propSentence.append(listElement)
    for ind in range(innerLen):
        propSentence.append(remElements[ind])
    
    return propSentence


def implicationRecursion(len, others, ind, range):
    """used to perform implication recursion """
    innerLen = len(others)
    for ind in range(innerLen):
        other = others[ind]
        if isinstance(other, list):
            other = implications(other)
            others[ind] = other
    
    return ind, innerLen

def implications(propSentence):
    """used to remove implication elements in the propositional sentence
    consists of 3 steps 
    Firstly,the list is traversed by recursion,
    Secondly,the implication statements are being checked,
    Thirdly, the implication statements are being replaced."""
    length = len(propSentence)
    listElement = propSentence[0]
    others = []
    
    for ind in range(1,length):
        others.append(propSentence[ind])
    
    ind, innerLen = implicationRecursion(len, others, ind, range)
            
    listElement = checkImplictions(listElement, others)
    propSentence = populateImplications(propSentence, len, listElement, others, ind, range, innerLen)
    
    return propSentence


def takeCareDeMorgan(others, innerListElement, negations):
    """use to perform deMorgan's law ["not",["and","A","B"]] is ["or",["not","A"],["not","B"]]"""
    if innerListElement == "and":
        innerListElement = "or"
    elif innerListElement == "or":
        innerListElement = "and"
    prop = [innerListElement]
    innerLen = len(others)
    for ind in range(1, innerLen):
        prop += [negations(["not", others[ind]])]
    
    return prop, ind


def checkDoubleNegations(others):
    """if there is a negation after a negation, then negations method is called again
    else deMorgan method is called.
    """ 
    innerListElement = others[0]
    if innerListElement == "not":
        prop = negations(others[1])
    else:
        prop, ind = takeCareDeMorgan(others, innerListElement, negations)
    return prop


def populateNegations(propSentence, listElement):
    """the modified list element is replaced in the prop sentence and returned."""
    prop = [listElement]
    propLen = len(propSentence)
    for ind in range(1, propLen):
        prop += [negations(propSentence[ind])]
    
    return prop

def negations(propSentence) : 
    """used to check negetions,if only a string A is found, then only the [not,A] is appended 
    else,we have to check for double negetions recursively,
    Finally we append the changed list elements in the end.  
    """ 
    if isinstance(propSentence, str) :
        prop = propSentence
    else :
        listElement = propSentence[0]
        if listElement == "not" :
            others = propSentence[1]
            if isinstance(others, str) :
                prop = []
                prop.append("not")
                prop.append(others) 
            else :
                prop = checkDoubleNegations(others)
        else :
            prop = populateNegations(propSentence, listElement)

    return prop
    


def distributionRecursion(others, length, len, ind, range):
    """used to perform distributive recursion"""
    length = len(others)
    for ind in range(length):
        others[ind] = distribution(others[ind])
    
    return length


def distribute(propSentence, listElement, others, length, ind, range):
    """ split the sentence for distribution"""
    propSentence = []
    propSentence.append(listElement)
    for ind in range(length):
        propSentence.append(distribution(others[ind]))
    
    return propSentence

def distribution(propSentence):
    """used to perform distributive law"""
    if isinstance(propSentence, list):
        listElement = propSentence[0]
        others = []
    
        length = len(propSentence)
        for ind in range(1,length):
            others.append(propSentence[ind])
            
        length = distributionRecursion(others, length, len, ind, range)
        
        if listElement == "and":
            propSentence = distribute(propSentence, listElement, others, length, ind, range)
        elif len(others) > 1:
            propSentence = checkOr( others )
            
    return propSentence


def populateCheckOrs(props, propSentence, length, len, ind, range):
    length = len(props)
    propSentence.append("or")
    for ind in range(length):
        propSentence.append(props[ind])


def checkOrList(props, propSentence, length, len, ind, range, prop):
    if prop[0] == "and":
        propSentence.append("and")
        innerLen = len(prop)
        for ind1 in range(1, innerLen):
            list1 = []
            if ind != 0:
                for ind2 in range(ind):
                    list1.append(props[ind2])
            
            list1.append(prop[ind1])
            for ind2 in range(ind + 1, length):
                list1.append(props[ind2])
            
            propSentence.append(checkOr(list1))

def checkOr( props):
    propSentence = []
    if isinstance(props, str):
        return props
    
    length = len(props)
    for ind in range(length):
        prop = props[ind]
        if isinstance(prop, list):
            checkOrList(props, propSentence, length, len, ind, range, prop)
            break;

    if len(propSentence) == 0:
        if isinstance(props, str):
            return props
        
        populateCheckOrs(props, propSentence, length, len, ind, range)
        
    return propSentence

def flattenCNF(propSentence):
    """used to flatten list of lists into one big list
    input is a nested list and the output is a list of conjuncts.
    Each list of conjunct contains list of disjuncts
    """
    def flattenDisjuncts(propSentence):
        
        def flattenDisJ(propSentence, length):
            prop = []
            for ind in range(1, length):
                prop += flattenDisjuncts(propSentence[ind])
            
            return prop

        length = len(propSentence)
        if isinstance(propSentence, list) and length > 2:
            prop = flattenDisJ(propSentence, length)
            return prop
        return [propSentence]
    
    length = len(propSentence)
    if isinstance(propSentence, list) and length > 2:
        listElement = propSentence[0]
        if listElement == "and":
            prop = []
            for ind in range(1,length):
                prop += flattenCNF(propSentence[ind])
            return prop
        if listElement == "or":
            prop = []
            for ind in range(1,length):
                prop += flattenDisjuncts(propSentence[ind])
            return [prop]
        
    return [propSentence]


def getPossibleDuplicates(prop):
    """used to get possible duplicates in the proposition"""
    duplicates = list(itertools.permutations(prop, len(prop)))
    duplicatesList = [list(elem) for elem in duplicates]
    return duplicatesList

def duplicates(propSentence):
    result = []
    for prop in propSentence :
        prop =  removeDup(prop)
        if prop not in result:
            dups = getPossibleDuplicates(prop)
            flag = True
            for dup in dups:
                if dup in result:
                    flag = False
                    break
            if flag:
                result += [prop]
    return result


def removeDupRecursion(propSentence, isinstance):
    """performs duplicate resursion"""
    first = propSentence[0]
    others = propSentence[1:]
    others = removeDup(others)
    if first in others:
        ans = others
    elif isinstance(others, list):
        ans = [first] + others
    else:
        ans = [first] + [others]
    return ans
    
def removeDup(propSentence) :
    """removes all duplicate strings from list  propSentence"""
    if isinstance(propSentence, str):
        return propSentence
    
    if len(propSentence) == 0 :
        ans = propSentence
    else :
        ans = removeDupRecursion(propSentence, isinstance)
    return ans


def performSubstitute(propSentence, length):
    for ind in range(length):
        prop = propSentence[ind]
        if isinstance(prop, list) and prop[0] != "not":
            prop.insert(0, "or")

def substituteOR(propSentence, flag):
    length = len(propSentence)
    
    performSubstitute(propSentence, length)
    if flag:        
        propSentence.insert(0, "and")
        return propSentence    
            
    return propSentence[0]


def singleLiterallistElementCase(prop):
    """used to remove all reduntant elements from the list 
    Eg:-[[and,A]] cannot be possible and hence has to be changed to [['A']]"""
    if isinstance(prop, list) and len(prop) == 2:
        listElement = prop[0]
        if listElement != "not":
            prop = prop[1]
    return prop


def singleLiteralCase(prop):
    """If ["A"] is given as input, then "A" is returned """
    if len(prop) == 1 and isinstance(prop[0], str):
        prop = prop[0]
    return prop

def edgeCases(prop):
    """used to handle edges cases of single literal and single literal list element cases"""
    prop = singleLiterallistElementCase(prop)
    prop = singleLiteralCase(prop)

    length = len(prop)
    if isinstance(prop, list):
        propSentence = []
        for ind in range(length):
            propSentence.append(edgeCases(prop[ind]))
        return propSentence
    return prop

def checkEmptyAndSingleLiteral(output, result):
    """if the output is null list or a string, then  output a null list """
    if len(output) == 0:
        result.append(output)
        return True
    if len(output) == 1 and isinstance(output[0], str):
        result.append(output)
        return True
    return False


def runAlgo(ind):
    """removes the biconditionals, implications,negetions and applies distributive law in an order"""
    result.append(biConditional(ips[ind]))
    result[ind] = implications(result[ind])
    result[ind] = negations(result[ind])
    result[ind] = distribution(result[ind])


def cleanup(ind, flag):
    """flattens CNF,"""
    listElement = result[ind][0]
    if listElement == "and":
        flag = True
    else:
        flag = False
    result[ind] = flattenCNF(result[ind])
    result[ind] = substituteOR(result[ind], flag)
    result[ind] = duplicates(result[ind])
    result[ind] = edgeCases(result[ind])

def main():
    """read each line from sentences.txt
    check if there is Empty or single Literal
    Else call runAlgo method and then do the cleanup"""
    getInput("sentences.txt")
    for ind in range(count):
        output = ips[ind]
        flag = checkEmptyAndSingleLiteral(output, result)
        if flag:
            continue
        runAlgo(ind)
        cleanup(ind, flag)
    
    putoutput("sentences_CNF.txt")

main()