import QtQuick 2.1
import QtGraphicalEffects 1.0

Rectangle {
	width: parent.width
	height: itemHighlightHeight
	color: Qt.rgba(0, 0, 0, 0)
	visible: false
	
    RadialGradient {
        anchors.fill: parent
        horizontalRadius: parent.width * 1.54
        horizontalOffset: 0
        verticalRadius: parent.height * 3
        verticalOffset: -70
		visible: parent.visible
        
        gradient: Gradient {
            GradientStop { position: 0.0; color: Qt.rgba(255 / 255.0, 243 / 255.0, 77 / 255.0, 0.5)}
            GradientStop { position: 1.0; color: Qt.rgba(255 / 255, 192 / 255, 0 / 255, 0.02)}
        }
        
    }
	LinearGradient {
		width: parent.width
		height: 1
		anchors.top: parent.top
		start: Qt.point(0, 0)
		end: Qt.point(width, 0)
		gradient: Gradient {
			GradientStop { position: 0.0; color: Qt.rgba(255 / 255.0, 192 / 255.0, 0 / 255.0, 0.05)}
			GradientStop { position: 0.5; color: Qt.rgba(255 / 255.0, 243 / 255.0, 77 / 255.0, 0.45)}
			GradientStop { position: 1.0; color: Qt.rgba(255 / 255.0, 192 / 255.0, 0 / 255.0, 0.05)}
		}
		visible: parent.visible
	}

	LinearGradient {
		width: parent.width
		height: 1
		anchors.bottom: parent.bottom
		start: Qt.point(0, 0)
		end: Qt.point(width, 0)
		gradient: Gradient {
			GradientStop { position: 0.0; color: Qt.rgba(255 / 255.0, 192 / 255.0, 0 / 255.0, 0.05)}
			GradientStop { position: 0.5; color: Qt.rgba(255 / 255.0, 243 / 255.0, 77 / 255.0, 0.15)}
			GradientStop { position: 1.0; color: Qt.rgba(255 / 255.0, 192 / 255.0, 0 / 255.0, 0.05)}
		}
		visible: parent.visible
	}
	
    Behavior on y {
        NumberAnimation {
            duration: 200
            easing.type: Easing.OutQuint
        }
    }
}
