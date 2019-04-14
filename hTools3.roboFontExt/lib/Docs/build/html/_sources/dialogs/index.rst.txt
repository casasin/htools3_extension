=======
Dialogs
=======

.. toctree::
   :hidden:
   :maxdepth: 1

   glyphs/index
   font/index
   batch/index
   glyph/index
   proof/index
   misc/index

Overview
--------

hTools3 dialogs are organized around common patterns or scopes in font production tasks:

- :doc:`Glyphs <glyphs/index>`: applying actions to selected glyphs in the current font
- :doc:`Font <font/index>`: applying font-level actions to a font
- :doc:`Batch <batch/index>`: applying an action to several fonts at once
- :doc:`Glyph <glyph/index>`: visualising and transforming single glyphs in the glyph window
- :doc:`Proof <proof/index>`: generating different kinds of proofs for the current font

Single dialogs are created using object inheritance. All dialogs inherit from the :class:`hDialog` class, which defines the basic look’n’feel and generic functionality. *Batch* and *Glyphs* dialogs inherit from higher-level :doc:`BatchDialogBase <batch/base>` and :doc:`GlyphsDialogBase <glyphs/base>` classes.

- :doc:`Misc <misc/index>`: widgets and components for use in hTools3 dialogs.

API
---

.. automodule:: hTools3.dialogs
