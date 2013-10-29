.. _development:

Development
===========

So you want to extend analys with your own use cases? Awesome! Heres how.

Initial Steps
-------------

Before you start development there are a couple things you will need to know
to get started. The following steps that you are already familure with the Python
programming language and the development of Python modules.

If you think that your module would be useful to others you are more than welcome
to share you code with others. If you want your plugin to be considered for inclusion
into Analys itself, there are a few things to consider:

* Code must use the same LICENSE as Analys
* Code must try to follow PEP8
* Code must make an effort to have some test coverage, and be documented in the 
  same style as the rest of the Analys codebase

That's it! Send a pull request, the more the merrier!

Requirements
------------

Every Analys plugin needs three files in order to function

1. \_\_init\_\_.py 
2. \*.analys-plugin
3. plugin.py


\_\_init\_\_.py
---------------

If you are familure python packaging you know that in order to import a module
the directory that contains the module requires a \_\_init\_\_.py in said directory.

\*.analys-plugin
----------------

This file serves two purposes. First the existance of this file in a directory signifies 
that it is indeed an Analys plugin and that Analys should attempt to load it. Secondly 
the file holds the configuration for that plugin. What this means is that this file 
would be where you would define any plugin level defaults your plugin might need.

Lets take a look at an example::

    [Core]
    Name = Pdfid
    Module = pdfid
    DataType = File
    ProcessType = Static
    Extensions = pdf

    [Documentation]
    Author = Kevin Glisson (kevin.glisson@gmail.com)
    Version = 1.0
    Description = "Scans PDF files"


There are two main sections to an Analys config file [Core] and [Documentation]. The
documentation section is used for informational purposes only and does not effect the
operation of Analys. 

Lets breakdown the [Core] section of the configuration file::

    Module = pdfid

This attribute describes which directory our plugin module resides. Analys uses this information
to correctly load the plugin in question this attribute **must** match the directory else it
will not be loaded correctly::

    DataType = File

There are currently two different DataTypes that are suppored by Analys, File and URL. This
attribute tells analys type of data the plugin can process. It is important to note that a plugin
can support multiple DataTypes as long as they are comma seperated like so ``DataType = File,URL``.::

    Extensions = pdf

Here we go beyond the DataType our plugin can handle and define the actual extensions which the plugin
is able to process. This is only needed for plugins that can also handle file datatypes.
Analys uses mimestypes to match files to their extensions. If you find that Analys is unable to currently
handle your type of file, you may need to add additional mapping. This process is described in the 'File Support' 
section of the documentation.

plugin.py
---------

This is the actual file that is instanciated and then executed by Analys. You can thing of it as the entrypoint
or 'main' method of your plugin.

Lets look at an example::

    from analys.plugins.plugin import Plugin

    class AnalysPlugin(Plugin):
        def __init__(self, *args, **kwargs):
            super(AnalysPlugin, self).__init__(*args, **kwargs)

        def submit(self):
            result = "I am an example plugin"
            self.insert(result)

Above we can see a very basic plugin. The important part here is the the submit() function is the 
entry point the application and the AnalysPlugin object inherts a wealth of useful variables and 
functions for communication with Analys resource such as queues and datastore.



