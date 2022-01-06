from bs4 import BeautifulSoup
import requests
import json

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
URL = "https://result.smtech.in/"
exam = "https://result.smtech.in/ex21.php?eid=MAY/JUNE%202020%20SEMESTER%20EXAMINATIONS" #exam link

jsonFileName = "may_june_2020_exam"

def scrap():
    allSubLink = []  #all branch and subject link
    studentResult = {}  #store result
    session = requests.Session()
    examhtml = session.get(exam, headers=headers)
    soup = BeautifulSoup(examhtml.content, 'html.parser')

    subjectLink(allSubLink,soup) #scrap and add all subject link to allSubjectLink[]

    for link in allSubLink:
        subject = session.get(link, headers=headers)
        soup = BeautifulSoup(subject.content,'html.parser')
        createTextFile(soup) #create a text file

        createDict(studentResult) # create a dictionary that will be converted to json file
    

    toJSON(studentResult)  #convert dict studentResult to json



def subjectLink(allSubLink,soup):
    for div in soup.findAll('div',class_='card-body'):
        for p in div.select('p'):
            for a in p.select('a'):
                allSubLink.append(URL+a['href'])

def createTextFile(soup):
    textFile = open("result.txt", 'w')
    textFile.write(soup.find('pre').getText())
    textFile.close()

def createDict(studentResult):
    sub=""
    code=""
    count = 0

    text = open("result.txt","r")

    text = text.read().strip() #remove all extra space before and after every line
    lines = text.split("\n")   #create a list if all lines as element including empty lines "" 
    
    newline = []
  
    #print("****************************************************************",count)

    for i in range(len(newline)):   #iterate each line
        if "Subject Code" in newline[i]:
            code = newline[i][16:22]
        if "Subject Title" in newline[i]:
            sub = newline[i][16:]
            sub = sub.strip()

        if "20" in newline[i]: #if line has "20" [part of regno]
            res = newline[i].split()  # spilt line and make a list
            if ((len(res)==2 or len(res)==5)):  # line with result should be of 2 or 5 length
                if(len(res[0])==9):  # and first element i.e. regno should be of length 9 only then assign values
                    reg = res[0]
                    if len(res)==2:
                        internal = "Nil"
                        ext = "Nil"
                        total = "Nil"
                        point = "P"
                    else:
                        internal = res[1]
                        ext = res[2]
                        total = res[3]
                        point = res[4]

                    marks = {}

                    marks["sub"] = sub
                    marks["int"] = internal
                    marks["ext"] = ext
                    marks["total"] = total
                    marks["grade"] = point

                    #print(reg)

                    if reg in studentResult:
                        studentResult[reg].update({code:marks})
                    else:
                        studentResult[reg] = {code:marks}

    #print(sub,code)       

def toJSON(studentResult):
    json_obj = json.dumps(studentResult, indent = 4)
  
    with open("{}.json".format(jsonFileName), "w") as outfile:
        outfile.write(json_obj)

scrap()    




