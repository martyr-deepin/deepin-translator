import QtQuick 2.1

MouseArea {
    id: mouseArea
    anchors.fill: parent
    hoverEnabled: true
    
    property variant target: null
	
    onEntered: {
        target.state = "hovered"
        mouseArea.cursorShape = Qt.PointingHandCursor
    }
    
    onExited: {
        target.state = ""
        mouseArea.cursorShape = Qt.ArrowCursor
    }
    
    onReleased: { 
        target.state = mouseArea.containsMouse ? "hovered" : ""
    }
}