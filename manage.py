from config import Configuration
from app import create_app

app = create_app(Configuration)

@app.route('/')
def index():
    sender = 'stevenrmonaghan@gmail.com'
    recipients = ['stevenrmonaghan@gmail.com']
    msg = Message()
    msg.subject = "Test Send"
    msg.recipients = recipients
    msg.sender = sender
    msg.body = 'testing'

    mail.send(msg)

if __name__ == '__main__':
    app.run()
