import QtQuick 2.1
import Deepin.Locale 1.0
import "../widgets"

Row {
    id: toolbar
    height: 24
    spacing: 5
    
    property string text
    property variant player
    property variant window
    
    property alias entryArea: entryArea
    property alias splitView: splitView
    property alias entry: entry
    property alias items: items
    property alias arrow: arrow
    property alias tooltip: tooltip
    property alias iconChildren: iconItems.children
    
    property int imageWidth: 16
    property int itemSpacing: 5
    property int itemWidth: imageWidth + itemSpacing
    
    property bool inButtonArea: false
    
    property variant dsslocale: DLocale {
        id: dsslocale
        dirname: "../locale"
        domain: "deepin-translator"
    }
    
    function dsTr(s){
        return dsslocale.dsTr(s)
    }
    
    function init(resetPosition) {
        entryArea.width = splitView.width - itemWidth
        entry.cursorWidth = 0
        arrow.expand = false
        arrow.source = "image/left_arrow.png"
        
        if (resetPosition) {
            entry.textInput.cursorPosition = 0
        }
    }
    
    function resetCursor() {
        entry.textInput.cursorPosition = 0
    }
    
    Item {
        id: iconItems
        
        Item {
            property string imagePath: "image/speaker.png"
            property string tooltip: dsTr("Voice")
            property string type: "voice"
        }

        Item {
            property string imagePath: "image/paste.png"
            property string tooltip: dsTr("Copy to clipboard")
            property string type: "paste"
        }

        Item {
            property string imagePath: "image/wikipedia.png"
            property string tooltip: dsTr("Wikipedia")
            property string type: "wikipedia"
        }

        Item {
            property string imagePath: "image/search.png"
            property string tooltip: dsTr("Google")
            property string type: "google"
        }
    }
    
    SplitView {
        id: splitView
        anchors.verticalCenter: parent.verticalCenter
        width: parent.width - arrow.width
        height: parent.height
        
        Row {
            id: entryArea
            height: parent.height
            width: parent.width - itemWidth
            anchors.verticalCenter: parent.verticalCenter
            
            Rectangle {
                height: parent.height
                width: parent.width - splitline.width
                anchors.verticalCenter: parent.verticalCenter
                color: "transparent"
                
                Entry {
                    id: entry
                    anchors.fill: parent
                    text: toolbar.text
                    visible: !tooltip.visible
                }
                
                Text {
                    id: tooltip
                    anchors.fill: parent
                    anchors.rightMargin: 5
                    anchors.verticalCenter: parent.verticalCenter
                    color: "grey"
                    horizontalAlignment: Text.AlignRight
                    verticalAlignment: Text.AlignVCenter
                    visible: false
		            font { pixelSize: 14 }
                }
            }
            
            Rectangle {
                id: splitline
                height: parent.height
                width: 7
                color: "transparent"
                
                Rectangle {
                    height: parent.height
                    width: 1
                    color: Qt.rgba(1, 1, 1, 0.15)
                }
            }
        }
        
        Row {
            id: items
            spacing: 5
            anchors.verticalCenter: parent.verticalCenter
            height: parent.height
            
            Repeater {
                model: iconChildren.length
                
                delegate: DOpacityImageButton {
                    id: iconButton
                    source: iconChildren[index].imagePath
                    anchors.verticalCenter: parent.verticalCenter
                    
                    Connections {
                        target: iconButton.mouseArea
                        onEntered: {
                            tooltip.text = iconChildren[index].tooltip
                            tooltip.visible = true
                            
                            toolbar.inButtonArea = true
                        }
                        
                        onExited: {
                            toolbar.inButtonArea = false
                            
                            showEntryTimer.restart()
                        }
                        
                        onClicked: {
                            if (iconChildren[index].type == "voice") {
                                player.playAudio()
                            } else if (iconChildren[index].type == "paste") {
                                window.hide()
                                window.save_to_clipboard(text)
                            } else if (iconChildren[index].type == "wikipedia") {
                                window.hide()
                                var lang = settingConfig.get_translate_config("dst_lang").toLowerCase()
                                Qt.openUrlExternally("https://" + lang.split("-", 1)[0] + ".wikipedia.org/" + lang + "/" + toolbar.text)
                            } else if (iconChildren[index].type == "google") {
                                window.hide()
                                Qt.openUrlExternally("https://www.google.com/search?q=" + toolbar.text)
                            }
                        }
                    }
                }
            }
        }
    }
    
    DOpacityImageButton {
        id: arrow
        anchors.verticalCenter: parent.verticalCenter
        source: "image/left_arrow.png"
        
        property bool expand: false
        
        Rectangle {
            id: hoverArea
            anchors.fill: parent
            anchors.topMargin: -2
            anchors.bottomMargin: -2
            color: Qt.rgba(1, 1, 1, 0.2)
            visible: false
        }
        
        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            
            onClicked: {
                if (arrow.expand) {
                    arrow.source = "image/left_arrow.png"
                    shrinkAnimation.restart()
                } else {
                    arrow.source = "image/right_arrow.png"
                    expandAnimation.restart()
                }
                
                arrow.expand = !arrow.expand
            }
            
            onEntered: {
                hoverArea.visible = true
            }
            
            onExited: {
                hoverArea.visible = false
            }
        }
    }
    
    Timer {
        id: showEntryTimer
		interval: 200
		repeat: false

        onTriggered: {
            if (!toolbar.inButtonArea) {
                tooltip.visible = false
            }
        }
    }
    
    ParallelAnimation{
        id: expandAnimation
        
        SmoothedAnimation {
            target: entryArea
            property: "width"
            duration: 200
            from: splitView.width - itemWidth
            to: splitView.width - itemWidth * iconChildren.length
        }
    }

    ParallelAnimation {
        id: shrinkAnimation
        
        SmoothedAnimation {
            target: entryArea
            property: "width"
            duration: 200
            from: splitView.width - itemWidth * iconChildren.length
            to: splitView.width - itemWidth
        }
    }
}
