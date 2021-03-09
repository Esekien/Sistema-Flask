from appchiapa import app
from appchiapa import mail


if __name__ == "__main__":
    app.run(debug=True)
    mail.init_app(app)