# Set the host, user, and passwords for each device
# Enter ASK for the password to always be prompted for it 
# Add more devices as needed

CISCO_DEVICES = [
    ('123.123.123.123', 'username', 'password'),
    ('123.123.123.124', 'username', 'password'),
    ('123.123.123.125', 'username', 'password'),
    ('123.123.123.126', 'username', 'password'),
    ('123.123.123.127', 'username', 'password')
    ]

APACHE_SERVERS = [
    ('10.10.10.10', 'username', 'password')
]

# Change the default directory Apache is located in 
# Do not include a trailing '/' 
APACHE_DIRECTORY = "/var/www"
APACHE_HTML_ROOT_DIR = "html"