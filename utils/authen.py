import sqlite3
import hashlib
import bridge
from os import path, remove
from pymongo import MongoClient


#address = "gilvirgill.com"

checkerList = [" ","'"]

def authenticate(checkBoxList, requestForm, userNames, passWords ):

    for i in checkerList:
        if( requestForm['username'].find(i) != -1 ):
            return "Username Cannot Contain Any Whitespace"
        if( requestForm['password'].find(i) != -1 ):
            return "Password Cannot Contain Any Whitespace"
        
    if( requestForm['username'] in userNames ):
        index = userNames.index(requestForm['username'])
        if passWords[index] == hashWord( requestForm['password'] ):
            return True
        else:
            return "Password Does Not Match"
    else:
        return "Username Not Found"

def register( checkBoxList, requestForm, userNames, passWords ):
    '''
    for i in checkerList:
        if( str(requestForm['username']).find(i) != -1 ):
            return "Username Cannot Contain Any Whitespace"
        if( str(requestForm['password']).find(i) != -1 ):
            return "Password Cannot Contain Any Whitespace"
    '''
    
    if( requestForm['username'] in userNames ):
        return "Username Already Taken"
    elif requestForm['password2'] != requestForm['password1']:
        return "Passwords Do Not Match"
    else:
        #userNames.append( requestForm['user'] )
        #passWords.append( hashWord(requestForm['password']) )
        return addToDB( requestForm['firstName'], requestForm['lastName'], requestForm['username'], hashWord(requestForm['password1']), requestForm['email'], requestForm['age'], requestForm['location'], requestForm['status'], checkBoxList)

def hashWord( strIn ):
    return hashlib.sha256(strIn).hexdigest()
    
def dbHandler( ):
    client = MongoClient('127.0.0.1')
    db = client.dataBase
    cursor = db.Account.find()
    firstName = []
    lastName = []
    userNames = []
    passWords = []
    email = []
    age = []
    location = []
    status = []
    interests = []
    for document in cursor:
        userNames.append( document['username'] );
        passWords.append( document['password'] );
        firstName.append( document['firstName'] );
        lastName.append( document['lastName'] );
        email.append( document['email'] );
        age.append( document['age'] );
        location.append( document['location'] );
        status.append( document['status'] );
        interests.append( document['interests'] ); 
    return { 'firstName': firstName, 'lastName': lastName, 'usernames' : userNames, 'passwords' : passWords, 'email': email, 'age': age, 'location': location, 'status': status, 'interests': interests}

def addToDB( firstName, lastName, userName, passWord,email, age, location, status, interests ):
    return bridge.createUser( {'firstName': firstName, 'lastName': lastName, 'username': userName, 'password' : passWord, 'email': email, 'age': age, 'location': location, 'status': status, 'interests': interests} )

