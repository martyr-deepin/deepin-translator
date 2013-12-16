import QtQuick 2.1
import "../widgets"

WindowFrame {
    id: window
    
    property int defaultWidth: 300
    property int defaultHeight: 140
    property int paddingX: 30
    property int paddingY: 60
    
    property alias messageText: messageText
    property alias cancelText: cancelText
    property alias confirmText: confirmText
    
    function showMessage(message, cancel, confirm) {
        messageText.text = message
        cancelText.text = cancel
        confirmText.text = confirm
        
        windowView.width = Math.max(defaultWidth, messageText.paintedWidth + paddingX * 2)
        windowView.height = Math.max(defaultHeight, messageText.paintedHeight + paddingY * 2)
        windowView.x = (screenWidth - defaultWidth) / 2
        windowView.y = (screenHeight - defaultHeight) / 2
        
        windowView.showNormal()
    }
    
    CloseButton {
        onClicked: {
            windowView.hide()
        }
    }
        
    DragArea {
        anchors.fill: parent
        window: windowView
        propagateComposedEvents: true
        
        onPositionChanged: {
            mouse.accepted = false
        }
        
        onClicked: {
            mouse.accepted = false
        }
    }
    
    Text {
        id: messageText
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        height: 100
        width: parent.width
        color: "#fff"
    }
    
    Row {
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
        anchors.rightMargin: 10
        
        DTextButton {
            id: cancelText
            
            onClicked: {
                windowView.hide()
            }
        }

        DTextButton {
            id: confirmText
            textColor: "#fbfbfb"
            
            onClicked: {
                windowView.hide()
                windowView.execute_action()
            }
        }
        
    }
}
