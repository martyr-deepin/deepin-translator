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
    
    function adjustWidth() {
        var maxWidth = Math.max(
            keyword.paintedWidth,
            trans.paintedWidth, 
            webtrans.paintedWidth, 
            usSpeech.getWidth() + ukSpeech.getWidth()
        ) + (borderMarin + textMargin) * 2
        windowView.width = maxWidth
        
        windowView.height = keyword.paintedHeight + trans.paintedHeight + webtrans.paintedHeight + ukSpeech.getHeight() + (borderMarin + textMargin) * 2
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
		    
		    Text { 
			    id: keyword
			    text: simpleinfo.keyword
                textFormat: TextEdit.RichText
			    font { 
                    pixelSize: 18
                    bold: true
                }
			    color: "#000000"
		    }
		    
		    Row {
                id: speech
			    spacing: 10
			    
			    Speech { 
                    id: ukSpeech
                    text: simpleinfo.ukphone 
					onClicked: {
						audioPlayer.source = simpleinfo.uklink
						audioPlayer.play()
					}
                }
                
			    Speech { 
                    id: usSpeech
                    text: simpleinfo.usphone
					onClicked: {
						audioPlayer.source = simpleinfo.uslink
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
