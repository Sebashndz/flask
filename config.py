SECRET_KEY = "13a8e3fe0dd8ea765284de02bdf830c342a203cf5487235083751fc76cf9f3f1a59dc978a095939067bea0c39287c8447938921ad66f641ef0983f34b2a8482d1b7b83014f0a0e3fed27b57da5530d81d176d019abed0cc8de55c0f26958f008f3c351906b17727ea07bf29513c117010f7210589e524555fb056d9eed24b72b"
SQLALCHEMY_DATABASE_URI = (
    "mssql+pyodbc_mssql://sa:Laniakea628@localhost:1433/Divisa?driver=FreeTDS"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
# BABEL_DEFAULT_LOCALE = "es"
# BABEL_DEFAULT_TIMEZONE = "America/Bogotá"
# Flask-Mail SMTP server settings
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = "divisaonenotificaciones@gmail.com"
MAIL_PASSWORD = "admindivisa"
MAIL_DEFAULT_SENDER = '"Divisa One" <noreply@divisas.com>'
# Flask-User settings
USER_APP_NAME = "Divisa One"  # Shown in and email templates and page footers
USER_ENABLE_EMAIL = True  # Enable email authentication
USER_ENABLE_USERNAME = False  # Disable username authentication
USER_EMAIL_SENDER_NAME = USER_APP_NAME
USER_EMAIL_SENDER_EMAIL = "noreply@example.com"
# USER_LOGIN_URL = "/login"
USER_LOGIN_TEMPLATE = "login_form.html"
USER_ENABLE_REGISTER = False
USER_FORGOT_PASSWORD_TEMPLATE = "forgot_password.html"
USER_EDIT_USER_PROFILE_TEMPLATE = "user_account.html"
USER_CHANGE_PASSWORD_TEMPLATE = "change_password.html"
USER_CHANGE_PASSWORD_URL = '/change-password'
USER_EDIT_USER_PROFILE_URL= '/edit_user_profile'
USER_RESET_PASSWORD_URL = '/reset-password/<token>'
USER_ENABLE_FORGOT_PASSWORD = True
USER_RESET_PASSWORD_TEMPLATE = '/reset_password.html'