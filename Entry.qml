import QtQuick 2.1

Item {
    id: entry
    width: parent.width
    height: 30
    
    property alias text: textInput.text
    property alias textInput: textInput

    signal accepted (string text)
    
    Rectangle {
        id: entryBorder
        anchors.fill: parent
        color: Qt.rgba(0, 0, 0, 0)

        Rectangle {
            id: textInputArea
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: actionButton.left
            anchors.leftMargin: 0
            anchors.rightMargin: 10
            anchors.topMargin: 5
            anchors.bottomMargin: anchors.topMargin
            clip: true          /* clip to avoid TextInput out of area */
            color: Qt.rgba(0, 0, 0, 0)
            
            TextInput {
                id: textInput
                anchors.fill: parent
                color: "#f7d303"
		        font { pixelSize: 18 }
                
                onAccepted: {
                    entry.accepted(text)
                }
            }
        }
        
        Image {
            id: actionButton
            source: "image/search.png"
            width: 16
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: entryBorder.right
            anchors.rightMargin: 10
            opacity: 0.5
            
		    states: State {
			    name: "hovered"
			    PropertyChanges { target: actionButton; opacity: 1.0 }
		    }
		    
		    transitions: Transition {
			    NumberAnimation { properties: "opacity"; duration: 350 }
		    }
		    
		    MouseArea {
			    id: mouseArea
			    anchors.fill: actionButton
                hoverEnabled: true
			    
			    onEntered: {
                    actionButton.state = "hovered"
                    mouseArea.cursorShape = Qt.PointingHandCursor
                }
                
			    onExited: {
                    actionButton.state = ""
                    mouseArea.cursorShape = Qt.ArrowCursor
                }
                
			    onReleased: { 
                    actionButton.state = mouseArea.containsMouse ? "hovered" : ""
                }
                onClicked: {
                    entry.accepted(textInput.text)
                }
		    }
        }
    }
}
