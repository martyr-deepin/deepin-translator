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
        border {
            width: 1
            color: Qt.rgba(0, 0, 0, 0.5)
        }
        radius: 3

        Rectangle {
            id: textInputArea
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: actionButton.left
            anchors.leftMargin: 10
            anchors.rightMargin: 10
            anchors.topMargin: 5
            anchors.bottomMargin: anchors.topMargin
            clip: true          /* clip to avoid TextInput out of area */
            
            TextInput {
                id: textInput
                anchors.fill: parent
                
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
            
            MouseArea {
                anchors.fill: parent
                
                onClicked: {
                    entry.accepted(textInput.text)
                }
            }
        }
    }
}
