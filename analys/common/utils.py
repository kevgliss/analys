"""
.. module: utils
    :platform: Unix
    :synopsis: Holds a few basic utils the pertain to analys

.. version:: 1.0
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
"""

def get_resource_type(resource):
    """ Simple function that correctly identifies the type of
        resource that is passed to it. 

        At the moment the only valid resource that a task is
        able to process is a url or file_id for a file that
        was previously stored in the datastore.

        This function's main use is to ensure that the correct
        plugins are executed against a resource it was designed 
        to handle.

        Ideally this function should be easily extendable to
        include other resource types in the future, md5s, sha1s, 
        uris, etc.

    """

    if '.' in resource:
        return 'URL'
    else:
        return 'FILE'



