PREFIX = /usr/local

all:
	cd tools; ./generate_mo.py; cd ..
	pycompile src

install:
	mkdir -p ${DESTDIR}${PREFIX}/bin
	mkdir -p ${DESTDIR}${PREFIX}/share/applications
	mkdir -p ${DESTDIR}${PREFIX}/share/deepin-translator
	mkdir -p ${DESTDIR}${PREFIX}/share/icons/hicolor/scalable/apps
	cp -r src ${DESTDIR}${PREFIX}/share/deepin-translator
	cp -r locale ${DESTDIR}${PREFIX}/share/deepin-translator
	cp src/deepin-translator.svg ${DESTDIR}${PREFIX}/share/icons/hicolor/scalable/apps
	cp src/deepin-translator.desktop ${DESTDIR}${PREFIX}/share/applications
	ln -sf ${PREFIX}/share/deepin-translator/src/main.py ${DESTDIR}${PREFIX}/bin/deepin-translator
