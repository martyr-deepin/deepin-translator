PREFIX = /usr/local

all:
	cd tools; ./generate_mo.py; cd ..

install:
	mkdir -p ${DESTDIR}${PREFIX}/bin
	mkdir -p ${DESTDIR}${PREFIX}/share/applications
	mkdir -p ${DESTDIR}${PREFIX}/share/deepin-translator
	mkdir -p ${DESTDIR}${PREFIX}/share/icons
	cp -r src ${DESTDIR}${PREFIX}/share/deepin-translator
	cp -r locale/mo ${DESTDIR}${PREFIX}/share/locale
	cp -r image/hicolor ${DESTDIR}${PREFIX}/share/icons
	cp src/deepin-translator.desktop ${DESTDIR}${PREFIX}/share/applications
	ln -sf ${PREFIX}/share/deepin-translator/src/main.py ${DESTDIR}${PREFIX}/bin/deepin-translator
