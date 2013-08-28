# Front end related data
FRONTEND_HOST = '0.0.0.0'
FRONTEND_PORT = 8080
FRONTEND_PREFIX = ''
FRONTEND_THEME = 'default'
TEMPLATES_PATH = 'templates'
SITE_NAME = 'GeoHolmes Demo'
CONTACT_MAIL = 'tobeedited@pwet.com'

# Data related to caches
CACHE_PATH = 'caches/'

# Misc
SECRET_KEY = '<your_secret_(random_string)>'
DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

# OAuth
API_CONSUMER_KEY      = '<your_key_here>'
API_CONSUMER_SECRET   = '<your_secret_here>'

# Assuming you are using staging API (You'll need to edit this when going into
# production)
API_BASE_URL          = 'https://staging.api.groundspeak.com/Live/v6beta/geocaching.svc/'
API_REQUEST_TOKEN_URL = 'https://staging.geocaching.com/OAuth/oauth.ashx'
API_ACCESS_TOKEN_URL  = 'https://staging.geocaching.com/OAuth/oauth.ashx'
API_AUTHORIZE_URL     = 'https://staging.geocaching.com/OAuth/oauth.ashx'
