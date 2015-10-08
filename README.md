Deepin translator for Deepin
==================================
Feature-rich dictionary lookup program from linux deepin
Features:
 
* Support of multiple dictionary file formats and online dictionary services, namely:
    * StarDict .ifo/.dict./.idx/.syn dictionaries
    * Google online dictionary services
    * Youdao online dictionary services
    * etc.
 * Scan popup functionality. A small window pops up with the translation of a word chosen from another application.
 * Use of QML for interface, more modern, more gorgeours
 * Include OCR function 

## Known issues
The project is a semi-finished products, there are a lot of bugs, but the project to verify the principle of the OCR word from under Linux is feasible.

## Depends
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

## Getting involved

We encourage you to report issues and contribute changes. Please check out the [Contribution Guidelines](http://wiki.deepin.org/index.php?title=Contribution_Guidelines) about how to proceed.

## License

GNU General Public License, Version 3.0
