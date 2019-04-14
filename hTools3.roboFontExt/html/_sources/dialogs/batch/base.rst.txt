====
base
====

All Batch dialogs are created by subclassing from :class:`BatchDialogBase` or :class:`BatchDialogBaseCopy` to inherit common batch functionality:

- choosing font files from a folder
- creating unique font IDs
- managing a list of target fonts

Each base object handles a different batch action pattern:

- :class:`BatchDialogBase`: doing something to a set of fonts
- :class:`BatchDialogBaseCopy`: copying something from one font to a set of fonts

----

.. automodule:: hTools3.dialogs.batch.base
