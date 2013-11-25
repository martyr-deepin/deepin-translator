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
	
	property int mouseX: 0
	property int mouseY: 0
	
	function adjustPosition() {
		var x = mouseX + windowOffsetX
		if (x < 0) {
			x = windowPadding
		} else if (x + windowView.width > Screen.width) {
			x = Screen.width - windowView.width - windowPadding
		}
		windowView.x = x
		cornerPos = mouseX - x
		
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
}
