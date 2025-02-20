# MediMate


Creating new doctor login credentials (from shell due exisiting password hashing bug in code):

python manage.py shell
from account.models import User
user = User.objects.create_user(name="Doctor", email="doc@test.doc", password="Test_Doc")


Backend Login Credentials

Username: Admin
Email: admin@admin.dev
Password: Dev


Username: Doctor
Email: doc@test.doc
Password: Test_Doc