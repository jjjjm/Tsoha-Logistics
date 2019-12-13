# Installation
## Local
To run the program locally, you need an postgresql database named ``recipes_local``, and user account ``localconn`` with password ``localhost`` that has full access rights to the databse. Then start the python virtual environment and load the dependencies from ``requirement.txt`` file. After that run ``run.py`` file with your python interpeter. The program should start work now.
## Heroku
To run the program in heroku, you need to activate your postgresql database in heroku remote and then push project the program to that remote. The program should run automagically after that.

**NOTE:** If the Users table is empty, the program will populate it with one account that has admin status. name: **admin** password: **password1**