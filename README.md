Secure Chat App with E2EE
Secure Chat is a real-time messaging application with end-to-end encryption.
Messages are encrypted using AES and exchanged securely with RSA public-key cryptography, ensuring only the sender and receiver can read them.

Technologies used:
Python & Flask
Flask-SocketIO for real-time communication
JavaScript & Web Crypto API for encryption
HTML & CSS for frontend

How to run:
Clone the repository.
Create a virtual environment and install dependencies:
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
Run the app:
python app.py


Open two browser tabs to test real-time chat.
