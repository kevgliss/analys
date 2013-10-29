.. _api:

API Interface
===================

.. module:: analys.views

This part of the documentation covers all the web interfaces of Analys.  For
parts where Analys depends on external libraries, we document the most
important right here and provide links to the canonical documentation.


Endpoints
---------

All of Analys endpoints are defined below.

.. autoclass:: analys.views.Submissions
   :members: get, collection_get, collection_post, delete

.. autoclass:: analys.views.Tasks
   :members: get, collection_get, collection_post, delete

.. autoclass:: analys.views.Results
   :members: get, collection_get, collection_post, delete

.. autoclass:: analys.views.Workflows
   :members: get, collection_get, collection_post, delete


Lower-Level Classes
~~~~~~~~~~~~~~~~~~~

Exceptions
~~~~~~~~~~

.. autoexception:: analys.exceptions.AnalysException
.. autoexception:: analys.exceptions.ResourceNotFound
.. autoexception:: analys.exceptions.InvalidResourceType
.. autoexception:: analys.exceptions.MimeTypeNotFound
.. autoexception:: analys.exceptions.EmptyCompressedFile
.. autoexception:: analys.exceptions.MaxFileDepth


Classes
~~~~~~~


