import urllib2, random, hashlib, uuid, re

class MxitGa:

    _base_url = 'http://www.google-analytics.com/__utm.gif' # Google Analytics tracking GIF

    def __init__(self, analytics_id, track_anonymous=False):
        """
        Construct Google Analytics for Mxit class.

        `analytics_id` - Google Analytics account ID to track events against.
        `track_anonymous` - if requests without a Mxit user ID header should be tracked.
        """
        self._analytics_id = analytics_id
        if (self._analytics_id.startswith('UA-')):
            self._analytics_id = self._analytics_id.replace('UA-', 'MO-')
        self._track_anonymous = track_anonymous

    def track_page(self, headers, client_ip, host, path, query_string=None):
        """
        Track a page view event.

        `headers` - dictionary-like object containing the HTTP headers for the request.
        `client_ip` - IP address of the remote client requesting the page.
        `host` - hostname of the server.
        `path` - path to the requested page (this may already include the query string).
        `query_string` - query string component of the URL (optional).
        """   

        user_id = headers.get('X-Mxit-USERID-R', None) # unique identifier for user

        if not user_id and not self._track_anonymous:
            return True # return without error

        visitor_id = self._visitor_id(user_id)

        path = path
        if query_string and path.find(query_string) == -1:
            # add query string to path if defined (and not already included in path)
            path += '?' + query_string

        ga_params = self._build_ga_params(headers, client_ip, host, path, query_string)

        ga_headers = self._build_ga_headers(headers)

        return self._make_ga_request(ga_params, ga_headers)

    def _make_ga_request(self, ga_params, ga_headers):
        """
        Make a request to the Google Analytics tracking service.

        `ga_params` - the query string parameters to include in the request.
        `ga_headers` - the HTTP headers to include in the request.
        """

        url = self._build_url(ga_params)

        ga_request = urllib2.Request(url=url)
        [ga_request.add_header(x[0], x[1]) for x in ga_headers.items()]

        try:
            urllib2.urlopen(ga_request) # just make request, no need to read response
        except:
            return False

        return True

    def _build_ga_params(self, headers, client_ip, host, path, query_string):
        user_id = headers.get('X-Mxit-USERID-R') # unique identifier for user

        visitor_id = self._visitor_id(user_id)

        path = path
        if query_string and path.find(query_string) == -1:
            # add query string to path if defined (and not already included in path)
            path += '?' + query_string

        ip_address = self._ip_address(headers, client_ip)

        ga_params = {
            'utmvid': visitor_id,
            'utmwv': '4.4sh', # analytics version
            'utmr': headers.get('Referer', '-'),
            'utmsr': headers.get('UA-Pixels', '-'),
            'utmp': urllib2.quote(path),
            'utmhn': urllib2.quote(host),
            'utmn': random.randint(0, 2**31-1), # is this necessary to prevent server-side caching?
            'utmcc': urllib2.quote('__utma=999.999.999.999.999.1;'), # cookie settings
            'utmip': ip_address,
        }
        
        return ga_params        

    def _build_ga_headers(self, headers):
        user_agent = headers.get('X-Device-User-Agent', None)
        if not user_agent:
            user_agent = headers.get('User-Agent', 'Unknown')

        accept_language = headers.get('Accept-Language', None)
        if not accept_language:
            accept_language = 'en-US,en;q=0.5' # use a sensible default for language

        ga_headers = {
            'User-Agent': user_agent,
            'Accept-Language': accept_language,
        }

        return ga_headers     

    def _visitor_id(self, user_id=None):
        """
        Generate a visitor ID from a Mxit user ID.
        If the Mxit ID is not supplied, then a GUID will be generated.
        Only the first 16 characters of the hex SHA-1 value will be used.

        `user_id` - Mxit ID of the current user.
        """
        if user_id:
            id = user_id
        else:
            id = str(uuid.uuid4())
        hash = hashlib.sha1(id)
        visitor_id = hash.hexdigest()[0:16] # get hex value and anonymise data
        return '0x' + visitor_id            

    def _ip_address(self, headers, client_ip):
        """
        Attempt to get the IP address of the user from the request headers.
        The IP address of the Mxit proxy will be used if the user IP address cannot be determined.
        The first three octets of the IP address are returned with the fourth being replaced with 0.

        `headers` - HTTP headers for the request.
        `client_ip` IP address of the client device (the Mxit proxy).
        """
        ip = headers.get('X-Forwarded-For', '')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = client_ip
        if not ip:
            return '-'
        # replace last octet of IP with '0'
        ip = re.sub(r'([0-9]+\.[0-9]+\.[0-9]+\.)[0-9]+', r'\g<1>0', ip)
        return ip

    def _build_url(self, params):
        """
        Construct the URL using the base URL and the supplied query string parameters.
        """
        param_strings = ['&{0}={1}'.format(x[0], x[1]) for x in params.items()]
        query_string = ''.join(param_strings)
        url = '{0}?utmac={1}{2}'.format(self._base_url, self._analytics_id, query_string)
        return url
