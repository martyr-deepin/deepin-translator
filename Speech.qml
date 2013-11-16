import QtQuick 2.1

Row {
    id: speech
	property alias text: display.text
	property alias display: display
	property alias speaker: speaker
	visible: display.text
	spacing: 6
    
    function getWidth() {
        return display.paintedWidth + speaker.width + spacing * 2
    }
    
    function getHeight() {
        return Math.max(display.paintedHeight, speaker.height)
    }
		
	Text { 
		id: display
        anchors.verticalCenter: parent.verticalCenter 
		font { pixelSize: 15 }
		color: "#636363"
	}
	
	Image {
		id: speaker
		source: "speaker.png"
		anchors.verticalCenter: parent.verticalCenter 
        
		states: State {
			name: "hovered"
			PropertyChanges { target: speaker; opacity: 0.5 }
		}
		
		transitions: Transition {
			NumberAnimation { properties: "opacity"; duration: 350 }
		}
		
		MouseArea {
			id: mouseArea
			anchors.fill: speaker
            hoverEnabled: true
            
			onEntered: {
                speaker.state = "hovered"
                mouseArea.cursorShape = Qt.PointingHandCursor
            }
            
			onExited: {
                speaker.state = ""
                mouseArea.cursorShape = Qt.ArrowCursor
            }
            
			onReleased: { 
                speaker.state = mouseArea.containsMouse ? "hovered" : ""
            }
		}
	}
}
