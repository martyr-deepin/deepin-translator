import QtQuick 2.1

Item {
    id: entry
    width: parent.width
    height: 24
    
    property alias text: textInput.text
    property alias textInput: textInput

    signal accepted (string text)
    signal test
    
    Rectangle {
        id: entryBorder
        anchors.fill: parent
        color: Qt.rgba(0, 0, 0, 0)

        TextInput {
            id: textInput
            anchors.verticalCenter: parent.verticalCenter
            color: "#f7d303"
            selectionColor: "#ffd008"
            selectedTextColor: "#000000"
		    font { pixelSize: 18 }
            
            onAccepted: {
                entry.accepted(text)
            }
            
            onTextChanged: {
                entry.test()
            }
        }
        
        Image {
            id: actionButton
            source: "image/search.png"
            width: 16
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: entryBorder.right
            anchors.rightMargin: 5
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
