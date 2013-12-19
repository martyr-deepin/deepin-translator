import QtQuick 2.1
import QtQuick.Window 2.1

RectWithCorner {
    radius: 6
    cornerDirection: "up"
    
    property int borderMargin: 10
    property int textMargin: 10
    
	property int windowPadding: 10
	property int windowOffsetX: -50
	property int windowOffsetY: 5
    property int minWindowWidth: 300
	
	property int mouseX: 0
	property int mouseY: 0
	
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
        windowView.x = x + windowView.width / 2
		
		var y = mouseY + windowOffsetY
		var direction = "up"
		if (y < 0) {
			y = windowPadding
		} else if (y + windowView.height > Screen.height) {
			y = mouseY - windowView.height - windowOffsetY
			direction = "down"
		}
		windowView.y = y + windowView.height / 2
		cornerDirection = direction
	}
}
