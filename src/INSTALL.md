* How to install deepin-translator?

1. Install depend packages in Debian base system:

    > sudo apt-get install python-tesseract python-pyocr tesseract-ocr-eng tesseract-ocr-chi-sim tesseract-ocr-chi-tra python-requests python-xpyb python-xmltodict xsel python-xlib
	
2. Install PyQt5:
    You just need below command to install those package if you use Linux Deepin:
    > sudo apt-get install qt5-extra python-pyqt5  	
	
	If you use other system, you need install pyqt5 with below steps:
	NOTE: We patch qt5 to support fcitx in Linux Deepin, you need handle this issue by yourself. 
    2.1 Install Qt5:
       Download http://download.qt-project.org/official_releases/qt/5.1/5.1.1/qt-linux-opensource-5.1.1-x86_64-offline.run
    
       And then 
       > sudo ./qt-linux-opensource-5.1.1-x86_64-offline.run
       
    2.2. Install Sip:
       Download http://sourceforge.net/projects/pyqt/files/sip/sip-4.15.3/sip-4.15.3.tar.gz
    
       And then
       > tar -xzvf ./sip-4.15.3.tar.gz
       > cd ./sip-4.15.3
       > sudo apt-get install build-essential python-dev   
       > python configure.py
       > make 
       > sudo make install
    
    2.3. Install PyQt5.1.1:
       Download http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.1.1/PyQt-gpl-5.1.1.tar.gz
    
       And then:
       > tar -xzvf ./PyQt-gpl-5.1.1.tar.gz
       > cd ./PyQt-gpl-.5.1.1
       > sudo apt-get install libgl1-mesa-dev libglu1-mesa-dev
       > python configure.py --qmake /opt/Qt5.1.1/5.1.1/gcc_64/bin/qmake 
       > sudo ln -s /usr/include/python2.7 /usr/local/include/python2.7
       > make
       > sudo make install
	
3. Install python-deepin-utils
    > git clone https://github.com/linuxdeepin/deepin-utils    	
	> cd ./deepin-utils && sudo python setup.py install

4. Install deepin-menu:
    > git clone https://github.com/linuxdeepin/deepin-menu
    > cd ./deepin-menu && sudo python setup.py install

5. Then switch deepin-translate to run:
    > cd ./deepin-translator/src && ./main.py 
