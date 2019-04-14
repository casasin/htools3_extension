==================
Installing hTools3
==================

Installing the extension
------------------------

Using Mechanic 2
^^^^^^^^^^^^^^^^

hTools3 is a paid extension available from the Extension Store. It be can be licensed and installed in RoboFont 3 using `Mechanic 2`_, an extension to manage other extensions. Mechanic 2 allows you to check for updates and easily upgrade your extension to the latest version.

1. install the `Mechanic 2 extension`_
2. open Mechanic and find hTools3 in the list of extensions
3. double click to install

If you haven’t bought a license for hTools3 yet, you will be directed to a payment page first. Users with a license can install/uninstall and update hTools3 using the Mechanic interface.

.. _Mechanic 2: http://robofontmechanic.com/
.. _Mechanic 2 extension: http://github.com/robofont-mechanic/mechanic-2

Manual installation
^^^^^^^^^^^^^^^^^^^

The extension can also be installed manually by double-clicking the file ``hTools3.roboFontExt``.

.. note:: By installing the extension manually you will **not** be notified of updates.

Installing from source
----------------------

If you have access to the hTools3 source code, you can use it directly (without of installing the extension).

hTools3 includes an initialization script which:

- adds the ``hTools3`` module to the ``sys.path``
- adds a *hTools3* entry to the RoboFont application menu

To install hTools3 directly from the source, open and run the script ``hTools3/Lib/start.py`` in RoboFont’s scripting window.

To install hTools3 permanently – so it is available every time you start RoboFont – set ``start.py`` as a start-up script in *Preferences > Extensions > Start Up Scripts*.
