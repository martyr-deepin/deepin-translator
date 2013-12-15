import QtQuick 2.1
import QtQuick.Window 2.1
import Deepin.Locale 1.0
import QtMultimedia 5.0
import "../../../src"

TranslateWindow {
	id: container
    
    property int scrollHeight: 200
    property int scrollWidth: 355
    
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
    }
	
    function adjustTranslateSize() {
        var maxWidth = Math.max(trans.paintedWidth, scrollWidth) + (borderMargin + textMargin + container.blurRadius) * 2
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
		    
			Speech { 
                id: voice
				text: dsTr("Read")
                
				onClicked: {
                    speechPlayer.playAudio()
				}
            }
            
	        ScrollWidget {
		        width: parent.width
                height: parent.height - voice.height
		        anchors.margins: textMargin
		        
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
                    
                    onTextChanged: {
                        cursorPosition: 0
                        cursorVislble: false
                    }
		        }		
            }
	    }        
	}
}
