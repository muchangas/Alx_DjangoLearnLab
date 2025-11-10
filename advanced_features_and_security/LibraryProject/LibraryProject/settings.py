INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'users'
]

AUTH_USER_MODEL = 'users.CustomUser'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# LibraryProject/settings.py
bookshelf.CustomUser
"SECURE_PROXY_SSL_HEADER", "HTTP_X_FORWARDED_PROTO"
# ... existing imports and settings ...

# --- Production Security Configuration (Step 1) ---

# CRITICAL: Set DEBUG to False in production
DEBUG = False

# Host configuration (REQUIRED when DEBUG=False)
ALLOWED_HOSTS = ['yourdomain.com', 'localhost', '127.0.0.1'] 
# Replace with your actual domain(s) in a real deployment

# SECURITY HEADERS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY' # Prevents clickjacking by denying framing

# COOKIE SECURITY (Assumes HTTPS is used in production)
CSRF_COOKIE_SECURE = True   # Ensures CSRF cookie is only sent over HTTPS
SESSION_COOKIE_SECURE = True # Ensures session cookie is only sent over HTTPS
# CSRF_COOKIE_HTTPONLY = True # Recommended: Prevents client-side JS access
# SESSION_COOKIE_HTTPONLY = True # Recommended: Prevents client-side JS access

# If serving over HTTPS, consider enabling HSTS (HTTP Strict Transport Security)
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000 # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True


# --- Content Security Policy (CSP) Setup (Step 4) ---

# Add the CSP middleware
MIDDLEWARE = [
    # ... existing middleware ...
    'csp.middleware.CSPMiddleware', # Add django-csp middleware
    # ... existing middleware ...
]

# CSP Configuration Directives
# This is a strict policy example. You must customize this based on your needs.
CSP_DEFAULT_SRC = ("'self'",) # Default source must be 'self'
CSP_SCRIPT_SRC = ("'self'", "https://cdn.example.com") # Allow scripts only from own domain and a specific CDN
CSP_STYLE_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:") # Allows images from own domain and inline data URLs
CSP_FONT_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)
CSP_BASE_URI = ("'self'",)
CSP_FRAME_ANCESTORS = ("'self'",) # Prevents external sites from embedding your content

# LibraryProject/settings.py

"""
----------------------------------------------------------------------
STEP 5: Security Best Practices Documentation
----------------------------------------------------------------------

1. Production Settings:
   - DEBUG is set to False, which is mandatory for production.
   - ALLOWED_HOSTS is configured to prevent HTTP Host Header attacks.

2. Browser Protections (Step 1):
   - X_FRAME_OPTIONS = 'DENY': Mitigates Clickjacking attacks.
   - SECURE_BROWSER_XSS_FILTER = True: Activates browser-side XSS filtering.
   - SECURE_CONTENT_TYPE_NOSNIFF = True: Prevents MIME type sniffing.

3. Cookie Security (Step 1):
   - CSRF_COOKIE_SECURE = True: Ensures the CSRF cookie is only sent over HTTPS.
   - SESSION_COOKIE_SECURE = True: Ensures the Session cookie is only sent over HTTPS.

4. CSRF Protection (Step 2):
   - All forms use the {% csrf_token %} tag in templates. Django's middleware handles checking this token on POST requests.

5. SQL Injection Prevention (Step 3):
   - Views (e.g., secure_search_books) use the **Django ORM** (`Book.objects.filter(...)`) exclusively. This ensures all user input is parameterized and properly escaped by the database driver, effectively preventing SQL injection.

6. Content Security Policy (Step 4):
   - The 'csp.middleware.CSPMiddleware' is integrated.
   - CSP headers are configured to restrict resource loading (scripts, styles, etc.) to trusted sources ('self' and defined CDNs), significantly reducing the risk of XSS attacks by controlling which content the browser can execute.

----------------------------------------------------------------------
"""

# LibraryProject/settings.py

# ... existing imports and settings ...

# --- Production Security Configuration (Step 1) ---

# CRITICAL: Set DEBUG to False in production
DEBUG = False

# Host configuration (REQUIRED when DEBUG=False)
ALLOWED_HOSTS = ['yourdomain.com', 'localhost', '127.0.0.1'] 
# Replace with your actual domain(s) in a real deployment

# SECURITY HEADERS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY' # Prevents clickjacking by denying framing

# COOKIE SECURITY (Assumes HTTPS is used in production)
CSRF_COOKIE_SECURE = True   # Ensures CSRF cookie is only sent over HTTPS
SESSION_COOKIE_SECURE = True # Ensures session cookie is only sent over HTTPS
# CSRF_COOKIE_HTTPONLY = True # Recommended: Prevents client-side JS access
# SESSION_COOKIE_HTTPONLY = True # Recommended: Prevents client-side JS access

# If serving over HTTPS, consider enabling HSTS (HTTP Strict Transport Security)
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000 # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True


# --- Content Security Policy (CSP) Setup (Step 4) ---

# Add the CSP middleware
MIDDLEWARE = [
    # ... existing middleware ...
    'csp.middleware.CSPMiddleware', # Add django-csp middleware
    # ... existing middleware ...
]

# CSP Configuration Directives
# This is a strict policy example. You must customize this based on your needs.
CSP_DEFAULT_SRC = ("'self'",) # Default source must be 'self'
CSP_SCRIPT_SRC = ("'self'", "https://cdn.example.com") # Allow scripts only from own domain and a specific CDN
CSP_STYLE_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:") # Allows images from own domain and inline data URLs
CSP_FONT_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)
CSP_BASE_URI = ("'self'",)
CSP_FRAME_ANCESTORS = ("'self'",) # Prevents external sites from embedding your content

# LibraryProject/settings.py

"""
----------------------------------------------------------------------
STEP 5: Security Best Practices Documentation
----------------------------------------------------------------------

1. Production Settings:
   - DEBUG is set to False, which is mandatory for production.
   - ALLOWED_HOSTS is configured to prevent HTTP Host Header attacks.

2. Browser Protections (Step 1):
   - X_FRAME_OPTIONS = 'DENY': Mitigates Clickjacking attacks.
   - SECURE_BROWSER_XSS_FILTER = True: Activates browser-side XSS filtering.
   - SECURE_CONTENT_TYPE_NOSNIFF = True: Prevents MIME type sniffing.

3. Cookie Security (Step 1):
   - CSRF_COOKIE_SECURE = True: Ensures the CSRF cookie is only sent over HTTPS.
   - SESSION_COOKIE_SECURE = True: Ensures the Session cookie is only sent over HTTPS.

4. CSRF Protection (Step 2):
   - All forms use the {% csrf_token %} tag in templates. Django's middleware handles checking this token on POST requests.

5. SQL Injection Prevention (Step 3):
   - Views (e.g., secure_search_books) use the **Django ORM** (`Book.objects.filter(...)`) exclusively. This ensures all user input is parameterized and properly escaped by the database driver, effectively preventing SQL injection.

6. Content Security Policy (Step 4):
   - The 'csp.middleware.CSPMiddleware' is integrated.
   - CSP headers are configured to restrict resource loading (scripts, styles, etc.) to trusted sources ('self' and defined CDNs), significantly reducing the risk of XSS attacks by controlling which content the browser can execute.

----------------------------------------------------------------------
"""
