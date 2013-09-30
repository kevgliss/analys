import re
import regex
from urlparse import urlparse

def deobfuscate(url):
    if not (regex.is_ipv4(url) or regex.is_ipv6(url)):
        url = re.sub('(?i)hxxp\:', 'http:', url)
        url = re.sub('(?i)hxxps\:', 'https:', url)
        url = re.sub('(?i)fxp\:\/\/', 'ftp://', url)
        url = re.sub('(?i)\[dot\]', '.', url)
        url = re.sub('(?i)\[\.\]', '.', url)
        url = re.sub('(?i)\ www\.', 'http://www.', url)

        if not url.startswith('http://'):
          if not url.startswith('www'):
              url = "".join(['www.', url])
          url = "".join(['http://', url])
    else:
        if not url.startswith('http://'):
          url = "".join(['http://', url])

    parsed = urlparse(url)

    return parsed.scheme, url
