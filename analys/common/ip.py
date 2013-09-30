"""
.. module: ip
    :platform: Unix
    :synopsis: This simple module uses the socket module
    to attempt to verify a real ip address.

.. version:: 1.0
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
"""
import socket

def is_ipv4(address):
    """ Returns True if address is a valid ipv4 address,
        returns false otherwise.

    """
    try:
        addr= socket.inet_pton(socket.AF_INET, address)
    except AttributeError: # no inet_pton here, sorry
        try:
            addr = socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error: # not a valid address
        return False

    return True

def is_ipv6(address):
    """ Returns True if address is a valid ipv6 address,
        returns false otherwise.

    """
    try:
        addr= socket.inet_pton(socket.AF_INET6, address)
    except socket.error: # not a valid address
        return False
    return True
