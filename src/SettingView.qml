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
    property int expandAreaHeight: 127
    property int listHeight: 240
    
    property alias expandArea: expandArea
    
    Component.onCompleted: {
        windowView.width = defaultWidth
        windowView.height = defaultHeight
        windowView.x = (screenWidth - defaultWidth) / 2
        windowView.y = (screenHeight - defaultHeight) / 2
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
                
                property alias expandItems: contentItems.children
                property int expandItemIndex: -1
                property int expandItemIndexHistory: -1
                
                onExpandItemIndexChanged: {
                    if (expandItemIndex == -1) {
                        if (expandItemIndexHistory != -1) {
                            shrinkAreaAnimation.restart()
                        }
                    } else {
                        if (expandItemIndexHistory == -1) {
                            windowView.height = defaultHeight + listHeight
                            expandAreaAnimation.restart()
                        }
                    }
                    
                    expandItemIndexHistory = expandItemIndex
                }
                
                Column {
                    id: content
                    anchors.fill: parent
                    
                    Item {
                        id: contentItems
                        
                        Item {
                            property string name: "源语言"
                            property variant model: sourceLangModel
                            property string type: "src_lang"
                        }

                        Item {
                            property string name: "目标源"
                            property variant model: destLangModel
                            property string type: "dst_lang"
                        }

                        Item {
                            property string name: "单词翻译"
                            property variant model: wordTranslateModel
                            property string type: "word_engine"
                        }

                        Item {
                            property string name: "长句翻译"
                            property variant model: wordsTranslateModel
                            property string type: "words_engine"
                        }
                    }
                    
                    Repeater {
                        model: expandArea.expandItems.length
                        delegate: DBaseExpand {
                            id: expand
                            expanded: expandArea.expandItemIndex == index
                            
                            property string currentDisplayName: ""
                            
                            onExpandedChanged: {
                                header.item.active = expanded
                            }
                            
                            header.sourceComponent: DDownArrowHeader {
                                text: expandArea.expandItems[index].name
                                darkText: expand.currentDisplayName
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
                            
                            content.sourceComponent: Component {
                                id: wordsContent
                                ScrollWidget {
                                    width: parent.width
                                    height: listHeight
                                    
                                    ListView {
                                        id: listview
                                        anchors.fill: parent
                                        model: expandArea.expandItems[index].model
                                        
                                        property string type: expandArea.expandItems[index].type
                                        property string currentName: ""
                                        
                                        Component.onCompleted: {
                                            listview.currentName = settingConfig.get_translate_config(listview.type)
                                            expand.currentDisplayName = model.getDisplayName(listview.currentName)
                                        }
                                        
                                        Connections {
                                            target: expand
                                            onExpandedChanged: {
                                                if (expand.expanded) {
                                                    listview.positionViewAtIndex(expandArea.expandItems[index].model.getNameIndex(listview.currentName), ListView.Center)
                                                }
                                            }
                                        }
                                        
                                        delegate: Item {
                                            width: parent.width
                                            height: 24
                                            anchors.left: parent.left
                                            anchors.leftMargin: 15
                                            
                                            Row {
                                                spacing: 5
                                                anchors.verticalCenter: parent.verticalCenter
                                                
                                                Image {
                                                    id: nameImage
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    source: "image/select.png"
                                                    opacity: listview.currentName == name ? 1 : 0
                                                }
                                                
                                                Text {
                                                    id: nameText
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    text: displayName
                                                    color: listview.currentName == name ? "#009EFF" : "#fff"
                                                    font.pixelSize: 12
                                                }
                                            }
                                            
                                            MouseArea {
                                                anchors.fill: parent
                                                hoverEnabled: true
                                                
                                                onEntered: {
                                                    listview.currentIndex = index
                                                }
                                                
                                                onClicked: {
                                                    settingConfig.update_translate_config(listview.type, name)
                                                    listview.currentName = settingConfig.get_translate_config(listview.type)
                                                    
                                                    expand.currentDisplayName = displayName
                                                    
                                                    if (listview.type == "src_lang") {
                                                    } else if (listview.type == "dst_lang") {
                                                    }
                                                }
                                            }
                                        }
                                        highlight: Rectangle {
                                            width: parent.width
                                            anchors.left: parent.left
                                            anchors.right: parent.right
                                            anchors.leftMargin: 5
                                            anchors.rightMargin: 5
                                            height: 24
                                            color: "#0D0D0D"
                                            radius: 4
                                        }                                        
                                        highlightMoveDuration: 200
				                        focus: true
				                        interactive: true
                                    }
                                }
                            }
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
        
        SmoothedAnimation {
            target: expandArea
            property: "height"
            duration: 200
            from: expandAreaHeight
            to: expandAreaHeight + listHeight
        }
    }    

    ParallelAnimation{
        id: shrinkAreaAnimation
        
         SmoothedAnimation {
            target: expandArea
            property: "height"
            duration: 200
            from: expandAreaHeight + listHeight
            to: expandAreaHeight
        }
         
        onRunningChanged: {
            if (!shrinkAreaAnimation.running) {
                windowView.height = defaultHeight
            }
        }
    }    
}
