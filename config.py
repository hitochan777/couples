# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

############### Azureの設定 ####################
FACE_API_CONFIG = {
    "KEY": 'c47c7f33d73a4d1b8a8dff1f679e6b2f',
    "ENDPOINTS": {
        "ROOT": {
            "HOST": "westus.api.cognitive.microsoft.com",
            "PATH": "/face/v1.0"
        }
    }
}

SEARCH_API_CONFIG = {
    "KEY": 'f1fc704a989a48cca6a10f099627a843',
    "ENDPOINTS": {
        "ROOT": {
            "HOST": "api.cognitive.microsoft.com",
            "PATH": "/bing/v5.0",
        },
        "IMAGE_SEARCH": {
            "HOST": "api.cognitive.microsoft.com",
            "PATH": "/bing/v5.0/images/search"
        }
    }
}

################################################

UPLOADED_IMAGES_DEST = BASE_DIR + '/app/static/img/'
UPLOADED_IMAGES_URL = '/static/img/'
