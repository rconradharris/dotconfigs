==========
Dotconfigs
==========

Description
===========

The goal here is: "One set of dotconfigs, anywhere in the world."

The setup.py script will:

    1. Install `git` (if don't already have it)
    2. Clone the canonical dotconfigs repository if it doesn't exist, or
       `git pull` if it does
    3. Backup any existing dotconfig files
    4. Symlink your dotconfig files into the dotconfig repository

Later on, when your dotconfigs need updating, just type::

    cd ~/.dotconfigs.git
    git pull origin

Installation
============

    1. Setup your user and add sudo privilges
    2. On the command-line run::

        wget -q http://github.com/downloads/rconradharris/dotconfigs/setup-0.1.0.py && python setup-0.1.0.py --os-flavor=debian --quick-start personal rick

Options
=======

    *  *dry_run* - log what would be done rather than actually doing it
    *  *undo* - most operations are reversible, use undo to attempt a recovery.

Caveats
=======

This project is very EXPERIMENTAL, use at your own risk!

License
=======

`WTFPL 2.0 <http://sam.zoy.org/wtfpl/COPYING>`_

Author
======

    * Rick Harris (rconradharris@gmail.com)
