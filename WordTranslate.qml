import QtQuick 2.1
import QtMultimedia 5.0

Rectangle {
	id: container
    radius: 6
    color: "#AA000000"
	border { 
        width: 1
        color: "#AAFFFFFF"
    }
    
    property alias keyword: keyword
    property alias trans: trans
    property alias webtrans: webtrans
    property int borderMarin: 10
    property int textMargin: 10
    
    function showTranslate() {
        adjustWidth()
        autoSpeech()
    }
    
    function adjustWidth() {
        var maxWidth = Math.max(
            keyword.height,
            trans.paintedWidth, 
            webtrans.paintedWidth, 
            usSpeech.getWidth() + ukSpeech.getWidth()
        ) + (borderMarin + textMargin) * 2
        windowView.width = maxWidth
        
        windowView.height = keyword.height + trans.paintedHeight + webtrans.paintedHeight + ukSpeech.getHeight() + (borderMarin + textMargin) * 2
    }    
    
    function autoSpeech() {
        var speechlink = simpleinfo.uslink ? simpleinfo.uslink : simpleinfo.uklink
        if (speechlink) {
		    audioPlayer.source = speechlink
            audioPlayer.play()
        }
    }
	
    Audio {
        id: audioPlayer
    }
    
	Rectangle {
        id: border
        radius: 6
	    anchors.fill: parent
		anchors.margins: borderMarin
        color: "#EEFFFFFF"
        
	    Column {
		    spacing: 10
		    anchors.fill: parent
		    anchors.margins: textMargin
		    
            Entry {
                id: keyword
                objectName: "textInput"
                text: simpleinfo.keyword
            }
		    
		    Row {
                id: speech
			    spacing: 10
			    
			    Speech { 
                    id: usSpeech
                    text: simpleinfo.usphone
                    
					onClicked: {
						audioPlayer.source = simpleinfo.uslink
						audioPlayer.play()
					}
                }			
                
			    Speech { 
                    id: ukSpeech
                    text: simpleinfo.ukphone 
					onClicked: {
						audioPlayer.source = simpleinfo.uklink
						audioPlayer.play()
					}
                }
		    }
		    
		    TextEdit { 
                id: trans
			    text: simpleinfo.trans
                textFormat: TextEdit.RichText
			    wrapMode: TextEdit.Wrap
			    selectByMouse: true
			    font { pixelSize: 12 }
			    color: "#333333"
                
                onTextChanged: {
                    cursorPosition: 0
                    cursorVislble: false
                }
		    }		
		    
		    TextEdit {
                id: webtrans
			    text: simpleinfo.webtrans
                textFormat: TextEdit.RichText
			    wrapMode: TextEdit.Wrap
			    selectByMouse: true
			    font { pixelSize: 12 }
			    color: "#333333"

                onTextChanged: {
                    cursorPosition: 0
                    cursorVislble: false
                }
		    }
	    }        
	}
}
