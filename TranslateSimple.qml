import QtQuick 2.1
import QtMultimedia 5.0

RectWithCorner {
	id: container
    radius: 6
    cornerPos: 50
    cornerDirection: "up"
    
    property alias keyword: keyword
    property alias trans: trans
    property alias webtrans: webtrans
    property int borderMargin: 10
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
        ) + (borderMargin + textMargin + container.blurRadius) * 2
        var maxHeight = keyword.height + trans.paintedHeight + webtrans.paintedHeight + ukSpeech.getHeight() + (borderMargin + textMargin + container.blurRadius + container.cornerHeight) * 2
        
        windowView.width = maxWidth
        windowView.height = maxHeight
        
        container.rectWidth = maxWidth
        container.rectHeight = maxHeight
        container.width = maxWidth
        container.height = maxHeight
    }    
    
    function autoSpeech() {
        var speechlink = translateInfo.uslink ? translateInfo.uslink : translateInfo.uklink
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
        anchors.topMargin: borderMargin + container.cornerHeight
		anchors.bottomMargin: borderMargin
		anchors.leftMargin: borderMargin
		anchors.rightMargin: borderMargin
        color: Qt.rgba(0, 0, 0, 0)
        
	    Column {
		    spacing: 10
		    anchors.fill: parent
		    anchors.margins: textMargin
		    
            Entry {
                id: keyword
                objectName: "textInput"
                text: translateInfo.keyword
            }
		    
		    Row {
                id: speech
			    spacing: 10
			    
			    Speech { 
                    id: usSpeech
                    text: translateInfo.usphone
                    type: "[美]"
                    
					onClicked: {
						audioPlayer.source = translateInfo.uslink
						audioPlayer.play()
					}
                }			
                
			    Speech { 
                    id: ukSpeech
                    text: translateInfo.ukphone 
                    type: "[英]"
					onClicked: {
						audioPlayer.source = translateInfo.uklink
						audioPlayer.play()
					}
                }
		    }
		    
		    TextEdit { 
                id: trans
			    text: translateInfo.trans
                textFormat: TextEdit.RichText
			    wrapMode: TextEdit.Wrap
			    selectByMouse: true
			    font { pixelSize: 12 }
			    color: "#FFFFFF"
                
                onTextChanged: {
                    cursorPosition: 0
                    cursorVislble: false
                }
		    }		
		    
		    TextEdit {
                id: webtrans
			    text: translateInfo.webtrans
                textFormat: TextEdit.RichText
			    wrapMode: TextEdit.Wrap
			    selectByMouse: true
			    font { pixelSize: 12 }
			    color: "#FFFFFF"

                onTextChanged: {
                    cursorPosition: 0
                    cursorVislble: false
                }
		    }
	    }        
	}
}
