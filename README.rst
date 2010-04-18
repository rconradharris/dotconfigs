==========
Dotconfigs
==========

Description
===========

The goal of this project is to provide an easy way to keep my dotconfig files
in sync across a wide-variety of systems. The dotconfigs git repo holds my
canonical dotconfig files which is then checked out on the hostmachined and
symlinked into the homedir. To use latest dotconfigs, just type::

    git pull origin

Installation
============

On command-line run::

    wget -q http://github.com/downloads/rconradharris/dotconfigs/setup-0.1.0.py && python setup-0.1.0.py --os-flavor=debian --quick-start personal rick

Caveat
======

This project is very EXPERIMENTAL, use at your own risk!

Author
======

    * Rick Harris (rconradharris@gmail.com)
