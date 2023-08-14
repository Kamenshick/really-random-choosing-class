from flask import Flask,render_template, request, redirect, url_for, session
import os
import sqlite3
import requests
from random import randint
import json

class Database:
    def query(self,query):
        self.sqlite_connection = sqlite3.connect("database/students.db")
        self.cursor = self.sqlite_connection.cursor()
        try:
            self.cursor.execute(query)
            record = self.cursor.fetchall()
            self.sqlite_connection.commit()
            self.cursor.close()
            return record
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (self.sqlite_connection):
                self.sqlite_connection.close()
                print("Соединение с SQLite закрыто")

class Session:
    def get_session(self):
        return session.get('username')
    def set_session(self,user_name):
        session['username'] = user_name

def getClassName():
    className = request.form["class-name"]
    return str(className)

def getClassCount():
    classCount = request.form["class-count"]
    return int(classCount)

def getStudentName(number):
    studentName = request.form[f"i-{number}"]
    return str(studentName)

def checkNotNone(name):
    setName = set(name)
    return False if setName == {' '} or setName == set() else True

def getStudents(classCount):
    students = []
    for number in range(1, classCount + 1):
        name = getStudentName(number)
        if checkNotNone(name):
            students.append(name)
    return students

def getStudentsWithZero(classCount):
    students = []
    for number in range(0, classCount):
        name = getStudentName(number)
        if checkNotNone(name):
            students.append(name)
    return students

database = Database()

def createClassInDatabase(name):
    database.query("INSERT INTO class ('name') VALUES ('{}');".format(name))

def getClassId(name):
    classId = database.query("SELECT `id` FROM class WHERE name='{}';".format(name))
    classId = classId[0]
    return classId

def getClassNameToId(classId):
    className = database.query("SELECT `name` FROM class WHERE id='{}';".format(classId))
    className = className[0][0]
    return className

def createStudentInDatabase(classname,name):
    database.query("INSERT INTO students ('class','name') VALUES ('{}','{}');".format(classname,name))

def deleteStudentInDatabase(classId):
    database.query("DELETE FROM students WHERE class='{}';".format(classId))

def deleteClassInDatabase(classId):
    database.query("DELETE FROM class WHERE id='{}';".format(classId))

def addStudent(classStudents,classId):
    for name in classStudents:
        createStudentInDatabase(classId, name)

def createСlassroom():
    className = getClassName()
    classCount = getClassCount()
    classStudents = getStudents(classCount)

    createClassInDatabase(className)
    classId = getClassId(className)

    addStudent(classStudents,classId[0])

def getСlassroom():
    classes = database.query("SELECT `id`,`name` FROM class;")
    return classes

def getStudentsinDatabase(classroom):
    students = database.query("SELECT `name` FROM students WHERE class='{}';".format(classroom))
    return students

def checkLenClassrom(students):
    if len(students) > 0:
        return True
    return False

def createStringStudents(students):
    students = [name[0] for name in students]
    return '|'.join(students)

def createСlassroomList(modeСheckLen=0):
    classList = []
    classes = getСlassroom()

    for classroom in classes:
        students = getStudentsinDatabase(classroom[0])
        if checkLenClassrom(students) or modeСheckLen == 0:
            string_students = createStringStudents(students)
            classList.append([classroom[0],classroom[1], string_students])
    return classList

def countStudentsInClassroom():
    countStudents = request.form.get("choose-count")
    return countStudents

def getStudentChooseName(studentNumber):
    name = request.form.get(f"s-{studentNumber}")
    return name

def checkIsNotNone(name):
    if name is not None:
        return True
    return False

def getClassIdInForm():
    classId = request.form["class-id"]
    return int(classId)

def getStudentsNamesInForm(studentCount):
    students = []
    for studentNumber in range(studentCount):
        name = getStudentChooseName(studentNumber)
        if checkIsNotNone(name):
            students.append(name)
    return students

