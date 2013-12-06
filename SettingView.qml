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
    property int defaultHeight: 255
    property int expandAreaHeight: 123
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
                height: paintedHeight + 40
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                text: "深度翻译设置"
                color: "#fff"
			    font { pixelSize: 20 }
                
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
                
                property alias expandItems: contentItems.children
                property int expandItemIndex: -1
                
                onExpandItemIndexChanged: {
                    windowView.height = expandItemIndex == -1 ? defaultHeight : defaultHeight + listHeight
                }
                
                Column {
                    id: content
                    anchors.fill: parent
                    
                    Component {
                        id: sourceContent
                        Rectangle {
                            width: parent.width
                            height: listHeight
                            color: "#181818"
                        }
                    }

                    Component {
                        id: targetContent
                        Rectangle {
                            width: parent.width
                            height: listHeight
                            color: "#181818"
                        }
                    }

                    Component {
                        id: wordContent
                        Rectangle {
                            width: parent.width
                            height: listHeight
                            color: "#181818"
                        }
                    }

                    Component {
                        id: wordsContent
                        Rectangle {
                            width: parent.width
                            height: listHeight
                            color: "#181818"
                        }
                    }
                    
                    Item {
                        id: contentItems
                        
                        Item {
                            property string name: "源语言"
                            property variant item: sourceContent
                        }

                        Item {
                            property string name: "目标源"
                            property variant item: targetContent
                        }

                        Item {
                            property string name: "单词翻译"
                            property variant item: wordContent
                        }

                        Item {
                            property string name: "长句翻译"
                            property variant item: wordsContent
                        }
                    }
                    
                    Repeater {
                        model: expandArea.expandItems.length
                        delegate: DBaseExpand {
                            id: expand
                            expanded: expandArea.expandItemIndex == index
                            
                            onExpandedChanged: {
                                header.item.active = expanded
                            }
                            
                            header.sourceComponent: DDownArrowHeader {
                                text: expandArea.expandItems[index].name
                                width: parent.width
                                anchors.left: parent.left
                                anchors.leftMargin: 2
                                anchors.right: parent.right
                                anchors.rightMargin: 2
                                
                                Component.onCompleted: {
                                    active = expand.expanded
                                }
                                
                                onClicked: {
                                    expandArea.expandItemIndex = active ? index : -1
                                }
                            }
                            
                            content.sourceComponent: expandArea.expandItems[index].item
                        }
                    }
                }
            }
            
            DTextButton {
                id: button
                text: "确定"
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
