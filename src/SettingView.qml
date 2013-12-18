import QtQuick 2.1
import QtGraphicalEffects 1.0
import QtQuick.Window 2.1
import QtQuick.Layouts 1.0
import Deepin.Locale 1.0
import "../widgets"

WindowFrame {
    id: window
    
    property int defaultWidth: 350
    property int defaultHeight: 320
    property int expandAreaHeight: 127
    property int listHeight: 240
    property int itemHeight: 30
    property alias expandArea: expandArea
    property alias windowItem: windowItem
    
    property variant dsslocale: DLocale {
        id: dsslocale
        dirname: "../locale"
        domain: "deepin-translator"
    }
    
    function dsTr(s){
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
                property string wordVoiceEngine: ""
                property string wordsVoiceEngine: ""
                property string srcLang: ""
                property string dstLang: ""
                
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
                
                function updateLanguage() {
                    var srcLang = settingConfig.get_translate_config("src_lang")
                    var dstLang = settingConfig.get_translate_config("dst_lang")
                    settingConfig.update_translate_config("src_lang", dstLang)
                    settingConfig.update_translate_config("dst_lang", srcLang)
                    expandArea.srcLang = dstLang
                    expandArea.dstLang = srcLang
                }
                
                Connections {
                    target: windowView
                    onUpdateLang: {
                        expandArea.srcLang = settingConfig.get_translate_config("src_lang")
                        expandArea.dstLang = settingConfig.get_translate_config("dst_lang")
                    }
                }
                
                Column {
                    id: content
                    anchors.fill: parent
                    
                    Item {
                        id: contentItems
                        
                        Item {
                            property string name: dsTr("Source language")
                            property variant model: sourceLangModel
                            property string type: "src_lang"
                        }

                        Item {
                            property string name: dsTr("Target language")
                            property variant model: destLangModel
                            property string type: "dst_lang"
                        }

                        Item {
                            property string name: dsTr("Word Translation")
                            property variant model: wordTranslateModel
                            property string type: "word_engine"
                        }

                        Item {
                            property string name: dsTr("Word speech")
                            property variant model: wordVoiceModel
                            property string type: "word_voice_engine"
                        }

                        Item {
                            property string name: dsTr("Full text translation")
                            property variant model: wordsTranslateModel
                            property string type: "words_engine"
                        }

                        Item {
                            property string name: dsTr("Sentences speech")
                            property variant model: wordVoiceModel
                            property string type: "words_voice_engine"
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
                                hintText: " (" + expand.currentDisplayName + ")"
                                width: defaultWidth
                                anchors.leftMargin: 2
                                anchors.rightMargin: 10
                                
                                Component.onCompleted: {
                                    active = expand.expanded
                                }
                                
                                onClicked: {
                                    expandArea.expandItemIndex = active ? index : -1
                                }
                            }
                            
                            content.sourceComponent: Component {
                                id: wordsContent
                                Rectangle {
                                    width: parent.width
                                    height: listHeight
                                    color: "transparent"
                                    
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
                                            target: expandArea
                                            onWordVoiceEngineChanged: {
                                                if (listview.type == "word_voice_engine") {
                                                    listview.currentName = settingConfig.get_translate_config(listview.type)
                                                }
                                            }
                                        }
                                        
                                        Connections {
                                            target: expandArea
                                            onWordsVoiceEngineChanged: {
                                                if (listview.type == "words_voice_engine") {
                                                    listview.currentName = settingConfig.get_translate_config(listview.type)
                                                }
                                            }
                                        }
                                        
                                        Connections {
                                            target: expandArea
                                            onSrcLangChanged: {
                                                if (listview.type == "src_lang") {
                                                    listview.currentName = settingConfig.get_translate_config(listview.type)
                                                }
                                            }
                                        }

                                        Connections {
                                            target: expandArea
                                            onDstLangChanged: {
                                                if (listview.type == "dst_lang") {
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
                                                    visible: ["src_lang", "dst_lang"].indexOf(listview.type) < 0
                                                    
                                                    Component.onCompleted: {
                                                        if (["word_engine", "words_engine"].indexOf(listview.type) >= 0) {
                                                            source = "dict_plugins/" + name + "/icon.png"
                                                        } else if (["word_voice_engine", "words_voice_engine"].indexOf(listview.type) >= 0) {
                                                            source = "tts_plugins/" + name + "/icon.png"
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
                                                        dictInterface.update_translate_engine(listview.type)
                                                        ttsIntreface.update_voice_with_src_lang()
                                                        expandArea.wordEngine = settingConfig.get_translate_config("word_engine")
                                                        expandArea.wordsEngine = settingConfig.get_translate_config("words_engine")
                                                        expandArea.wordVoiceEngine = settingConfig.get_translate_config("word_voice_engine")
                                                        expandArea.wordsVoiceEngine = settingConfig.get_translate_config("words_voice_engine")
                                                    } else if (listview.type == "dst_lang") {
                                                        dictInterface.update_translate_engine(listview.type)
                                                        expandArea.wordEngine = settingConfig.get_translate_config("word_engine")
                                                        expandArea.wordsEngine = settingConfig.get_translate_config("words_engine")
                                                    } else if (listview.type == "word_engine") {
                                                        dictInterface.update_word_module()
                                                    } else if (listview.type == "words_engine") {
                                                        dictInterface.update_words_module()
                                                    } else if (listview.type == "word_voice_engine") {
                                                        ttsIntreface.update_word_voice_module()
                                                    } else if (listview.type == "words_voice_engine") {
                                                        ttsIntreface.update_words_voice_module()
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
                                    
                                    DScrollBar {
                                        flickable: listview
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
            Item {
                width: parent.width
                anchors.bottom: parent.bottom
                
                DTextButton {
                    id: button
                    text: dsTr("OK")
                    anchors.right: parent.right
                    anchors.rightMargin: 10
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 10
                    
                    onClicked: {
                        windowView.hide()
                    }
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
