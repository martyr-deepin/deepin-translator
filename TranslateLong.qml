import QtQuick 2.1
import QtMultimedia 5.0

RectWithCorner {
	id: container
    radius: 6
    cornerPos: 50
    cornerDirection: "up"
    
    property int borderMargin: 10
    property int textMargin: 10
	property int voiceIndex: 0
	property bool isManualStop: false
    
    width: 300
    height: 200
    
    function showTranslate() {
    }
	
	function manualStopAudio() {
		container.isManualStop = true
		container.voiceIndex = 0
		audioPlayer.stop()
		container.isManualStop = false
	}
	
	Connections {
		target: windowView
		onVisibleChanged: {
			if (!arg) {
				manualStopAudio()
			}
		}
	}
	
	
    Audio {
        id: audioPlayer
		onStopped: {
			if (!container.isManualStop) {
				container.voiceIndex += 1
				if (container.voiceIndex <= translateInfo.voices.length) {
					audioPlayer.source = translateInfo.voices[container.voiceIndex]
					audioPlayer.play()
				} else {
					container.voiceIndex = 0
				}

			}
		}
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
		    
		    TextEdit { 
                id: trans
			    text: translateInfo.translate
                textFormat: TextEdit.RichText
			    wrapMode: TextEdit.Wrap
			    selectByMouse: true
			    font { pixelSize: 12 }
			    color: "#FFFFFF"
                width: parent.width
                
                onTextChanged: {
                    cursorPosition: 0
                    cursorVislble: false
                }
		    }		
			
			Speech { 
                id: voice
				text: "朗读"
				visible: translateInfo.voices.length > 0
                
				onClicked: {
					container.isManualStop = true
					container.voiceIndex = 0
					audioPlayer.stop()
					audioPlayer.source = translateInfo.voices[container.voiceIndex]
					audioPlayer.play()
					container.isManualStop = false
				}
            }			
			
	    }        
	}
}
