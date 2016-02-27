import itertools
from collections import OrderedDict
items = []
literalList = []
import sys

def compareLists(itemsList,compareItemList):
    #check for the length of itemslist and compareItemList
    compareList = []
    for item in itemsList:
        if compareItemList(item):
            compareList.append(item)
    return len(compareList) == len(itemsList) 


def exists(itemsList,compareItemList):
    #check if contents in compareItemList is present in itemslist
    compareList = []
    for item in itemsList:
        if compareItemList(item):
            compareList.append(item)
    return  len(compareList)>0


#used to flatten a list
def flatten(listToBeFlattend):
    flattendList = []
    for items in listToBeFlattend:
        for item in items:
            flattendList.append(item)
    return flattendList


#find all the unique literals in CNFsentence

def getUniqueLiteralList(CNFsentence):
    return list(set([ abs(literal) for literal in flatten(CNFsentence) ]))



def getList(literalList):
    return lambda literal:literal in literalList

#check if the clause contains atleast one literal,so that the entire clause can be satisfied
def clause_satisfied(clause,literalList):
    return exists(clause, getList(literalList))



def getSatisfiedList(literalList):
    return lambda clause:clause_satisfied(clause, literalList)

#checks if every clause in the CNF sentence is satisfied by the contents in literal list,
#if yes returns true

def satisfied(CNFsentence,literalList):
    return compareLists(CNFsentence, getSatisfiedList(literalList))



#checks if there exists a clause in the sentence that is false 

def getUnsatisfiedList(literalList):
    return lambda clause:compareLists(clause, lambda literal:-literal in literalList)

def unsatisfiable(CNFsentence,literalList):
    return exists(CNFsentence, getUnsatisfiedList(literalList))




def literalSearch(CNFsentence, literals,literalList):
    if satisfied(CNFsentence,literalList): return literalList
    elif unsatisfiable(CNFsentence,literalList): return False
    else:
        literal, s = literals[0], literals[1:]
        flag1 = literalSearch(s, literalList+[literal])
        flag2 =  literalSearch(s, literalList+[-literal])
        return  flag1 or flag2 

def unassigned_literals(clause,literalList):
    #helper class for unitClauseSearch
    newList = []
    for item in clause:
        if item not in literalList and -item not in literalList:
            newList.append(item)
    return newList


def unitClauseSearch(CNFsentence,literalList):
    #used to remove unit clause in CNF sentence
    for clause in CNFsentence:
        unassigned = unassigned_literals(clause,literalList)
        if len(unassigned) == 1:
            return unassigned[0]
    return None


def pureLiteralSearch(CNFsentence):
    #searching pure literal in the CNF sentence
    literals = flatten(CNFsentence)
    for literal in literals:
        if -literal not in literals:
            newList = []
            for item in CNFsentence:
                if literal not in item:
                    newList.append(item) 
            return literal, newList
    return None, None

def remove(literals,item):
    #helper method to remove literals
    x = literals.index(item)
    literals.pop(x)
    return literals

def search(CNFsentence,literals,literalList):
    #DPLL implementation containing 
    #unit clause searching,pure literal search 
    
    if satisfied(CNFsentence,literalList): return True
    elif unsatisfiable(CNFsentence,literalList): return False
    else:
        literal = unitClauseSearch(CNFsentence,literalList)
        if literal:
            items.append(literal)
            return search(CNFsentence, remove(literals,abs(literal)), literalList+[literal])
        literal, g = pureLiteralSearch(CNFsentence)
        if literal:
            items.append(literal)
            return search(g, remove(literals,abs(literal)), literalList+[literal])
        literal, s = literals[0], literals[1:]
        return search(CNFsentence, s, literalList+[literal]) or search(CNFsentence, s, literalList+[-literal])



def dpllAlgorithmImplemention(CNFsentence):
    #perform the dpll algorithm implementation
    return search(CNFsentence, getUniqueLiteralList(CNFsentence), [])




def nonNotCasesInDisjuncts(prop, ans):
    #if nots are not found in the disjuncts,they are simply appended to the sentence
    for i in range(1, len(prop)):
        temp = prop[i]
        ans = ans + flattenDisjuncts(temp) 
    
    return ans

def notAndNonNotCaseInDisjuncts(prop, ans, op):
    #if an operator not is found,then - is appended
    if op == "not":
        ans = ["-" + flattenCNF(prop[1])]
    else:
        ans = nonNotCasesInDisjuncts(prop, ans)
    return ans

def flattenDisjuncts(prop) :
    
    #takes a nested list with ORS and makes a list of all the literals and its negetions of the ORS
    
    ans= []
    if isinstance(prop, str) :
        ans = [prop]
    else :  
        op = prop[0]
        ans = notAndNonNotCaseInDisjuncts(prop, ans, op)
    return ans





