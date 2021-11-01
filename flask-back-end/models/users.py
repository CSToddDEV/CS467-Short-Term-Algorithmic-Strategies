# flask resources
from flask_bcrypt import generate_password_hash, check_password_hash

# mongodb resources #
###
from mongoengine import(Document,
                        EmbeddedDocument,
                        EmbeddedDocumentField,
                        ListField,
                        StringField,
                        EmailField,
                        BooleanField,
                        ReferenceField)

# Local resources
from models.tickers import Ticker

# External Resources
import re


class Access(EmbeddedDocument):
    """Custom EmbeddedDocument to set user authorizations.
    
    :param user: boolean to signifiy if user is a user
    :param admin" boolean to signify if user is an admin
    """
    user = BooleanField(default=True)
    admin = BooleanField(default=True)
    
class PhoneField(StringField):
    """Custom StringField to verify phone numbers
    
    US Phone Number that accepts a dot, space, daash, forward slash between numbers.
    Will accept a 1 or 0 in front. Area code is not required
    """
    REGEX = re.compile(r"((\(\d{3}\)?)|(\d{3}))([-\s./]?)(\d{3})([-\s./]?)(\d{4})")
    
    def validate(self, value):
        if not PhoneField.REGEX.match(string=value):
            self.error(f"ERROR: `{value}` Is An Invalid Phone Number.")
        super(PhoneField, self).validate(value=value)


class Users(Document):
    """
    Template for a mongoengine document, which represents a user.
    Password is automatically hashed before saving.
    :param password: required string value, longer than 6 characters
    :param access: Access object
    :param tickers_tracked: ListField
    :param phone: optional string phone-number, must be valid via regex
    :param email: unique required email-string value
    """
    password = StringField(required=True, min_length=6, regex=None)
    email = EmailField(required=True, unique=True)
    access = EmbeddedDocumentField(Access, default=Access(user=True, admin=False))
    tickers_tracked = ListField(ReferenceField(Ticker))
    phone = PhoneField()

    def generate_pw_hash(self):
        self.password=generate_password_hash(password=self.password).decode('utf-8')

    # From BCrypt documentation
    generate_password_hash.__doc__ = generate_password_hash.__doc__

    def check_pw_hash(self, password:str) -> bool:
        return check_password_hash(pw_hash=self.password, password=password)

    # From BCrypt documentation
    check_pw_hash.__doc__ = check_password_hash.__doc__

    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash prior to saving
        if self._created:
            self.generate_pw_hash()
        super(Users, self).save(*args, **kwargs)