import QtQuick 2.0;

Item {
    id: scrollbar
    width: handleSize
    visible: (flickable.visibleArea.heightRatio < 1.0)
    anchors {
        top: flickable.top
        right: flickable.right
        bottom: flickable.bottom
        margins: 1
    }

    property Flickable flickable : null
    property int handleSize: 12
    property alias backHandle: backHandle
    property color inactiveColor: Qt.rgba(0, 0, 0, 0.5)
    property color activeColor: Qt.rgba(0, 0, 0, 0.9)
    property bool inInteractive: false

    function scrollDown () {
        flickable.contentY = Math.min (flickable.contentY + (flickable.height / 4), flickable.contentHeight - flickable.height)
    }
    function scrollUp () {
        flickable.contentY = Math.max (flickable.contentY - (flickable.height / 4), 0)
    }

    Binding {
        target: handle
        property: "y"
        value: (flickable.contentY * clicker.drag.maximumY / (flickable.contentHeight - flickable.height))
        when: (!clicker.drag.active)
    }
    
    Binding {
        target: flickable
        property: "contentY"
        value: (handle.y * (flickable.contentHeight - flickable.height) / clicker.drag.maximumY)
        when: (clicker.drag.active || clicker.pressed)
    }
    
    Item {
        id: groove
        clip: true
        anchors {
            fill: parent
            margins: 1
        }

        MouseArea {
            id: clicker
            anchors.fill: parent
            hoverEnabled: true
            
            drag {
                target: handle
                minimumY: 0
                maximumY: (groove.height - handle.height)
                axis: Drag.YAxis
            }
            
            onClicked: { 
                flickable.contentY = (mouse.y / groove.height * (flickable.contentHeight - flickable.height)) 
            }
            
            onEntered: {
                backHandle.opacity = 0.7
                backHandle.color = inactiveColor
                
                scrollbar.inInteractive = true
            }
            
            onExited: {
                scrollbar.inInteractive = false
                hideTimer.restart()
            }
        }
        
        Item {
            id: handle
            height: Math.max(50, (flickable.visibleArea.heightRatio * groove.height))
            anchors {
                left: parent.left
                right: parent.right
            }

            Rectangle {
                id: backHandle
                color: scrollbar.inactiveColor
                anchors { fill: parent }
                border.color: "#44ffffff"
                border.width: 1
                radius: 6
                opacity: 0

                Behavior on opacity { NumberAnimation { duration: 150 } }
            }
            
            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
        
                onEntered: {
                    backHandle.opacity = 0.7
                    backHandle.color = activeColor

                    scrollbar.inInteractive = true
                }
                
                onExited: {
                    backHandle.color = inactiveColor

                    scrollbar.inInteractive = false
                    hideTimer.restart()
                }
            }
        }
    }

    Timer {
        id: hideTimer
        interval: 150
        repeat: false
        onTriggered: {
            if (!scrollbar.inInteractive) {
                backHandle.opacity = 0
            }
        }
    }
}
