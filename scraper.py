from bs4 import BeautifulSoup
import requests
import json

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
URL = "https://result.smtech.in/"
exam = "" #exam link

jsonFileName = ""

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
    count = 0

    text = open("result.txt","r")

    text = text.read().strip() #remove all extra space before and after every line
    lines = text.split("\n")   #create a list if all lines as element including empty lines "" 
    
    newline = []
    
    for line in lines:   #removing empty lines "" element
        if line!="":
            newline.append(line)

    if len(newline)>1:  #find number of student appeared (count)
        for i in range(6,len(newline)):
            if (newline[i].split()[0])[0:2]=="20":
                count = count+1

        code = newline[2][16:22]  
        sub = newline[3][16:]
        credit = newline[4][16:]
        
        for line in range(count):
            reg = newline[6+line].split()[0]
            if credit==" 0.0":   #if credit is zero
                internal = "Nil"
                ext = "Nil"
                tot = "Nil"
                point = newline[6+line].split()[1]
            else:
                internal = newline[6+line].split()[1]
                ext = newline[6+line].split()[2]
                tot = newline[6+line].split()[3]
                point = newline[6+line].split()[4]
                     
            marks = {}

            marks["sub"] = sub
            marks["int"] = internal
            marks["ext"] = ext
            marks["total"] = tot
            marks["grade"] = point
            marks["credit"] = credit

            if reg in studentResult:
                studentResult[reg].update({code:marks})
            else:
                studentResult[reg] = {code:marks}

def toJSON(studentResult):
    json_obj = json.dumps(studentResult, indent = 4)
  
    with open("{}.json".format(jsonFileName), "w") as outfile:
        outfile.write(json_obj)

        

    


# print(newline)

# marks = newline[6].split()
# print(marks)

# print(float(newline[6].split()[2]))  

# if len(newline)!=0:
#     info["code"] = newline[2][16:]
#     info["sub"] = newline[3][16:]
#     info["credit"] = float(newline[4][16:])
#     info["int"] = float(newline[6].split()[1])
#     info["ext"] = float(newline[6].split()[2])
#     info["tot"] = float(newline[6].split()[2])
#     info["cgpa"] = float(newline[6].split()[2])

scrap()    




