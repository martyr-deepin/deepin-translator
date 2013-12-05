import QtQuick 2.1
import QtQuick.Window 2.1
import QtGraphicalEffects 1.0

RectWithCorner {
    radius: 6
    cornerDirection: "up"
    
    property int borderMargin: 10
    property int textMargin: 10
    
	property int windowPadding: 10
	property int windowOffsetX: -50
	property int windowOffsetY: 5
	
	property int mouseX: 0
	property int mouseY: 0
    
    property alias textWin: textWin
	
    Window {
        id: textWin
	    flags: Qt.Popup | Qt.FramelessWindowHint
	    color: "transparent"
        visible: false
        width: textContent.paintedWidth + (padding + margin) * 2
        height: textContent.paintedHeight + (padding + margin) * 2
        
        property int margin: 10
        property int padding: 5
        property alias textContent: textContent
        property alias rect: rect
        
        property int mouseX: 0
        property int mouseY: 0
        
        Rectangle {
            id: rect
            anchors.fill: parent
            radius: 6
            anchors.margins: textWin.margin
		    gradient: Gradient {
			    GradientStop { position: 0.0; color: "#F5ED00"}
			    GradientStop { position: 1.0; color: "#E9CD00"}
		    }
		    visible: parent.visible
	    }
        
        Text {
            id: textContent
            anchors.centerIn: parent
			font { pixelSize: 18 }
        }        
    }
    
    function showTextWin(x, y, text) {
        textWin.visible = true
        textWin.textContent.visible = false
        textWin.textContent.text = text
        textWin.x = x - textWin.width / 2
        textWin.y = y - textWin.height / 2
        textWin.mouseX = x
        textWin.mouseY = y
        
        textWin.rect.scale = 0.5
        showingTextWinAnimation.restart()
    }
    
	function adjustPosition() {
        var x = 0
        var pos = 0
        if (mouseX - windowView.width / 2 < 0) {
            x = windowPadding
            pos = mouseX - x
        } else if (mouseX + windowView.width / 2 > Screen.width) {
            x = Screen.width - windowView.width - windowPadding
            pos = mouseX - x
        } else {
            x = mouseX - windowView.width / 2
            pos = windowView.width / 2
        }
        cornerPos = pos
        windowView.x = x
		
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
    
    ParallelAnimation {
        id: showingTextWinAnimation
        
        PropertyAnimation {
            target: textWin.rect
            property: "scale"
            from: 0.5
            to: 1
            duration: 500
            easing.type: Easing.OutBack
        }
        
        onRunningChanged: {
            textWin.textContent.visible = true
            /* showTranslate(textWin.mouseX, textWin.mouseY, textWin.textContent.text) */
        }
    }    
}
