# fastapi_development

Python API Development - Comprehensive Course for Beginners 

https://youtu.be/0sOvCWFmrtA

https://youtube.com/playlist?list=PL8VzFQ8k4U1IiGUWdBI7s9Y7dm-4tgCXJ

https://github.com/Sanjeev-Thiyagarajan/fastapi-course

Course from Sanjeev Thiyagarajan

```
uvicorn app.main:app --reload
```

FastAPI First Steps https://fastapi.tiangolo.com/tutorial/first-steps/

PostgreSQL https://wiki.postgresql.org/wiki/Apt

SQLAlchemy https://www.sqlalchemy.org 
https://fastapi.tiangolo.com/tutorial/sql-databases/#install-sqlalchemy

Automatic interactive project documentation: 

http://127.0.0.1:8000/docs

http://127.0.0.1:8000/redoc

[HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

[HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

Password hashing

pip install passlib[bcrypt]

https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/?h=hashing#password-hashing

When using bcrypt with passlib in some versions, an error may occur, which does not seem to affect the operation of the application:
`AttributeError: module 'bcrypt' has no attribute '__about__'`

OAuth2 with Password (and hashing), Bearer with JWT tokens
https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#install-python-jose

Setup environment: [Postman](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=27764), [Thunder Client](https://blog.openreplay.com/use-thunder-client-and-vscode-as-an-alternative-to-postman)

###Path variable on Ubuntu

```
echo $PATH
```

Create a new environment variable on Ubuntu:

1. Open the terminal.
2. Type the following command to open your .bashrc file in a text editor:
```
nano ~/.bashrc
```
3. Add the following line at the end of the file:
```
export My_DB_URL="localhost:5432"
```
4. Save the file and exit the editor.
5. Apply the changes with the following command:
```
source ~/.bashrc
```
6. You can verify that it's set by typing:
```
echo $My_DB_URL
```
This should output localhost:5432.

Env Variables https://www.youtube.com/watch?v=0sOvCWFmrtA&t=32033