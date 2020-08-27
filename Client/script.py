from subprocess import call

call("pip install virtualenv", shell=True)
call("virtualenv env", shell=True)
call("source env/bin/activate", shell=True)
call("pip install flask", shell=True)
call("pip install requests", shell=True)
call("python application.py", shell=True)
