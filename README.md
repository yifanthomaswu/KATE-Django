Deployed instance on Cloud VM
http://146.169.46.94:8888/

Jenkins on Cloud VM
http://146.169.46.94:8080/
User: admin
Password: kate

PostgreSQL on Cloud VM
IP: 146.169.46.229
Port: 5432
Initial Database: kate
User Name: kateapp
Password: KateApp

To login as student
Add entry in kateapp_people table, where login is your collage login and tutor_id is one of any other login in the table
Login on deployed instance with collage identity

To login as teacher
Add entry in kateapp_people table, where login is your collage login and tutor_id is Null
Login on deployed instance with collage identity
