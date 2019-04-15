import pyrebase
config = {
    "apiKey": "AIzaSyBW8sALdhQZBdx1imWvqtK1NLDizNtpwB0",
    "authDomain": "clubevents-6d507.firebaseapp.com",
    "databaseURL": "https://clubevents-6d507.firebaseio.com",
    "projectId": "clubevents-6d507",
    "storageBucket": "clubevents-6d507.appspot.com",
    "messagingSenderId": "328916169448"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

def signIn(email, password):
    user = auth.sign_in_with_email_and_password(email, password)
    data = {
    "name": "Mortimer 'Morty' Smith"
    }
    db = firebase.database()

    # Pass the user's idToken to the push method
    db.child("users").push(data, user['idToken'])
    print(user)

signIn("izat.khamiyev@nu.edu.kz", "123456i")
