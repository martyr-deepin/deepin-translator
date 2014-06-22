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
	signal pressUp
	signal pressDown
    
    function activeFocus() {
        cursorWidth = 2
        textInput.forceActiveFocus()
    }
    
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
			    selectByMouse: true
		        font { pixelSize: 18 }
                
                property int blinkCounter: 0
                property int blinkTimes: 10
                
                cursorDelegate: Rectangle {
                    id: textCursor
                    width: cursorWidth
                    color: "#AAFFFFFF"
                    
                    SequentialAnimation on opacity  {
                        id: cursorBlinkAnimation
                        
                        PropertyAnimation {
                            from: 1
                            to: 1
                            duration: 200
                        }
                        
                        PauseAnimation { 
                            duration: 600
                        }

                        PropertyAnimation {
                            id: endAnimation
                            from: textInput.blinkCounter <= textInput.blinkTimes ? 0 : 1
                            to: textInput.blinkCounter <= textInput.blinkTimes ? 0 : 1
                            duration: 200
                        }
                        
                        onRunningChanged: {
                            if (!cursorBlinkAnimation.running) {
                                textInput.blinkCounter += 1
                                restart()
                            }
                        }
                    }                    
			    }
                
                onAccepted: {
                    entry.accepted(text)
                }
                
                onTextChanged: {
                    if (activeFocus) {
                        entry.inputChanged()
                    }
                }
                
				Keys.onPressed: {
					if (event.key == Qt.Key_Up) {
						entry.pressUp()
					} else if (event.key == Qt.Key_Down) {
						entry.pressDown()
					}
                    
                    textInput.blinkCounter = textInput.blinkTimes + 1
                    resetCursorBlinkTimer.stop()
				}
                
                Keys.onReleased: {
                    resetCursorBlinkTimer.restart()
                }

	            Timer {
		            id: resetCursorBlinkTimer
		            interval: 300
		            repeat: false
		            
		            onTriggered: {
                        textInput.blinkCounter = 0
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
            source: "image/enter.png"
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
