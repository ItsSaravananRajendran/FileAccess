import os
from flask import Flask, render_template, request

app = Flask(__name__)




@app.route('/')
def hello_world():
	return render_template('index.html')




@app.route('/upload', methods=['POST'])
def upload_file():
	perm = request.form['perm']
	fileList = request.files.getlist("image")
	directory = request.form['directory']
	alreadyPresent = ''
	status = "FILE UPLOAD IS SUCCESSFULL"
	if directory != "None":
		for file in fileList:
			if file.filename == '':
				return render_template('upload.html',status="PLEASE SELECT A FILE TO UPLOAD",directory=directory,perm=perm)
			if file.filename not in os.listdir(directory):
				f = os.path.join(directory+'/', file.filename)
				file.save(f)
			else:
				alreadyPresent += " " + file.filename
		return render_template("makeDir.html",directory=directory,items=createListToBeSent(directory),status="",perm=perm)
	else:
		return render_template('index.html',status="KINDLY LOGIN WITH YOUR CREDENTIALS")

	if alreadyPresent != '':
		status = "THESE FILE NAMES ARE ALREADY PRESENT IN THE FOLDER:" + alreadyPresent	
	return render_template('upload.html',status=status,directory=directory,perm=perm)


@app.route('/fileSelect',methods=['POST','GET'])
def fileSelect():
	perm = request.form['perm']
	directory = request.form['dir']
	submit= request.form['submit']
	if submit == "upload":
		return render_template('upload.html',status="",directory=directory,perm=perm)
	elif (submit!=None and len(submit.split('.')) == 1):
		directory = directory +"/"+submit
		return render_template("makeDir.html",directory=directory,items=createListToBeSent(directory),status="",perm=perm)
	elif (len(submit.split('.')) == 2):
		ext = submit.split('.')[-1]
		if ext.lower() in ["html","txt","py","css","cpp","c"]:
			with open(directory+"/"+submit,'r') as d:
				data = d.read()
				read = "false"
			return render_template("show.html",directory=directory,status="",file=submit,data=str(data),read=read,perm=perm)
		else :
			return render_template("makeDir.html",directory=directory,items=createListToBeSent(directory),status="Format not supported for editing")

@app.route('/retr',methods=['GET','POST'])
def retr():
	perm = request.form['perm']
	name = request.form['folderName']
	directory = request.form['dir']
	if name == "":
		return render_template('makeDir.html',directory=directory,items=createListToBeSent(directory),status="PLEASE ENTER A FOLDER NAME",perm=perm)	
	if directory == "None":
		return render_template('index.html',status="KINDLY LOGIN WITH YOUR CREDENTIALS")
	status = 'FOLDER  HAS BEEN CREATED'
	if name in os.listdir(directory):
		status = "FOLDER ALREADY EXISTS"
	else:
		os.mkdir(directory+'/'+name)

	return render_template('makeDir.html',directory=directory,items=createListToBeSent(directory),status=status,perm=perm)

@app.route('/login', methods=['GET', 'POST'])
def login():	
	user = request.form['username']
	password = request.form['password']
	dirList = os.listdir('login')
	details =  None
	for name in dirList:
		if name == user:
			with open('login/'+name,'r') as inputFile:
				details = inputFile.read().split(',')
				break
	if details != None :
		if details[1] == password:
			directory =  "uploads"
			perm = details[3]
			return render_template('makeDir.html',directory=directory,items=createListToBeSent(directory),status="",perm=perm)
		else:
			return render_template('index.html',status="PASSWORD IS WRONG")
	return render_template('index.html',status="NO USER FOUND, PLEASE SIGNUP")



@app.route('/save', methods=['GET', 'POST'])
def save():	
	directory = request.form['dir']
	file = request.form['file']
	data = request.form['data'].encode("UTF-8")

	with open(directory+"/"+file,"w") as out:
		out.write(data)
	return render_template('makeDir.html',directory=directory,items=createListToBeSent(directory),status="File has been saved")



@app.route('/signup', methods=['GET', 'POST'])
def signup():	
	user = request.form['username']
	password = request.form['password']
	dirList = os.listdir('login')
	status = ''
	if user.lower() in dirList:
		status = 'USER ALREADY EXISTS , TRY OTHER USER NAMES'
	else:
		os.mkdir('uploads/'+user.lower()) 
		string = user + ',' + password + ',uploads/' + user.lower() +","+"true" 
		with open('login/'+user,'w') as inputFile:
			inputFile.write(string)
		status = 'USER HAS BEEN CREATED'	
	return render_template('index.html',status=status)


def createListToBeSent(directory):
	dirList = os.listdir(directory)
	fileType = []
	for dirc in dirList:
		if len(dirc.split("."))==2:
			fileType.append("file")
		else:
			fileType.append("dir")
	return zip(fileType,dirList)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