def mixingList(list_):
    lenList = len(list_) - 1
    for elem in enumerate(list_):
        index = randint(0,lenList)
        list_[elem[0]], list_[index] = list_[index],list_[elem[0]]
    return list_

def checkValidateNumber(number):
    if str(number).isdigit():
        if int(number) > 0:
            return True
    return False

def comparisonNumbers(countChoose,countStudents):
    if countStudents >= countChoose:
        return True
    return False

def getRealRandomNumber(countChoose,countStudents):
    url = 'https://api.random.org/json-rpc/1/invoke'
    data = {'jsonrpc': '4.0', 'method': 'generateIntegers',
            'params': {'apiKey': '550655ac-fe35-4016-8da2-1dae61812dc9', 'n': countChoose, 'min': 0, 'max': countStudents-1,
                       'replacement': 'false', 'base': 10}, 'id': 24565}
    params = json.dumps(data)
    response = requests.post(url, params)
    return (response.json())

def getSubsequenceRandom(countChoose,countStudents):
    subsequenceRandom = getRealRandomNumber(countChoose,countStudents)
    subsequenceRandom = subsequenceRandom["result"]["random"]["data"]
    return subsequenceRandom

def getApiAnswer(countChoose,countStudents):
    apiAnswer = set(getSubsequenceRandom(countChoose, countStudents))
    while len(apiAnswer) < countChoose:
        apiAnswer = set(getSubsequenceRandom(countChoose, countStudents))
    return apiAnswer

def chooseStudents(students,countChoose,countStudents):
    chooseStudents = []
    apiAnswer = getApiAnswer(countChoose,countStudents)
    for indexApi in apiAnswer:
        chooseStudents.append(students[indexApi])
    return chooseStudents


def changeListStudents(countStudents):
    students = getStudentsNamesInForm(countStudents)
    students = mixingList(students)
    return students

def findClassroomList(allClassroomList,classId):
    for classroom in allClassroomList:
        if classroom[0] == classId:
            return classroom

def checkNoneList(StudentList):
    if StudentList == []:
        return False
    return True

#def comparisonСlassroomList(classStudent,FormStudents):
#    lenOriginal = len(classStudent) - 1
#    for element in enumerate(FormStudents):
  #      print(lenOriginal)
    #    if lenOriginal >= element[0]:
        #   print(element[1])
            #print(classStudent[0])
            #print(FormStudents)
    #    else:
    #        pass
     #   print(element)

app = Flask(__name__)

app.secret_key = os.getenv("SECRET", "randomstring123")

@app.route('/', methods=['GET', 'POST'])
def index():
    state = [""]
    classList = createСlassroomList(1)
    if request.method == "POST":
        countChoose = countStudentsInClassroom()
        countStudents = getClassCount()
        students = changeListStudents(countStudents)
        countStudents = len(students)

        state = ["Введите валидное число"]
        if checkValidateNumber(countChoose):
            countChoose = int(countChoose)
            state = ["Введёное число больше количества студентов"]
            if comparisonNumbers(countChoose,countStudents):
                state = chooseStudents(students,countChoose,countStudents)

    return render_template("index.html",classList=classList,state=state)

@app.route('/create', methods=['GET', 'POST'])
def create():
    state = [""]
    if request.method == "POST":
        try:
            createСlassroom()
        except: state = ["Ошибка"]
        else: state = ["Вы создали класс"]
    return render_template("create-class.html",state=state)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    state = [""]
    classList = createСlassroomList()
    if request.method == "POST":
        try:
            classCount = getClassCount()
            FormStudents = getStudentsWithZero(classCount)
            classId = getClassIdInForm()
            deleteStudentInDatabase(classId)
            if checkNoneList(FormStudents):
                addStudent(FormStudents, classId)
                print('yes')
            else:
                print('+')
                deleteClassInDatabase(classId)
        except:
            state = ["Ошибка"]
        else:
           state = ["Вы изменили класс"]
    return render_template("edit-class.html",classList=classList,state=state)



if __name__ == '__main__':
    app.run(debug=True)
