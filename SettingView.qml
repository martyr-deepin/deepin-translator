import QtQuick 2.1
import QtGraphicalEffects 1.0
import QtQuick.Window 2.1
import QtQuick.Layouts 1.0
import "./widgets"

Item {
    id: window
    
    property int frameRadius: 3
    property int shadowRadius: 10
    property int defaultWidth: 350
    property int defaultHeight: 245
    property int expandAreaHeight: 113
    property int listHeight: 240
    
    property alias expandArea: expandArea
    
    Component.onCompleted: {
        windowView.width = defaultWidth
        windowView.height = defaultHeight
        windowView.x = (screenWidth - windowView.width) / 2
        windowView.y = (screenHeight - windowView.height) / 2
    }
    
    Connections {
        target: windowView
        onHeightChanged: {
            if (windowView.height == defaultHeight) {
                shrinkAreaAnimation.restart()
            } else {
                expandAreaAnimation.restart()
            }
        }
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
        
        Column {
            anchors.fill: parent
            
            Text {
                id: name
                anchors.left: parent.left
                anchors.right: parent.right
                /* anchors.top: parent.top */
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
                id: expandArea
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: 1
                anchors.rightMargin: 1
                height: expandAreaHeight
                color: "transparent"
                clip: true
                
                Column {
                    id: content
                    anchors.fill: parent
                    
                    property variant expandId: undefined
                    
                    onExpandIdChanged: {
                        windowView.height = content.expandId == undefined ? defaultHeight : defaultHeight + listHeight
                        
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
                            header.item.active = expanded
                        }
                        
                        header.sourceComponent: DSwitchButtonHeader {
                            text: "源语言"
                            width: parent.width
                            anchors.left: parent.left
                            anchors.leftMargin: 2
                            anchors.right: parent.right
                            anchors.rightMargin: 2
                            
                            Component.onCompleted: {
                                active = sourceExpand.expanded
                            }
                            
                            onClicked: {
                                sourceExpand.expanded = active
                                if (active) {
                                    content.expandId = sourceExpand
                                } else {
                                    content.expandId = undefined
                                }
                            }
                        }
                        
                        content.sourceComponent: Rectangle {
                            width: parent.width
                            height: listHeight
                            color: "#181818"
                        }
                    }

                    DBaseExpand {
                        id: targetExpand
	                    expanded: false

                        onExpandedChanged: {
                            header.item.active = expanded
                        }
                        
                        header.sourceComponent: DSwitchButtonHeader {
                            text: "目标语言"
                            width: parent.width
                            anchors.left: parent.left
                            anchors.leftMargin: 2
                            anchors.right: parent.right
                            anchors.rightMargin: 2
                            
                            Component.onCompleted: {
                                active = targetExpand.expanded
                            }
                            onClicked: {
                                targetExpand.expanded = active
                                if (active) {
                                    content.expandId = targetExpand
                                } else {
                                    content.expandId = undefined
                                }
                            }
                        }
                        
                        content.sourceComponent: Rectangle {
                            width: parent.width
                            height: listHeight
                            color: "#181818"
                        }
                    }
                    
                    DBaseExpand {
                        id: wordExpand
	                    expanded: false

                        onExpandedChanged: {
                            header.item.active = expanded
                        }
                        
                        header.sourceComponent: DSwitchButtonHeader {
                            text: "单词翻译"
                            width: parent.width
                            anchors.left: parent.left
                            anchors.leftMargin: 2
                            anchors.right: parent.right
                            anchors.rightMargin: 2
                            
                            Component.onCompleted: {
                                active = wordExpand.expanded
                            }
                            onClicked: {
                                wordExpand.expanded = active
                                if (active) {
                                    content.expandId = wordExpand
                                } else {
                                    content.expandId = undefined
                                }
                            }
                        }
                        
                        content.sourceComponent: Rectangle {
                            width: parent.width
                            height: listHeight
                            color: "#181818"
                        }
                    }

                    DBaseExpand {
                        id: wordsExpand
	                    expanded: false

                        onExpandedChanged: {
                            header.item.active = expanded
                        }
                        
                        header.sourceComponent: DSwitchButtonHeader {
                            text: "长句翻译"
                            width: parent.width
                            anchors.left: parent.left
                            anchors.leftMargin: 2
                            anchors.right: parent.right
                            anchors.rightMargin: 2

                            Component.onCompleted: {
                                active = wordsExpand.expanded
                            }

                            onClicked: {
                                wordsExpand.expanded = active
                                if (active) {
                                    content.expandId = wordsExpand
                                } else {
                                    content.expandId = undefined
                                }
                            }
                        }
                        
                        content.sourceComponent: Rectangle {
                            width: parent.width
                            height: listHeight
                            color: "#181818"
                        }
                    }
                }
            }
            
            DTextButton {
                id: button
                text: "确定"
                /* anchors.bottom: parent.bottom */
                anchors.right: parent.right
                anchors.rightMargin: 10
                anchors.bottomMargin: 10
                anchors.topMargin: 25
                
                onClicked: {
                    windowView.hide()
                }
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
        id: expandAreaAnimation
        
        PropertyAnimation {
            target: expandArea
            property: "height"
            duration: 200
            from: expandAreaHeight
            to: expandAreaHeight + listHeight
            easing.type: Easing.OutQuint
        }
    }    

    ParallelAnimation{
        id: shrinkAreaAnimation
        
        PropertyAnimation {
            target: expandArea
            property: "height"
            duration: 200
            from: expandAreaHeight + listHeight
            to: expandAreaHeight
            easing.type: Easing.OutQuint
        }
    }    
}
