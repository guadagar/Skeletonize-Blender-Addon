
INSTALL_DIR = /Applications/Blender-2.79-CellBlender/blender.app/Contents/Resources/2.79/scripts/addons

SHELL = /bin/sh

SOURCES = ./skeletonize_addon/__init__.py ./skeletonize_addon/skel_panel.py ./skeletonize_addon/bin/skeletonize
ZIPFILES = $(SOURCES)

ZIPOPTS = -X -0 -D -o


all: skeletonize_addon skeletonize_addon.zip


skeletonize_addon:
	ln -s . skeletonize_addon


skeletonize_addon.zip: $(SOURCES)
	@echo Updating skeletonize_addon.zip
	@echo Sources = $(SOURCES)
	@zip $(ZIPOPTS) skeletonize_addon.zip $(ZIPFILES)


clean:
	rm -f skeletonize_addon.zip


install: skeletonize_addon.zip
	@ mkdir -p $(INSTALL_DIR)
	@ unzip -o skeletonize_addon.zip -d $(INSTALL_DIR); \
