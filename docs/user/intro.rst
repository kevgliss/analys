.. _introduction:

Introduction
============

Malware impact assessment and orchestration tool.

The malware tool space as begun to develop very rapidly in
last few years. Some of the tools are simple scripts to 
analyze malware an interesting way, others are SaaS providers
using amazing analytical and machine learning algorithms to
mine IOCs out of terabytes of data. 

With all of these tools in available it is becoming increasingly
hard to manage all the information that these tools are exporting.

Analys is an attempt to wrangle some of of those different data
sources and provide a malware anaylst/incident responder a framework
to automated some of those tasks.

See relevant XKCD: http://xkcd.com/927/

With that said it is important to realize that Analys does little to
no actual malware processing/correlation itself. Instead it relies on plugins
that allow each individual to customize it to their specific workflow/environment.

Philosophy
----------

Analys was developed to power back to analysts looking to streamline
their malware analysis. It should not have any unbreakable or deep dependencies 
of third-party or close security tools.

.. _`apache2`:

Goals
----
- It should provide allow itself to be configured for a specific environment.

- It should provide entry points that allow both the ingestion and exportation of data.
Information wants to be free.

- It should not do any actual analysis itself. It should present data from it's
plugins in a clean and logical way, and get out of the analysts way.

Plugins
-------
Anyone can write a plugin allowing them to customize
analys for their network environment and toolset.

Only a handful of plugins will be merged into core while the rest will be available seperately. Becuase malware analysis tools tend to have sometimes difficult dependencies, the plugins in core will focus on getting analys up and running and start being useful as quickly as possible.

User contributed plugins will be graciously accepted and merged upstream, provided A)They work, and B)
They following some basic coding and testing concepts.

Please see the plugin documentation for examples on how to write your
own.


Architecture
-----
Analys is built on angularjs, python, mongodb and redis. All tasks are handled
asynchronously by as many task workers you decide to run. Obviously
the more workers the increased throughput analys will have. 

The analys webui is built with angularjs and is entirely optional. Analys is an 'API First' application, wherein all core functionality should be available through the API. If you skip out on the UI and only use the CLI you will miss out on some workflow nicities, but nothing that is a show stopper.

MongoDB is used as the datastore although additional datastores
will be considered in the future. 

Analys has only been `tested` on Mac OS X and Ubuntu Server Latest but should work on 
any unix like system. The hardest dependencies will based on which plugins you wish to install/develop.

An installer will be made for a few different unix distributes, but
running all of the projects tests is a good way to ensure compatibility.

Running Analys on Windows will not be supported. Feel free to fork if you have requirements to run on windows.

Each plugin will have additional dependencies/environmental needs
Before installing a plugin ensure it's tests pass.


Apache2 License
---------------

A large number of open source projects you find today are `GPL Licensed`_.
While the GPL has its time and place, it should most certainly not be your
go-to license for your next open source project.

A project that is released as GPL cannot be used in any commercial product
without the product itself also being offered as open source.

The MIT, BSD, ISC, and Apache2 licenses are great alternatives to the GPL
that allow your open-source software to be used freely in proprietary,
closed-source software.

Analys is released under terms of `Apache2 License`_.

.. _`GPL Licensed`: http://www.opensource.org/licenses/gpl-license.php
.. _`Apache2 License`: http://opensource.org/licenses/Apache-2.0


Analys License
----------------

    .. include:: ../../LICENSE
