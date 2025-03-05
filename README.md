# MediMate

How to run project (initial run):

1. Create python virtual enviornment and install requirements.txt
2. Access vector_database_indexer.py file, follow commented instructions within this file to create vector database embeddings.
3. Access account/api.py file. Uncomment import, file_path (this will have to be changed) and function name. (when you first login on the frontend it will load the dataset patients into standard SQL database).
4. Creating new a doctors account credentials (from shell due exisiting password hashing bug when creating account within backend and there is no signup functionality): Shell commands.
    `python manage.py shell`
    `from account.models import User`
    `user = User.objects.create_user(name="Doctor", email="doc@test.doc", password="Test_Doc")`
5. run `python manage.py createsuperuser` in Medimate_backend directory to create superuser for Django backend
6. Open two terminals and Cd into Medimate_backend and Medimate_fronted directories, in backend directory run `python manage.py runserver` and in frontend run `npm run dev` (if this     fails try `npm i` first)
7. localhost:5173 for frontend application and localhost:8000/admin/ for backend server. You will need to create a superuser to access Django backend.
8. changes undertaken in steps 2. and 3. should be undone after an initial run of the application.  


Post initial run:
1. `python manage.py runserver` in MediMate_backend directory to start backend server
2. `npm run dev` in MediMate_frontend directory to start frontend server






