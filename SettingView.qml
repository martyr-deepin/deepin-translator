import QtQuick 2.1
import QtGraphicalEffects 1.0
import QtQuick.Window 2.1
import QtQuick.Layouts 1.0
import "./widgets"

Item {
    id: window
    
    property int frameRadius: 3
    property int shadowRadius: 10
    property int expandHeight: 240
    property int defaultWidth: 350
    property int defaultHeight: 260
    
    Component.onCompleted: {
        windowView.width = defaultWidth
        windowView.height = defaultHeight
        windowView.x = (screenWidth - windowView.width) / 2
        windowView.y = (screenHeight - windowView.height) / 2
    }
    
    Rectangle {
        id: frame
        anchors.centerIn: parent
        color: "#232323"
        radius: frameRadius
        border.width: 1
        border.color: Qt.rgba(1, 1, 1, 0.3)
        width: window.width - (shadowRadius + frameRadius) * 2
        height: window.height - (shadowRadius + frameRadius) * 2
        
        Item {
            anchors.top: parent.top
            anchors.right: parent.right
            width: closeImage.width
            height: closeImage.height
            
            Rectangle {
                id: closeBackground
                anchors.fill: parent
                anchors.topMargin: 3
                anchors.rightMargin: 3
                anchors.bottomMargin: 1
                anchors.leftMargin: 1
                color: Qt.rgba(0, 0, 0, 0)
            }
            
            Image {
                id: closeImage
                source: "image/window_close.png"
            }
            
            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                
                onEntered: {
                    closeBackground.color = Qt.rgba(1, 1, 1, 0.3)
                }
                
                onExited: {
                    closeBackground.color = Qt.rgba(1, 1, 1, 0)
                }
                
                onClicked: {
                    windowView.hide()
                }
            }
        }
        
        Text {
            id: name
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            height: paintedHeight + 40
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            text: "深度翻译设置"
            color: "#fff"
			font { pixelSize: 20 }
            
            DragArea {
                anchors.fill: parent
                window: windowView
            }
        }
            
        Rectangle {
            anchors.top: name.bottom
            anchors.bottom: button.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 1
            anchors.rightMargin: 1
            color: "transparent"
            clip: true
            
            Column {
                id: content
                anchors.fill: parent
                
                property variant expandId: undefined
                
                onExpandIdChanged: {
                    windowView.height = content.expandId == undefined ? defaultHeight : defaultHeight + expandHeight
                    
                    if (content.expandId != undefined) {
                        for (var i = 0; i < content.children.length; i++) {
                            if (content.children[i] != content.expandId) {
                                content.children[i].expanded = false
                            }
                        }
                    } 
                }
                
                DBaseExpand {
                    id: sourceExpand
	                expanded: false

                    onExpandedChanged: {
                        header.item.checked = expanded
                    }
                    
                    header.sourceComponent: DSwitchButtonHeader {
                        text: "源语言"
                        width: parent.width
                        anchors.left: parent.left
                        anchors.leftMargin: 2
                        anchors.right: parent.right
                        anchors.rightMargin: 2
                        
                        Component.onCompleted: {
                            checked = sourceExpand.expanded
                        }
                        onClicked: {
                            sourceExpand.expanded = checked
                            if (checked) {
                                content.expandId = sourceExpand
                            } else {
                                content.expandId = undefined
                            }
                        }
                    }
                    
                    content.sourceComponent: Rectangle {
                        width: parent.width
                        height: expandHeight
                        color: "#181818"
                    }
                }

                DBaseExpand {
                    id: targetExpand
	                expanded: false

                    onExpandedChanged: {
                        header.item.checked = expanded
                    }
                    
                    header.sourceComponent: DSwitchButtonHeader {
                        text: "目标语言"
                        width: parent.width
                        anchors.left: parent.left
                        anchors.leftMargin: 2
                        anchors.right: parent.right
                        anchors.rightMargin: 2
                        
                        Component.onCompleted: {
                            checked = targetExpand.expanded
                        }
                        onClicked: {
                            targetExpand.expanded = checked
                            if (checked) {
                                content.expandId = targetExpand
                            } else {
                                content.expandId = undefined
                            }
                        }
                    }
                    
                    content.sourceComponent: Rectangle {
                        width: parent.width
                        height: expandHeight
                        color: "#181818"
                    }
                }
                
                DBaseExpand {
                    id: wordExpand
	                expanded: false

                    onExpandedChanged: {
                        header.item.checked = expanded
                    }
                    
                    header.sourceComponent: DSwitchButtonHeader {
                        text: "单词翻译"
                        width: parent.width
                        anchors.left: parent.left
                        anchors.leftMargin: 2
                        anchors.right: parent.right
                        anchors.rightMargin: 2
                        
                        Component.onCompleted: {
                            checked = wordExpand.expanded
                        }
                        onClicked: {
                            wordExpand.expanded = checked
                            if (checked) {
                                content.expandId = wordExpand
                            } else {
                                content.expandId = undefined
                            }
                        }
                    }
                    
                    content.sourceComponent: Rectangle {
                        width: parent.width
                        height: expandHeight
                        color: "#181818"
                    }
                }

                DBaseExpand {
                    id: wordsExpand
	                expanded: false

                    onExpandedChanged: {
                        header.item.checked = expanded
                    }
                    
                    header.sourceComponent: DSwitchButtonHeader {
                        text: "长句翻译"
                        width: parent.width
                        anchors.left: parent.left
                        anchors.leftMargin: 2
                        anchors.right: parent.right
                        anchors.rightMargin: 2

                        Component.onCompleted: {
                            checked = wordsExpand.expanded
                        }

                        onClicked: {
                            wordsExpand.expanded = checked
                            if (checked) {
                                content.expandId = wordsExpand
                            } else {
                                content.expandId = undefined
                            }
                        }
                    }
                    
                    content.sourceComponent: Rectangle {
                        width: parent.width
                        height: expandHeight
                        color: "#181818"
                    }
                }
            }
        }
            
        DTextButton {
            id: button
            text: "确定"
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.margins: 10
            
            onClicked: {
                windowView.hide()
            }
        }
    }
    
    RectangularGlow {
        id: shadow
        anchors.fill: frame
        glowRadius: shadowRadius
        spread: 0.2
        color: Qt.rgba(0, 0, 0, 0.3)
        cornerRadius: frame.radius + shadowRadius
        visible: true
    }
    
    ParallelAnimation{
        id: expandWindowAnimation
        
        PropertyAnimation {
            target: windowView
            property: "height"
            duration: 200
            from: defaultHeight
            to: defaultHeight + expandHeight
            easing.type: Easing.OutQuint
        }
    }    

    ParallelAnimation{
        id: shrinkWindowAnimation
        
        PropertyAnimation {
            target: windowView
            property: "height"
            duration: 200
            from: defaultHeight + expandHeight
            to: defaultHeight
            easing.type: Easing.OutQuint
        }
    }    
}
