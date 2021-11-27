# 3STAT Algorithm - email.py
# Fall 2021 CS 463

from email_creds import password, login
import db as d
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailClient:
    """
    Class for sending subscribers emails
    """
    def __init__(self, info):
        self._password = password
        self._login = login
        self._subscriber_emails = d.Database().get_subscribers()
        self._sender = "3stat.signals@gmail.com"
        self._port = 465
        self._info = info

    # Get Methods
    def get_info(self):
        """
        Returns self._info
        """
        return self._info

    def get_sender(self):
        """
        Returns self._sender
        """
        return self._sender

    def get_port(self):
        """
        Returns self._port
        """
        return self._port

    def get_password(self):
        """
        Returns self._password
        """
        return self._password

    def get_login(self):
        """
        Returns self._login
        """
        return self._login

    def get_subscriber_emails(self):
        """
        Returns subscriber emails
        """
        return self._subscriber_emails

    def send_email(self):
        """
        Sends signal emails
        """
        print("IN EMAIL")
        port = self._port
        context = ssl.create_default_context()
        info = self.get_info()
        message = self.compose_email(info)

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(self.get_login(), self.get_password())
            server.sendmail(self.get_sender(), ([self.get_sender()] + (self.get_subscriber_emails())), message)

    def compose_email(self, info):
        """
        Composes and formats the email
        """
        print(info)
        message = MIMEMultipart("alternative")
        message["From"] = self.get_sender()
        message["To"] = self.get_sender()
        message["Subject"] = "[3STAT] ---> New Signal"

        text = """\
        A New Signal From 3STAT!
        {4}
        {0}!
        {1} at ${3}
        Currently Invested: {2}%
        
        https://www.cstodd.dev/3stat
        This is not intended as financial advice.  Invest at your own risk.""".format(info["signal"], info["ticker"], info["total_invested"], info["closing"], info["date"])

        html = """\
        <html>

<body>
    <div style="text-align:center">
        <h1>A New Signal From 3STAT!</h1>
        <h2>{5}</h2>
    </div>
    <br><br>
    <div style="text-align:center">
        <p style="color:{0}"><strong>{1}!</strong></p>
    </div>
    <div style="text-align:center">
        <p><strong>{2}</strong> at ${4}</p>
    </div>
    <div style="text-align:center">
        <p>Total Portfolio Invested: {3}%</p>
    </div><br>
    <div style="text-align:center">
        <p style=><a href="https://www.cstodd.dev/3stat">3STAT</a></p>
    </div><br>
    <br><br>
    <div style="text-align:center">
        <p>This is not intended as Financial Advice. Investment carries risks, invest at your own risk.</p>
    </div><br>

</body>

</html>
        """.format("green" if info["signal"] == "BUY" else "red", info["signal"], info["ticker"], info["total_invested"], info["closing"], info["date"])

        print(html)

        plain_text = MIMEText(text, "plain")
        html_text = MIMEText(html, "html")

        message.attach(plain_text)
        message.attach(html_text)

        return message.as_string()
