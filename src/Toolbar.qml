import QtQuick 2.1
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
    
    property int imageWidth: 16
    property int itemSpacing: 5
    property int itemWidth: imageWidth + itemSpacing
    
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
            width: parent.width - itemWidth
            
            Entry {
                id: entry
                width: parent.width - splitline.width
                text: toolbar.text
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
                source: "image/speaker.png"
                
                onClicked: {
                    player.playAudio()
                }
            }

            DOpacityImageButton {
                source: "image/paste.png"
                
                onClicked: {
                    window.hide()
                    
                    window.save_to_clipboard(text)
                }
            }

            DOpacityImageButton {
                source: "image/wikipedia.png"

                onClicked: {
                    var lang = settingConfig.get_translate_config("src_lang")
                    Qt.openUrlExternally("https://" + lang + ".wikipedia.org/wiki/" + toolbar.text)
                    window.hide()
                }
            }

            DOpacityImageButton {
                source: "image/search.png"

                onClicked: {
                    Qt.openUrlExternally("https://www.google.com/search?q=" + toolbar.text)
                    window.hide()
                }
            }
        }
    }
    
    DOpacityImageButton {
        id: arrow
        anchors.verticalCenter: parent.verticalCenter
        source: "image/left_arrow.png"
        
        property bool expand: false
        
        MouseArea {
            anchors.fill: parent
            
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

    ParallelAnimation{
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
