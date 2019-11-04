# -*- coding: utf-8 -*-
from vanilla import FloatingWindow, CheckBox, PopUpButton, List, Button
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.roboFont import CurrentFont, CurrentGlyph, RGlyph, version
from mojo.events import addObserver, removeObserver
from mojo.glyphPreview import GlyphPreview
from mojo.UI import UpdateCurrentGlyphView
import drawBot
from drawBot.ui.drawView import DrawView
from moshikTools.modules.spinner import *

class ReplaceComponentsTool(BaseWindowController, hDialog):

    height    = 240
    width     = 360
    col_width = 160

    color_contours   = 0, 0, 1
    color_components = 0, 1, 0
    color_alternates = 1, 0, 0

    def __init__(self):
        # window setup
        self.w = FloatingWindow(
                (self.width, self.height),
                "replace component",
                minSize=(self.width, self.height))
        # sorting order
        x = y = p = self.padding
        self.w.sort_order = CheckBox(
                (x+2, y, -p, self.text_height),
                "sort alphabetically",
                sizeStyle='small',
                value=True,
                callback=self.sort_callback)
        # show colors
        y += self.text_height
        self.w.show_colors = CheckBox(
                (x+2, y, -p, self.text_height),
                "show colors",
                sizeStyle='small',
                value=True,
                callback=self.show_colors_callback)
        # components in current glyph
        y += self.text_height + p*0.75
        self.w.components_list = PopUpButton(
                (x, y, self.col_width, self.text_height),
                [],
                callback=self.get_selected_component_callback)
        # component alternates
        y += self.text_height + p
        col_height = -self.text_height - p*2
        self.w.all_glyphs_list = List(
                (x, y, self.col_width, col_height),
                [],
                allowsMultipleSelection=False,
                enableTypingSensitivity=True,
                selectionCallback=self.get_selected_alternate_callback)
        # replace component button
        y = -self.text_height - p
        self.w.replace_component_button = Button(
                (x, y, self.col_width, self.text_height),
                'replace component',
                sizeStyle='small',
                callback=self.replace_component_callback)
        # glyph preview
        y = p
        x += self.col_width + p
        self.w.canvas = DrawView((x, y, -p, -p))
        # setup window behaviour
        self.setUpBaseWindowBehavior()
        addObserver(self, "update_components_list", "currentGlyphChanged")
        # update components list
        g = CurrentGlyph()
        self.update_components(g)
        self.update_preview(g)
        self.load_glyphs_list()
        # done
        self.w.open()

    # dynamic attributes

    @property
    def selected_component(self):
        # get components
        components = self.w.components_list.getItems()
        if not len(components):
            return []
        # get selection
        component_selection = self.w.components_list.get()
        return components[component_selection]

    @property
    def selected_alternate(self):
        # get selection
        selection = self.w.all_glyphs_list.getSelection()
        if not len(selection):
            return
        alternates = self.w.all_glyphs_list.get()
        # get alternate
        return alternates[selection[0]]

    # callbacks

    def windowCloseCallback(self, sender):
        removeObserver(self, "currentGlyphChanged")
        super(ReplaceComponentsTool, self).windowCloseCallback(sender)

    def show_colors_callback(self, sender):
        self.update_preview(CurrentGlyph())

    def sort_callback(self, sender):
        self.load_glyphs_list()
        self.update_components(CurrentGlyph())

    def get_selected_component_callback(self, sender):
        self.update_preview(CurrentGlyph())

    def get_selected_alternate_callback(self, sender):
        # get font
        f = CurrentFont()
        if not f:
            return
        # update glyph view
        self.update_preview(CurrentGlyph())

    def replace_component_callback(self, sender):
        g = CurrentGlyph()
        if g is None:
            return
        self.replace_component(g, self.selected_component, self.selected_alternate)

    # observers

    def update_components_list(self, notification):
        g = notification['glyph']
        self.update_components(g)
        self.update_preview(g)

    # methods

    def load_glyphs_list(self):
        # get font
        f = CurrentFont()
        if not f:
            return
        # load glyph names
        if self.w.sort_order.get():
            self.w.all_glyphs_list.set(sorted(f.glyphOrder))
        else:
            self.w.all_glyphs_list.set(f.glyphOrder)

    def update_components(self, g):
        # get components list
        if g is None or not len(g.components):
            components = []
        else:
            components = [c.baseGlyph for c in g.components]
            # sort components list
            if self.w.sort_order.get():
                components.sort()
        # update UI list
        self.w.components_list.setItems(components)

    def replace_component(self, g, component, alternate):
        if component is None or alternate is None:
            return
        # replace matching component(s)
        g.prepareUndo('replace component')
        for c in g.components:
            if c.baseGlyph == component:
                c.baseGlyph = alternate

        if version >= "3.0":
            g.changed()
        else:
            g.update()

        g.performUndo()
        # update components list
        self.update_components(g)

    def update_preview(self, g):
        if g is None:
            return

        # get font
        try:
            # RF3 (new fontParts API)
            f = g.font
        except:
            # RF3 (old fontParts API) / RF1
            f = g.getParent()

        if not f:
            return

        # get options
        show_colors = self.w.show_colors.get()

        # make new document
        drawBot.newDrawing()
        drawBot.size('A4Landscape')

        # calculate scale
        margin = 100
        canvas_width = drawBot.width()
        canvas_height = drawBot.height()

        if version >= "3.0":
            glyph_width = g.bounds[2] - g.bounds[0]
            glyph_height = g.bounds[3] - g.bounds[1]
        else:
            glyph_width = g.box[2] - g.box[0]
            glyph_height = g.box[3] - g.box[1]

        sw = float(canvas_width - margin * 2) / glyph_width
        sh = float(canvas_height - margin * 2) / glyph_height

        if sw <= sh:
            s = sw
        else:
            s = sh

        # calculate position
        if version >= "3.0":
            x = -g.bounds[0]
            y = -g.bounds[1]
        else:
            x = -g.box[0]
            y = -g.box[1]

        x_shift = (canvas_width - glyph_width * s) * 0.5
        y_shift = (canvas_height - glyph_height * s) * 0.5

        # make preview
        drawBot.save()
        drawBot.translate(x_shift, y_shift)
        drawBot.scale(s)
        drawBot.translate(x, y)

        # draw components
        sub = set()
        for c in g.components:
            if self.selected_component and self.selected_alternate and c.baseGlyph == self.selected_component:
                sub_txt = u'%s → %s' % (c.baseGlyph, self.selected_alternate)
                sub.add(sub_txt)
                # get alternate
                component_glyph = f[self.selected_alternate]
                # set color
                if show_colors:
                    drawBot.fill(*self.color_alternates)
            else:
                # get component
                component_glyph = f[c.baseGlyph]
                # set color
                if show_colors:
                    drawBot.fill(*self.color_components)
            drawBot.save()
            drawBot.translate(*c.offset)
            drawBot.drawGlyph(component_glyph)
            drawBot.restore()

        # draw outlines
        outlines = RGlyph()
        for c in g.contours:
            outlines.appendContour(c)
        if show_colors:
            drawBot.fill(*self.color_contours)
        drawBot.drawGlyph(outlines)

        # draw caption
        drawBot.restore()
        x, y = 10, drawBot.height() - 20
        n = 2
        txt = drawBot.FormattedString()
        txt.font("Menlo-Bold")
        txt.fontSize(13)
        if show_colors:
            txt.append(u'contours', fill=(0, 0, 1))
            txt.append(u' '*n)
            txt.append(u'components', fill=(0, 1, 0))
            txt.append(u' '*n)
            txt.append(u'alternate', fill=(1, 0, 0))
            txt.append(u' '*n)
        for s in sub:
            txt.append(s + u' '*n)
        drawBot.text(txt, (x, y))

        # update glyph view
        pdf_data = drawBot.pdfImage()
        self.w.canvas.setPDFDocument(pdf_data)
