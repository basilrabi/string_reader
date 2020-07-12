#/***************************************************************************
# StringReader
#
# Reads string files
#							 -------------------
#		begin				: 2020-07-11
#		git sha				: $Format:%H$
#		copyright			: (C) 2020 by Basil Eric C. Rabi
#		email				: ericbasil.rabi@gmail.com
# ***************************************************************************/
#
#/***************************************************************************
# *																		    *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or	    *
# *   (at your option) any later version.								    *
# *																		    *
# ***************************************************************************/

PLUGINNAME = string_reader

PY_FILES = \
	__init__.py \
	geom.py \
	string_importer.py \
	string_reader.py \
	string_reader_dialog.py

UI_FILES = string_reader_dialog_base.ui

EXTRAS = metadata.txt icon.png

COMPILED_RESOURCE_FILES = resources.py

PEP8EXCLUDE=pydev,resources.py,conf.py,third_party,ui

PLUGINDIR=$(HOME)/.local/share/QGIS/QGIS3/profiles/default/python/plugins/$(PLUGINNAME)

RESOURCE_SRC=$(shell grep '^ *<file' resources.qrc | sed 's@</file>@@g;s/.*>//g' | tr '\n' ' ')

.PHONY: default
default:
	@echo "String File Reader for QGIS"

compile: $(COMPILED_RESOURCE_FILES)

%.py : %.qrc $(RESOURCES_SRC)
	pyrcc5 -o $*.py  $<

deploy: compile
	@echo "Installing plugin..."
	mkdir -p $(PLUGINDIR)
	cp -vf $(PY_FILES) $(PLUGINDIR)/
	cp -vf $(UI_FILES) $(PLUGINDIR)/
	cp -vf $(COMPILED_RESOURCE_FILES) $(PLUGINDIR)/
	cp -vf $(EXTRAS) $(PLUGINDIR)/

dclean:
	find $(PLUGINDIR) -iname "*.pyc" -delete
	find $(PLUGINDIR) -iname ".git" -prune -exec rm -Rf {} \;

derase:
	rm -Rf $(PLUGINDIR)

zip: deploy dclean
	rm -f $(PLUGINNAME).zip
	cd $(PLUGINDIR); cd ..; zip -9r $(CURDIR)/$(PLUGINNAME).zip $(PLUGINNAME)

package: compile
	rm -f $(PLUGINNAME).zip
	git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION)
	echo "Created package: $(PLUGINNAME).zip"

clean:
	rm $(COMPILED_RESOURCE_FILES)
