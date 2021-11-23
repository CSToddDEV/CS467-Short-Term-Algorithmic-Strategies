from flask_mail import Message

from flask_back_end.app import mail
from flask_back_end.models.users import Users


def get_users_no_auth():
    """
    Gets all user emails
    returns: User Emails stored in db
    """
    return Users.objects()


def email_signals(signals):
    """
    :param signals: Buy and sell signals as a dict object
    Emails signals to users emails
    returns: None
    """
    users = get_users_no_auth()
    with mail.connect() as conn:
        for user in users:
            subject = f"Updated Signals from 3STAT for, {user.name}"
            message = f"The signal is {signals['signal']} for {signals['ticker']} on {signals['date']}" \
                      f"\nThe total invested portfolio amount should be adjusted to {signals['total amount']}." \
                      f"\nThe opening price today was {signals['opening_price']} " \
                      f"with a closing price {signals['closing_price']}"

            msg = Message(recipients=[user.email],
                          body=message,
                          subject=subject)
            conn.send(msg)
