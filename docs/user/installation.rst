Installation
==============

Analys needs the following in order function:
+ Python 2.7+, Python 3 is not yet supported
+ Redis
+ MongoDB

Clone Analys into the newly created virtualenv:
    git clone https://github.com/kevgliss/analys.git

The easiest way to get a installation of Analys up and running
is to run the install script and answer all configuration questions.

    python installer install

At its core Analys is a simple python modules, if you already have mongodb
and redis servers setup on different machines you can also run the install 
(it will ask you if you need those services) or you can simply do the following:

Make a new virtualenv anywhere you would like:
    virtualenv Analys

Install the project into the virutalenv:
    source Analys/bin/activate
    python analys/setup.py install

Thats it! Anayls is now installed, make sure you run all of the tests to make sure everything
looks good:
    py.test Analys
