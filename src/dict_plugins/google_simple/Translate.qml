import QtQuick 2.1
import QtQuick.Window 2.1
import Deepin.Locale 1.0
import QtMultimedia 5.0
import "../../../src"

TranslateWindow {
	id: container
    
    property alias toolbar: toolbar
    
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
		var maxWidth = Math.max(trans.paintedWidth + (borderMargin + container.blurRadius) * 2, minWindowWidth)
        var maxHeight = trans.paintedHeight + toolbar.height + cornerHeight + (borderMargin + container.blurRadius) * 2 
        
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
            
		    TextEdit { 
                id: trans
			    text: translateInfo.translate
			    wrapMode: TextEdit.WordWrap
			    selectByMouse: true
			    font { pixelSize: 12 }
			    color: "#FFFFFF"
				selectionColor: "#11ffffff"
				selectedTextColor: "#5da6ce"
                width: parent.width
                readOnly: true
		    }		
	    }        
	}
}
