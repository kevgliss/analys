"""
.. module:: symantec
    :platform: Unix
    :synopsis: A module used for interaction with the symantec web portal
.. moduleauthor:: Kevin Glisson <kevin.glisson@jpmchase.com>

"""

import mechanize
import magic
import logging

log = logging.getLogger(__file__)

class Symantec(object):
    """ This is a symantec object. It will submit a file to
        the platinum webportal
        An example of using the symantec class is:
       >>> s = Symantec(file, firstname, lastname, email)
       >>> s.submit()
    """
    def __init__(self, fileblob, fname, lname, email, company, pin):
        """ Symantec init function

        :param maliciousfile: maliciousfile
        :type maliciousfile: raw file data
        :param firstname: firstname
        :type firstname: str
        :param lastname: lastname
        :type lastname: str
        :param email: email
        :type email: str

	    """
        self.url = "https://submit.symantec.com/websubmit/platinum.cgi"
        self.firstname = fname
        self.lastname = lname
        self.email = email
        self.company = company
        self.pin = pin
        self.tmpfile = temporary.TemporaryFile(fileblob)

    def submit(self):
        br = mechanize.Browser()
        try:
            br.open(self.url)
            br.select_form(name="appform")
            br['fname'] = self.firstname
            br['lname'] = self.lastname
            br['cname'] = self.company
            br['email'] = self.email
            br['email2'] = self.email
            br['pin'] = self.pin
            f = open(self.tmpfile.path(), 'rb')
            mime = magic.from_file(self.tmpfile.path(), mime=True)
            br.form.add_file(f, mime, 'test')
            br.form.set_all_readonly(False)
            response = br.submit()
        except:
            self.log.error("Could not submit sample to symantec", exc_info=True)
            self.messages.append({"Symantec":
                {"Could not submit sample to symantec": {"type":"error"}}})

        self.tmpfile.remove()
        return response.read()
