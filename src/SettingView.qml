import QtQuick 2.1
import QtGraphicalEffects 1.0
import QtQuick.Window 2.1
import QtQuick.Layouts 1.0
import Deepin.Locale 1.0
import "../widgets"

WindowFrame {
    id: window
    
    property int defaultWidth: 350
    property int defaultHeight: 255
    property int expandAreaHeight: 127
    property int listHeight: 240
    property int itemHeight: 30
    property alias expandArea: expandArea
    
    property variant dsslocale: DLocale {
        id: dsslocale
        domain: "deepin-translator"
        dirname: "../locale"
    }
    
    function dsTr(s){
        print("*** ", dsslocale.dirname, dsslocale.lang)
        return dsslocale.dsTr(s)
    }
    
    Component.onCompleted: {
        windowView.width = defaultWidth
        windowView.height = defaultHeight
        windowView.x = (screenWidth - defaultWidth) / 2
        windowView.y = (screenHeight - defaultHeight) / 2
    }
    
    Item {
        id: windowItem
        
        anchors.fill: parent
        
        CloseButton {
            onClicked: {
                windowView.hide()
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
                text: dsTr("Deepin Translator Settings")
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
                property string wordEngine: ""
                property string wordsEngine: ""
                
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
                            property string name: dsTr("Source Language")
                            property variant model: sourceLangModel
                            property string type: "src_lang"
                        }

                        Item {
                            property string name: dsTr("Target Language")
                            property variant model: destLangModel
                            property string type: "dst_lang"
                        }

                        Item {
                            property string name: dsTr("Word Translate")
                            property variant model: wordTranslateModel
                            property string type: "word_engine"
                        }

                        Item {
                            property string name: dsTr("Sentences Translate")
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
                                hintText: expand.currentDisplayName
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
                                        
                                        onCurrentNameChanged: {
                                            expand.currentDisplayName = model.getDisplayName(listview.currentName)
                                        }
                                        
                                        Component.onCompleted: {
                                            listview.currentName = settingConfig.get_translate_config(listview.type)
                                        }
                                        
                                        Connections {
                                            target: expandArea
                                            onWordEngineChanged: {
                                                if (listview.type == "word_engine") {
                                                    listview.currentName = settingConfig.get_translate_config(listview.type)
                                                }
                                            }
                                        }
                                        
                                        Connections {
                                            target: expandArea
                                            onWordsEngineChanged: {
                                                if (listview.type == "words_engine") {
                                                    listview.currentName = settingConfig.get_translate_config(listview.type)
                                                }
                                            }
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
                                            height: itemHeight
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

                                                Image {
                                                    id: iconImage
                                                    anchors.verticalCenter: parent.verticalCenter
                                                    visible: listview.type == "word_engine" || listview.type == "words_engine"
                                                    
                                                    Component.onCompleted: {
                                                        if (listview.type == "word_engine" || listview.type == "words_engine") {
                                                            source = "plugins/" + name + "/icon.png"
                                                        } else {
                                                            source = ""
                                                        }

                                                    }
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
                                                    
                                                    if (listview.type == "src_lang") {
                                                        translateInfo.update_translate_engine()
                                                        expandArea.wordEngine = settingConfig.get_translate_config("word_engine")
                                                        expandArea.wordsEngine = settingConfig.get_translate_config("words_engine")
                                                    } else if (listview.type == "dst_lang") {
                                                        translateInfo.update_translate_engine()
                                                        expandArea.wordEngine = settingConfig.get_translate_config("word_engine")
                                                        expandArea.wordsEngine = settingConfig.get_translate_config("words_engine")
                                                    } else if (listview.type == "word_engine") {
                                                        translateInfo.update_word_module()
                                                    } else if (listview.type == "words_engine") {
                                                        translateInfo.update_words_module()
                                                    }
                                                }
                                            }
                                        }
                                        
                                        highlight: Rectangle {
                                            anchors.leftMargin: 5
                                            anchors.rightMargin: 5
                                            height: itemHeight
                                            color: "#0D0D0D"
                                            radius: 4
                                            
                                            /* We shoulde set parent when onCompleted signal to fixed 'Result of expression is not an object' */
                                            Component.onCompleted: {
                                                anchors.left = parent.left
                                                anchors.right = parent.right
                                            }
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
                text: dsTr("OK")
                anchors.right: parent.right
                anchors.rightMargin: 10
                anchors.bottomMargin: 10
                anchors.topMargin: 25
                
                onClicked: {
                    windowView.hide()
                }
            }
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
}
