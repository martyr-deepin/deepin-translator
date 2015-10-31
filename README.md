# Deepin Translator

Feature-rich dictionary lookup program from Deepin

## Features

* Support of multiple dictionary file formats and online dictionary services, namely:
    * StarDict .ifo/.dict./.idx/.syn dictionaries
    * Google online dictionary services
    * Youdao online dictionary services
    * etc.
 * HyperTranslate functionality. A small window pops up with the translation of a word selected from another application.
 * Use of QML for interface, more modern, more gorgeours
 * Include OCR function

## Known issues

This is a working in progress project, and the initial goal is to check the OCR usability under Linux, so you may encounter variety kinds of issues.

## Dependencies

* [deepin-menu](https://github.com/linuxdeepin/deepin-menu)
* python-tesseract
* python-pyocr
* tesseract-ocr-eng
* tesseract-ocr-chi-sim
* tesseract-ocr-chi-tra
* python-requests
* python-sip
* python-xpyb
* python-xmltodict
* qt5-extra
* xsel
* [python-deepin-utils](https://github.com/linuxdeepin/deepin-utils)
* python-xlib
* [deepin-qml-widgets](https://github.com/linuxdeepin/deepin-qml-widgets)

## Installation

Deepin:
`sudo apt-get install deepin-translator`

Manual:
Refer to [INSTALL.md](INSTALL.md) for detial.

## Usage
Double click to translate word around cursor, or select text to pop translate window.
You can use Alt + Mouse to translate word that can't selection, such as, text in image or pdf.

## Getting help

Any usage issues can ask for help via

* [Gitter](https://gitter.im/orgs/linuxdeepin/rooms)
* [IRC channel](https://webchat.freenode.net/?channels=deepin)
* [Forum](https://bbs.deepin.org)
* [WiKi](http://wiki.deepin.org/)

## Getting involved

We encourage you to report issues and contribute changes

* [Contribution guide for users](http://wiki.deepin.org/index.php?title=Contribution_Guidelines_for_Users)
* [Contribution guide for developers](http://wiki.deepin.org/index.php?title=Contribution_Guidelines_for_Developers).

## License

Deepin Translator is licensed under [GPLv3](LICENSE).
