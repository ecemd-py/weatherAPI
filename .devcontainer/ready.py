import subprocess
import sys
import os

def system(cmd):
    """Run system command cmd."""
    process = subprocess.Popen(cmd)
    output, error = process.communicate()
    if error:
       print('Command\n  %s\nfailed.' % cmd)
       print(output)
       sys.exit(1)

system(["pip", "install", "flask"])
system(["pip", "install", "pyjwt"])
system(["pip", "install", "pyjwt[crypto]"])
system(["pip", "install", "pandas"])
system(["pip", "install", "sqlalchemy"])
system(["pip", "install", "psycopg2"])

os.chdir(os.path.abspath('weatherAPI/src'))

system(["flask", "run", "--host=127.0.0.1", "--port=8000"])
