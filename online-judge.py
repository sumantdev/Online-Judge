import os
import cgi, cgitb
import sys
import MySQLdb
import time
from threading import Thread
from webob import Request
#import webapp2
from webapp2 import RequestHandler
from pprint import pprint
from mod_python import util
import cookielib
import urllib2
from header import *

def index(user="",password="",submit="",password2="",login_user="",login_password="",login_submit="",login_value="",
	pid="",rid="",code_lang="",source_code="",submit_source_code="",ques_id="",code_submit="",submit_sol="",add_ques="",
	submit_ques="",ques_title="",ques_statement="",input_data="",output_data=""):
	out=""
	msg=""
	error=""
	er_msg=""
	
	# Open database connection
	db = MySQLdb.connect("localhost","root","sumant","online_judge" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	local_time=time.localtime()
	
	#Adding Questions
	if  login_value=="true" and add_ques=="true":
		out+=index2()
		out+="""<script type="text/javascript" src="lib/ckeditor/ckeditor.js"></script>
		<form name="add_questions" method="post" action="" style="margin:50 0 0 100;">
		Title: <input type="text" name="ques_title"> <br /><br />
		Statement: <br /><textarea rows="30" cols="70" name="ques_statement" class="ckeditor"></textarea><br /><br />
		<div style="width:900px; height:500px;">
		<div style="float:left;">Input: <br />
		<textarea rows="30" cols="30" class="ckeditor" name="input_data">
		</textarea>&nbsp;&nbsp;</div>
		<div style="float:left; ">Output: <br /> <textarea rows="30" cols="30" class="ckeditor" name="output_data"></textarea></div>
		</div><br />
		<input type="submit" value="Submit" name="submit_ques"></form></body></html>"""

	#Storing Question in database
	if login_value=="true" and not submit_ques=="":
		sql = """INSERT INTO questions(ques_id,statement,input,output,date_of_creation)
        		 VALUES ('%s','%s','%s','%s','%s')"""%(ques_title,ques_statement,input_data,output_data,time.strftime("%Y-%m-%d %H:%M:%S",local_time))
        		#cursor = db.cursor()
        	cursor.execute(sql)
		db.commit()
		out+= '''<html><meta HTTP-EQUIV="REFRESH" content="0; url=?login_value=true"></html>'''


	#Submission Page
	if login_value=="true" and code_submit=="" and add_ques=="":
			
		if not submit_sol=="":
			cursor.execute("SELECT ques_id from questions where pid='%s'"%pid)
			result=cursor.fetchone()
			ques_id=result[0]
			if not submit_source_code=="" and (code_lang=="" or source_code==""):
				er_msg="1"
			out+=index2()
			out+="""<form name="code_submission" method="post" action="" style="margin:50 0 0 100">
				<h3>Submit the source code.</h3>
				
				Question: %s <br /><br />
				Select the language:
				<select name="code_lang">
				<option value="c">C</option>
				<option value="cpp" selected>C++</option>
				<option value="java">Java</option>
				</select>
				<br /><br />
				<textarea rows="30" cols="70" name="source_code"></textarea><br />
				<input type="submit" name="submit_source_code" value="Submit"></form><br />""" %ques_id
			if er_msg=="1":
				out+="""<script>
				alert("Please select any language and provide source code!!");
				</script></body></html>""" 
			else:
				out+="""</body></html>"""

		#Home Page
		if submit_sol=="":
			if pid=="":
				out+=index2()
				out+="""<h3>Login Successful!!</h3>
			 	<div style="height:700; width:1080px; margin:0 0 0 50px; border:2px solid black;">
				<div style="float:left; border-right:2px solid black;padding-right:50px;height:700px; ">Problems: <br />
				<ol>
				<li><a href="?login_value=true&pid=1">Square</a></li>
				<li><a href="?login_value=true&pid=3">Pallindrome</a></li>
				</ol></div>
				<div style="margin:0 50 0 10; float:left; width:500px;border-right:2px solid black;padding-right:50px;height:700px;">
				
				<h2>Welcome to my Online Judge.</h2></div>
				<div style="float:left;">
				<div style="height:400px; text-align:center;">
				Recent Activity:<hr><br /></div>
				<div style="text-align:center;">Your Submissions<hr></div>
				Score: 
				</div></div>
				
				</body></html>"""

			#Question Statement Page
			if not pid=="":
				cursor.execute("SELECT ques_id from questions where pid='%s'"%pid)
				result=cursor.fetchone()
				ques_id=result[0]
				cursor.execute("SELECT statement from questions where pid='%s'"%pid)
				result2=cursor.fetchone()
				statement=result2[0]

				out+=index2()
				out+="""<h3>Login Successful!!</h3>
			 	<div style="height:700; width:1080px; margin:0 0 0 50px; border:2px solid black;">
				<div style="float:left;  border-right:2px solid black;padding-right:50px;height:700px; ">Problems: <br />
				<ol>
				<li><a href="?login_value=true&pid=1">Square</a></li>
				<li><a href="?login_value=true&pid=3">Pallindrome</a></li>
				</ol></div>
				<div style="margin:0 50 0 10; float:left; width:500px;border-right:2px solid black;padding-right:50px;height:700px;">%s<br /><hr>
				<a href="?login_value=true&pid=1&submit_sol=true">Submit</a><br />
				<p>%s</p></div>
				<div style="float:left;">
				<div style="height:400px; text-align:center;">
				AC Submissions:<hr><br /></div>
				<div style="text-align:center;">Your Submissions<hr></div>
				Score: 
				</div></div>
				
				</body></html>""" % (ques_id,statement)

		#Code getting stored in database
		if not submit_source_code=="" and not code_lang=="" and not source_code=="":
		
				local_time=time.localtime()
				
				sql = """INSERT INTO source_code(ques_id,pid,source,language,date_of_submission)
        		 VALUES ('%s','%s','%s','%s','%s')"""%(ques_id,pid,source_code,code_lang,time.strftime("%Y-%m-%d %H:%M:%S",local_time))
        		#cursor = db.cursor()
        			cursor.execute(sql)
				db.commit()
				cursor.execute("SELECT MAX(rid) from source_code")
				result=cursor.fetchone()
				rid=result[0]
			
				out+= '''<html><meta HTTP-EQUIV="REFRESH" content="0; url=?login_value=true&code_submit=true&pid=1&ques_id=square&rid=%s&code_lang=%s"></html>'''%(rid,code_lang)
	
	#Code Execution Block		
	elif login_value=="true" and code_submit=="true":
		out+="<html>Code successfully submitted<br />Please wait for the result...<br /><br />"
		cursor.execute("SELECT source from source_code where rid='%s'"%rid)
		result=cursor.fetchone()
		source=result[0]
		if code_lang=="c":
				fo=open("/var/www/code.c","wb+")
				open("/var/www/error.txt","w+")
				#os.system("chmod 777 /var/www/code.c")
				fo.write(source)
				fo.close()
				os.system("gcc /var/www/code.c -o /var/www/a.out 2> /var/www/error.txt")
				
		elif code_lang=="cpp": 
			fo=open("/var/www/code.cpp","w+")
			open("/var/www/error.txt","w+")
			fo.write(source)
			fo.close()
			os.system("g++ /var/www/code.cpp -o /var/www/a.out 2> /var/www/error.txt")
		elif code_lang=="java":
			fo=open("/var/www/code.java","w+")
			open("/var/www/error.txt","w+")
			os.system("chmod 777 error.txt")
			fo.write(source)
			fo.close()
			#os.system("chmod 777 error.txt")
			os.system("javac /var/www/code.java 2>/var/www/error.txt")
			#os.system("g++ /var/www/code.cpp")
		#os.system("chmod 777 /var/www/code.cpp")
		fo=open("/var/www/out.txt","w+")
		fi=open("/var/www/in.txt","r+")
		#os.system("/var/www/./a.out < /var/www/in.txt >/var/www/out.txt")
		ce=open("/var/www/error.txt","r")
		ce_read=ce.read()
		if ce_read:
  			out+="""<br />Compilation Error!! <a href="error.txt">Click to see error!!</a></html>"""
		else:
  			t0=time.time()
  			tle=0
			
			class Test(Thread):
				def __init__(self):
        				self.running = True
        				self.t1=time.time()
        				Thread.__init__(self)
        				self.flag=0


   		 		def run(self):
   		 				
        				os.system("/var/www/./a.out < /var/www/in.txt >/var/www/out.txt")  
        					#else: 
        					#	out+=1
        						#1#os.system("")      
        				self.flag =1
        				self.t1=time.time()-t0
        				exit()

  			class Sec(Thread):

    				def __init__(self):
        				Thread.__init__(self)
          
    				def run(self):
        				while 1: 
        					t1=time.time()
            				t2=t1-t0
            				if t2>1:
                				os.system("pkill a.out")
                				exit()
                  
  
 	 		def calling_thread(tm):
    	  			th1=Test()
      				th1.start()
      				th2=Sec()
    
   		   		time.sleep(1)
      
     	 			if th1.flag != 1:
        			#os.system("pkill a.out")
        				ap=open("/var/www/out.txt","r+")
        				ap.write("tle")
        				ap.close()
        				th2.start()
      				else:
        				tm=th1.t1
        				return tm
           
  			tm=0 
  			t1=calling_thread(tm)
  			ap=open("/var/www/out.txt","r+")
  			apr=ap.read()
  			#print apr
  			if apr=="tle":
    				out+="TLE</html>"
  			elif apr=="":
    				out+="RTE</html>"
  			else:
    				ac=open("/var/www/actual.txt","r+")
    				acr=ac.read()
    				if apr==acr:
	   					out+= '''AC Execution Time = %.3f seconds</html>'''%t1
    				else:
	   					out+= '''WA</html>'''
	   		os.system("rm /var/www/out.txt")
	   		os.system("rm /var/www/a.out")

	#Login and Registry Page
	elif add_ques=="" and login_value=="":

		if not submit=="" and (user=="" or password=="" or password2==""):
			out+="""<font color="red">Required value missing!!</font>"""
		elif not (password==password2):
			out+="""<font color="red">Passwords do not match!! Retry</font>"""

		elif (not submit=="" and not user=="" and not password=="" and not password2==""):
				cursor.execute("SELECT COUNT(user_name) from users where user_name='%s'"%user)
				result=cursor.fetchone()
				number_of_users=result[0]
				if not number_of_users==0:
					msg="User already exists!!"
				else:
					sql = """INSERT INTO users(user_name,password,date_of_creation)
        			VALUES ('%s','%s','%s')"""%(user,password,time.strftime("%Y-%m-%d %H:%M:%S",local_time))

					cursor.execute(sql)
					db.commit()
					msg="""Thank you :)"""
		if not login_submit=="" and (login_user=="" or login_password == ""):
			error="Please provide a value!!"
		elif not login_submit=="" and not login_user=="" and not login_password=="":
	 		sql = """SELECT password FROM users where user_name='%s'"""%login_user
	 		cursor.execute(sql)
	 		valid = cursor.fetchall()
	 		for row in valid:
	 			valid_password=row[0]
	 			break
	 		cursor.execute("SELECT COUNT(user_name) from users where user_name='%s'"%login_user)
			result=cursor.fetchone()
			number_of_users=result[0]
			#out+=str(number_of_rows)
			if number_of_users==0:
				error="User does not exists!!"
	 		elif not valid_password==login_password and not login_submit=="":
	 			error="Incorrect Password!!"
	 		elif valid_password==login_password and not login_submit=="":
	 			out+= '''<meta HTTP-EQUIV="REFRESH" content="0; url=?login_value=true">'''
	
		out+= """ <html><body>
	<form name="register" action="" method="post"> Register here:<br>
	User Name: <input type="text" name="user"><br>
	Password: <input type="password" name="password"><br>
	Retype Password: <input type="password" name="password2"><br>
	<input type="submit" value="Register" name="submit">
	</form><h2><font color="green">%s</font></h2>
	<form name="login" action="" method="post">Login Here: <br />
	User_Name:<input type="text" name="login_user"><br />
	Password:<input type="password" name="login_password"><br />
	<input type="submit" value="Login" name="login_submit"></form><h3><font color="red">%s</font></h3>
	</body></html>""" % (msg,error)
	return out

