import QtQuick 2.1

Item {
    id: entry
    width: parent.width
    height: 20
    
    property alias text: textInput.text
    property alias textInput: textInput
	property int cursorWidth: 2

    signal accepted (string text)
    signal inputChanged
    
    Rectangle {
        id: entryBorder
        anchors.fill: parent
        color: Qt.rgba(0, 0, 0, 0)

        Rectangle {
            anchors.left: parent.left
            anchors.right: actionButton.left
            anchors.rightMargin: 5
            height: parent.height
            color: Qt.rgba(0, 0, 0, 0)
            clip: true
            
            TextInput {
                id: textInput
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.rightMargin: 2
                color: "#f7d303"
                selectionColor: "#11ffffff"
                selectedTextColor: "#5da6ce"
		        font { pixelSize: 18 }
                cursorDelegate: Rectangle {
                    width: cursorWidth
                    color: "#AAFFFFFF"
			    }
                
                onAccepted: {
                    entry.accepted(text)
                }
                
                onTextChanged: {
                    if (activeFocus) {
                        entry.inputChanged()
                    }
                }
                
                MouseArea {
                    anchors.fill: parent
                    propagateComposedEvents: true
                    
                    onPressed: {
                        mouse.accepted = false
						
						cursorWidth = 2
                    }
                }
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
