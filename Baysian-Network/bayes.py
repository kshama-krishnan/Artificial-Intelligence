#Your code for bayes.py goes here
import json
import itertools
import copy
import sys
from glob import glob
def findSolution1(symptomTrueList):

    symCount=0; 
    probabilityList = []
    innerList = []
    numerator=1
    denominator=1
    patientDict = {}
    for i in symptomTrueList:
        probabilityList = diseaseList[count]
        
        if i == 'T':
        
            innerList = probabilityList[symCount]
    
            numerator = numerator * float(innerList[0])
            denominator = denominator * float(innerList[1])
           
            
        if i == 'F':
            
            innerList = probabilityList[symCount]
            numerator = numerator * float(innerList[2])
            denominator = denominator * float(innerList[3])
          
        symCount=symCount+1
        
    numerator = numerator * float(probabilityList["prob_of_disease"])
    denominator = denominator * (1 - float(probabilityList["prob_of_disease"]))
    
    result = numerator/(numerator+denominator)
    patientDict[probabilityList["diseaseName"]]=format(result, '.4f')

    return patientDict




def findSolution2(symptomTrueList):
    dictMaxMinMain = {}
    dictMaxMinForDiesease = {}
    dictMaxMin = {}
    minMaxList = []
    s2List = []
    s2List = copy.deepcopy(symptomTrueList)
    countVal = symptomTrueList.count('U')
    
    tupleList = []
    for i in itertools.product(['T','F'],repeat=countVal):
        tupleList.append(i)  
    
    
    tupleCount = 0
    listCount = 0
    
    
    while(listCount<len(tupleList)):
        for n,i in enumerate(s2List):
            if i == 'U':
                s2List[n] = tupleList[listCount][tupleCount]
                tupleCount = tupleCount+1       
        dictMaxMin = findSolution1(s2List) 
        minMaxList.append(dictMaxMin.values())
        
        s2List = copy.deepcopy(symptomTrueList)
        listCount=listCount+1       
        tupleCount = 0
    finalMinMaxList = []
    finalMinMaxList.append(min(minMaxList))
    finalMinMaxList.append(max(minMaxList))
    merged = list(itertools.chain(*finalMinMaxList))
    dictMaxMinForDiesease[str(dictMaxMin.keys()[0])]=merged
    

    return dictMaxMinForDiesease


def findSolution3(symptomTrueList, disease, symptoms):
   
    s2List = []
    baseValue = eval(findSolution1(symptomTrueList)[disease])
    d = {}
    for i in range(len(symptomTrueList)):
        s2List = copy.deepcopy(symptomTrueList)
        if s2List[i] == 'U':
            s2List[i] = 'T'
            d[str([symptoms[i], 'T'])] = eval(findSolution1(s2List)[disease])
            s2List[i] = 'F'
            d[str([symptoms[i], 'F'])] = eval(findSolution1(s2List)[disease])
            
    list1 = []
    if len(d)>0:
        minimum = min(d, key=d.get)
        val = d[minimum]
        for key in d:
          if d[key] == val and key < minimum:
            minimum = key
            
        maximum = max(d, key=d.get)
        val = d[maximum]
        for key in d:
          if d[key] == val and key < maximum:
            maximum = key
                
        if d[maximum] > baseValue:
            list1 = eval(maximum)
        else:
            list1 = ['none', 'N']
        if d[minimum] < baseValue:
            list1 += eval(minimum)
        else:
            list1 += ['none', 'N']    
    else:
        list1 = ['none', 'N','none', 'N']
    
    return { disease : list1}
    

   
text_file = open(sys.argv[2])
filename=sys.argv[2]
fileval=filename.rsplit('/',1)[1]
filesplit=fileval.split('.')
output_file=str(filesplit[0])+'_inference.txt'
handler=open(output_file,'w')
    
    
lines = text_file.read().split('\n')
k = lines[0].split(' ')
symptoms = eval(k[0])
patients = eval(k[1])
s=""
totalLines = int(symptoms)*4
linecount=1
diseaseList = []
mainList = []
while(linecount < totalLines):
    dict = {}
    l = lines[linecount].split(' ')
    m = eval(lines[linecount+1])
    n = eval(lines[linecount+2])
    o = eval(lines[linecount+3])
    diseaseName = l[0]
    no_of_symptoms = l[1]
    prob_of_disease = l[2]

    for index in range(int(no_of_symptoms)):
        dict[index] = [n[index],o[index],1-n[index],1-o[index]]
    dict["symptoms"] = m
    dict["prob_of_disease"]=prob_of_disease
    dict["diseaseName"]=diseaseName
    diseaseList.append(dict)
    linecount=linecount+4

patientDict1 = {}
patientDictMinMax = {}
patientDictMinMaxUnknown = {}
patient_starting_line = linecount
global count
patientCount = 0



while(patientCount < patients):
    count = 0
    symptomTrueList = []
    patientDictMinMaxList = []
    patientDictMinMaxUnknownList = []
    patientList = []
    mainDict = {} 
    mainDictMinMax = {}
    mainDictMinMaxUnknown = {}
    
    while (count<symptoms):
        symptomTrueList = eval(lines[patient_starting_line])
        patientDict1 = findSolution1(symptomTrueList)
        patientList.append(patientDict1)
        
        patientDictMinMax = findSolution2(symptomTrueList)
        patientDictMinMaxList.append(patientDictMinMax)
        
        
        patientDictMinMaxUnknown = findSolution3(symptomTrueList, diseaseList[count]['diseaseName'],diseaseList[count]['symptoms'])
        patientDictMinMaxUnknownList.append(patientDictMinMaxUnknown)
        
        
        
        patient_starting_line=patient_starting_line+1
        count = count+1
    
    
    patientresult = {}
    for d in patientList: patientresult.update(d)
    mainDict[patientCount+1]=patientList
    
    
    minMaxresult = {}
    for d in patientDictMinMaxList: minMaxresult.update(d)
    mainDictMinMax[patientCount+1]=patientDictMinMaxList
    
    minMaxUnknownresult = {}
    for d in patientDictMinMaxUnknownList: minMaxUnknownresult.update(d)
    mainDictMinMaxUnknown[patientCount+1]=patientDictMinMaxUnknownList
  
    
    
    
    
    handler.write("Patient-"+str(patientCount+1)+":\n")
    handler.write(str(patientresult) + "\n")
    handler.write(str(minMaxresult) + "\n")
    handler.write(str(minMaxUnknownresult) + "\n")
    
    patientCount=patientCount+1
    mainDict={}
    mainDictMinMax={}



    

handler.close();
text_file.close()
