QR Code Generator Setup
Step 1: Open your terminal on your visual studio code by pressing Ctrl+C

Step 1: active the virtual environment i.e a packages provider used to store all the packages for your application setup process (qrenv/Scripts/activate  for powershell and qrenv\Scripts\activate)


Step 2: install the requirements package i.e all the packages and framework dependencies
(pip install -r requirements.txt)

Step 3: makemigrations and migrate i.e to add your default database (sqlclient)
python manage.py makemigrations and python manage.py migrate

Step 4: run the development server( a server to show what you have been designing)
python manage.py runserver

Step 5: copy the ip address generated and paste in on the web browser

Step 6: to break the server press and hold ctrl + c in your terminal

