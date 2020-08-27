from subprocess import call

call("pip install virtualenv", shell=True)
call("virtualenv env", shell=True)
call("source env/bin/activate", shell=True)
call("pip install flask", shell=True)
call("pip install flask-restful", shell=True)
call("python app.py", shell=True)
