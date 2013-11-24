import QtQuick 2.1
import QtQuick.Window 2.1
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
    
	property int windowPadding: 10
	property int windowOffsetX: -50
	property int windowOffsetY: 5
	
	property int mouseX: 0
	property int mouseY: 0
	
    width: 300
    height: 200
    
    function showTranslate(x, y, text) {
		mouseX = x
		mouseY = y
		
		/* Move window out of screen before adjust position */
		windowView.x = 100000
		windowView.y = 100000
		windowView.showNormal()
		windowView.get_translate(text)
		
		adjustTranslateSize()
    }
	
	function adjustPosition() {
		var x = mouseX + windowOffsetX
		if (x < 0) {
			x = windowPadding
		} else if (x + windowView.width > Screen.width) {
			x = Screen.width - windowView.width - windowPadding
		}
		windowView.x = x
		cornerPos = mouseX - x
		
		var y = mouseY + windowOffsetY
		var direction = "up"
		if (y < 0) {
			y = windowPadding
		} else if (y + windowView.height > Screen.height) {
			y = mouseY - windowView.height - windowOffsetY
			direction = "down"
		}
		windowView.y = y
		cornerDirection = direction
	}
	
    function adjustTranslateSize() {
		var maxWidth = trans.paintedWidth + (borderMargin + textMargin + container.blurRadius) * 2
        var maxHeight = trans.paintedHeight + voice.height + container.cornerHeight + (borderMargin + textMargin + container.blurRadius) * 2 
        
        windowView.width = maxWidth
        windowView.height = maxHeight
        
        container.rectWidth = maxWidth
        container.rectHeight = maxHeight
        container.width = maxWidth
        container.height = maxHeight
		
		adjustPosition()
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
	    }        
	}
}