def flattenOrAndNots(prop):
    #used to flatten ORs and  NOTs in the sentence
    
    if (prop[0] == "or"):
        answer = [flattenDisjuncts(prop)]
    elif (prop[0] == "not"):
        answer = [["-" + (prop[1])]]
    return answer


def flattenAnd(prop, answer):
    
    #Used to flatten Ands, if AND encloses ORs and NOT,
    #corresponding flattening takes place.
    
    for i in range(1, len(prop)):
        temp = prop[i]
        op = temp[0]
        if op == "or":
            answer = answer + [flattenDisjuncts(temp)]
        elif op == "not":
            answer = answer + [["-" + flattenCNF(temp[1])]]
        else:
            answer = answer + [flattenDisjuncts(temp)]
    
    return answer

def flattenCNFList(prop, answer):
    
    #based on the sentence, the list is flatterned based on the 
    #list element being a string,or having ony ANDS or ORAndNots
    
    
    flag = "and" not in prop
    if (flag):
        answer = flattenOrAndNots(prop)
    else:
        if isinstance(prop, str): 
            answer = prop
        else:
            answer = flattenAnd(prop, answer)
    
    return answer

def flattenCNF(prop) :
          
    #   used to make a list of conjuncts which has nested list of ORS.
    
    answer=[]
    
    if isinstance(prop, str) :  
        answer = prop 
    else :
        answer = flattenCNFList(prop, answer)          
    return answer



"""-------------------start of main function------------------------------------------------"""

result = []
result2 = []
CNFsentence=open('CNF_satisfiability.txt','w')
lines = [line.strip() for line in open(sys.argv[2])]
sentenceLen=int(lines[0])
for i in range(1,sentenceLen+1):
    output = eval(lines[i])
    """append the changes biconditional list to the main proposition """
    if len(output) == 0:        
        s1="["+'"true"'+"]"
        CNFsentence.write(s1+"\n")
    elif (len(output) == 1 and isinstance(output[0], str)):   
        """if the list has only one literal, [A] then print [true,A=true] """
        result2.append('"true"')
        result2.append('"' + output[0]+ '=true"')
        s3 = ','.join(result2)
        CNFsentence.write("[%s]\n" % (s3))
    
    
    else:
        for item in output:
            if((isinstance(item, str)) and (item != "and") and (item != "or") and (item != "not")) :
                temp=item
                output.remove(item)
                output.append(temp)
        prop4 = flattenCNF(output)
        if isinstance(prop4, str) :
            prop5 = list(prop4)
            prop6 = []
            for i in range(0,len(prop5)):
                subli = []
                subli.append(prop5[i])
                prop6.append(subli)
        else :
            prop6 = prop4
        output = prop6
        merged = list(itertools.chain(*output))
        output2 =  list(OrderedDict.fromkeys(merged))
        output4 =  list(OrderedDict.fromkeys(output2))
        def literalASCIIEquivalent(literal):
            if literal.startswith('-'):
                num = ord(literal[1:]) - 64
                number = '-'+str(num)
            else :
                number = ord(literal) - 64
            return str(number)
    
        def convertToASCIIEquivalent(CNFsentence):
            literals = output4
            LiteralASCIIMapping = dict(zip(literals, [ literalASCIIEquivalent(literal) for literal in literals ]))
            def getASCIIFromLiteral(literal):
                assert literal != 0
                return LiteralASCIIMapping[literal]
            def getClause(clause):
                return "[" + ",".join([ getASCIIFromLiteral(literal) for literal in clause ]) + "]"
            return "[" +",".join([ getClause(clause) for clause in CNFsentence ])+ "]"
    
        literals = output4
        LiteralASCIIMapping = dict(zip(literals, [ literalASCIIEquivalent(literal) for literal in literals ]))
        output5 = []
        temp =  convertToASCIIEquivalent(output)
        output5 = eval(temp)
        status = dpllAlgorithmImplemention(output5)
        printList = []
        if status:
            printList.append('"true"');
            for alpha, num in LiteralASCIIMapping.items():
                if int(num) in items:
                    if(int(num)<0):
                        printList.append('"' + alpha[1:]+ '=false"')
                    
                    else :
                        printList.append('"' + alpha+ '=true"')
                else :
                    if(int(num)<0):
                        printList.append('"' + alpha[1:]+ '=false"')
                    else :
                        printList.append('"' + alpha+ '=false"')
        else:
            printList.append('"false"');
        s1 = ','.join(printList)
        CNFsentence.write("[%s]\n" % (s1))
CNFsentence.close();
    