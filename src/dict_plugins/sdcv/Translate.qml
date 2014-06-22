import QtQuick 2.1
import QtQuick.Window 2.1
import Deepin.Locale 1.0
import Deepin.Widgets 1.0
import QtMultimedia 5.0
import "../../../src"

TranslateWindow {
	id: container
    
    property int scrollHeight: 200
    property int scrollWidth: 400
    property alias toolbar: toolbar
    property alias trans: trans
    
	property bool isManualStop: false
    
    property variant dsslocale: DLocale {
        id: dsslocale
        dirname: "../../../locale"
        domain: "deepin-translator"
    }
    
    function dsTr(s){
        return dsslocale.dsTr(s)
    }
    
    function showTranslate(x, y, text) {
		mouseX = x
		mouseY = y
		
		/* Move window out of screen before adjust position */
		windowView.x = 100000
		windowView.y = 100000
		windowView.showNormal()
		windowView.get_translate(text)
		
		adjustTranslateSize()
        speechPlayer.autoplayAudio()
        
        toolbar.init(false)
    }
	
    function adjustTranslateSize() {
        var maxWidth = Math.max(Math.min(trans.paintedWidth, scrollWidth) + (borderMargin + container.blurRadius) * 2, minWindowWidth)
        var maxHeight = Math.min(trans.paintedHeight + container.cornerHeight + (borderMargin + textMargin + container.blurRadius) * 2, scrollHeight)
        
        windowView.width = maxWidth
        windowView.height = maxHeight
        
        container.rectWidth = maxWidth
        container.rectHeight = maxHeight
        container.width = maxWidth
        container.height = maxHeight
		
        adjustPosition()
    }    
    
	Connections {
		target: windowView
		onVisibleChanged: {
			if (!arg) {
                speechPlayer.stopAudio()
			}
		}
        
        onHided: {
            toolbar.resetCursor()
            container.resetCorner()
        }
	}
    
    Player {
        id: speechPlayer
        voices: translateInfo.voices
    }
	
	Rectangle {
        id: border
        radius: 6
	    anchors.fill: parent
        anchors.topMargin: cornerDirection == "up" ? borderMargin + container.cornerHeight : borderMargin
		anchors.bottomMargin: borderMargin
		anchors.leftMargin: borderMargin
		anchors.rightMargin: borderMargin
        color: Qt.rgba(0, 0, 0, 0)
        
	    Column {
		    spacing: 10
		    anchors.fill: parent
		    anchors.margins: textMargin
		    
            Toolbar {
                id: toolbar
                width: parent.width
                text: translateInfo.text
                phonetic: translateInfo.phonetic
                player: speechPlayer
                window: windowView
            }
            
	        Rectangle {
		        width: parent.width
                height: parent.height
		        anchors.margins: textMargin
                color: "transparent"
                
                Flickable {
                    id: flick

                    width: parent.width; 
                    height: parent.height;
                    contentWidth: trans.paintedWidth
                    contentHeight: trans.paintedHeight
                    clip: true

                    function ensureVisible(r)
                    {
                        if (contentX >= r.x)
                        contentX = r.x;
                        else if (contentX+width <= r.x+r.width)
                        contentX = r.x+r.width-width;
                        if (contentY >= r.y)
                        contentY = r.y;
                        else if (contentY+height <= r.y+r.height)
                        contentY = r.y+r.height-height;
                    }

		            TextEdit {
                        id: trans
			            text: translateInfo.translate
			            wrapMode: TextEdit.WordWrap
			            selectByMouse: true
			            font { pixelSize: 14 }
			            color: "#FFFFFF"
				        selectionColor: "#11ffffff"
				        selectedTextColor: "#5da6ce"
                        width: scrollWidth
                        readOnly: true
		            }
                }
                
                DScrollBar {
                    flickable: flick
                }
            }
	    }        
	}
}
