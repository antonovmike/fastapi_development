# fastapi_development

Python API Development - Comprehensive Course for Beginners 

https://youtu.be/0sOvCWFmrtA

https://youtube.com/playlist?list=PL8VzFQ8k4U1IiGUWdBI7s9Y7dm-4tgCXJ

https://github.com/Sanjeev-Thiyagarajan/fastapi-course

Course from Sanjeev Thiyagarajan

```bash
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
```bash
pip install passlib[bcrypt]
```
https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/?h=hashing#password-hashing

When using bcrypt with passlib in some versions, an error may occur, which does not seem to affect the operation of the application:
`AttributeError: module 'bcrypt' has no attribute '__about__'`

OAuth2 with Password (and hashing), Bearer with JWT tokens
https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#install-python-jose

Setup environment: [Postman](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=27764), [Thunder Client](https://blog.openreplay.com/use-thunder-client-and-vscode-as-an-alternative-to-postman)

## Set Path variable on Ubuntu

```bash
echo $PATH
```

Create a new environment variable on Ubuntu:

1. Open the terminal.
2. Type the following command to open your .bashrc file in a text editor:
```bash
nano ~/.bashrc
```
3. Add the following line at the end of the file:
```bash
export My_DB_URL="localhost:5432"
```
4. Save the file and exit the editor.
5. Apply the changes with the following command:
```bash
source ~/.bashrc
```
6. You can verify that it's set by typing:
```bash
echo $My_DB_URL
```
This should output localhost:5432.

## Remove Path variable on Ubuntu

Repeat the steps 1-5. After this type
```bash
unset My_DB_URL
```
And step 6 to be sure path variable is removed

## [Votes Table](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=33996)

Create table "votes" where both columns are composite primary key:
```SQL
CREATE TABLE votes (
post_id INT NOT NULL,
user_id INT NOT NULL,
PRIMARY KEY (post_id, user_id)
);
```
Or add composite primary key to existing table:
```SQL
ALTER TABLE votes ADD PRIMARY KEY (post_id, user_id);
```
To add a foreign key to the post_id column in the votes table, referencing the id column in the public.posts table, use the following SQL query:
```SQL
ALTER TABLE votes
ADD CONSTRAINT votes_posts_fk
FOREIGN KEY (post_id) REFERENCES public.posts(id);
```
```SQL
ALTER TABLE votes
ADD CONSTRAINT votes_users_fk
FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;
```

[SQL Joins](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-joins/)
```SQL
SELECT posts.*, COUNT(votes.post_id) AS likes FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id;
```

[Alembic’s documentation](https://alembic.sqlalchemy.org/en/latest)  
Create folder for alembic. Let's name it "alembic":
```bash
pip install alembic
pip freeze > requirements.txt 
alembic init alembic
```
Alembic revision  
```bash
alembic revision -m "create posts table"
```
Auto create revision  
```bash
alembic revision --autogenerate -m "auto-vote"
```

[CORS](https://fastapi.tiangolo.com/tutorial/cors/)

### Section 13: Deployment Heroku 
[11:34:39](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=41679s) Heroku intro  
[11:35:40](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=41740s) Create Heroku App  
[11:40:21](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=42021s) Heroku procfile  
[11:44:59](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=42299s) Adding a Postgres database  
[11:48:42](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=42522s) Env Variables in Heroku  
[11:58:59](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=43139s) Alembic migrations on Heroku Postgres instance  
[12:02:52](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=43372s) Pushing changed to production  