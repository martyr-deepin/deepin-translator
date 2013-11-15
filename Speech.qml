import QtQuick 2.1

Row {
		
	property alias text: display.text
	visible: display.text
	spacing: -6
		
	Text { 
		id: display; anchors.verticalCenter: parent.verticalCenter 
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
			onEntered: speaker.state = "hovered"
			onExited: speaker.state = ""
			onReleased: { speaker.state = mouseArea.containsMouse ? "hovered" : ""}
			
		}
	}
}
