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
    
    SplitView {
        id: splitView
        anchors.verticalCenter: parent.verticalCenter
        width: parent.width - arrow.width
        
        Row {
            id: entryArea
            height: parent.height
            width: parent.width - itemWidth
            
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
                    color: "grey"
                    horizontalAlignment: Text.AlignRight
                    visible: false
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
            
            DOpacityImageButton {
                id: speakerButton
                source: "image/speaker.png"
                
                Connections {
                    target: speakerButton.mouseArea
                    onEntered: {
                        tooltip.text = dsTr("Voice")
                        tooltip.visible = true
                        
                        toolbar.inButtonArea = true
                    }
                    
                    onExited: {
                        toolbar.inButtonArea = false
                        
                        showEntryTimer.restart()
                    }
                    
                    onClicked: {
                        player.playAudio()
                    }
                }
            }

            DOpacityImageButton {
                id: pasteButton
                source: "image/paste.png"

                Connections {
                    target: pasteButton.mouseArea
                    onEntered: {
                        tooltip.text = dsTr("Copy to clipboard")
                        tooltip.visible = true

                        toolbar.inButtonArea = true
                    }
                    
                    onExited: {
                        toolbar.inButtonArea = false
                        
                        showEntryTimer.restart()
                    }
                    
                    onClicked: {
                        window.hide()
                        
                        window.save_to_clipboard(text)
                    }
                }
            }

            DOpacityImageButton {
                id: wikiButton
                source: "image/wikipedia.png"

                Connections {
                    target: wikiButton.mouseArea
                    onEntered: {
                        tooltip.text = dsTr("Wikipedia")
                        tooltip.visible = true
                        
                        toolbar.inButtonArea = true
                    }
                    
                    onExited: {
                        toolbar.inButtonArea = false
                        
                        showEntryTimer.restart()
                    }
                    
                    onClicked: {
                        var lang = settingConfig.get_translate_config("src_lang")
                        Qt.openUrlExternally("https://" + lang.split("-", 1)[0] + ".wikipedia.org/wiki/" + toolbar.text)
                        window.hide()
                    }
                }
            }

            DOpacityImageButton {
                id: searchButton
                source: "image/search.png"

                Connections {
                    target: searchButton.mouseArea
                    onEntered: {
                        tooltip.text = dsTr("Google")
                        tooltip.visible = true
                        
                        toolbar.inButtonArea = true
                    }
                    
                    onExited: {
                        toolbar.inButtonArea = false
                        
                        showEntryTimer.restart()
                    }
                    
                    onClicked: {
                        Qt.openUrlExternally("https://www.google.com/search?q=" + toolbar.text)
                        window.hide()
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
            to: splitView.width - itemWidth * items.children.length
        }
    }

    ParallelAnimation {
        id: shrinkAnimation
        
        SmoothedAnimation {
            target: entryArea
            property: "width"
            duration: 200
            from: splitView.width - itemWidth * items.children.length
            to: splitView.width - itemWidth
        }
    }
}
