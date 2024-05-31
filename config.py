# # config.py

DEBUG = True  # Turns on debugging features in Flask

BCRYPT_LEVEL = 12  # Configuration for the Flask-Bcrypt extension
BCRYPT_LOG_ROUNDS = 12
BCRYPT_HASH_PREFIX = "2b"
BCRYPT_HANDLE_LONG_PASSWORDS = False  # True

MAIL_FROM_EMAIL = "admin@kapsharma.in"  # For use in application emails
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"

# Flask-User settings
# Shown in and email templates and page footers
USER_APP_NAME = "Professor Research Work App"
USER_ENABLE_EMAIL = False      # Disable email authentication
USER_ENABLE_USERNAME = True    # Enable username authentication
USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form

# My App User settings
#Roles
ADMIN = "Admin" # SuperUser
GUIDE = "Guide" # Superviser / Guide / Mentor ...
STUDENT = "Student" # Project / Thesis Student
# Username and password length
MINUNAME = 5
MINPASWD = 8
MAXNUNAME = 50
MAXPASWD = 30

# Paper settings
MAXKEYWORDS = 10

# File Upload Setting
MAX_CONTENT_LENGTH = 25 * 1024 * 1024 * 8 # 25 MB size
