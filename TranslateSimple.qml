import QtQuick 2.1
import QtMultimedia 5.0

RectWithCorner {
	id: container
    radius: 6
    cornerPos: 50
    cornerDirection: "up"
    
    property alias keyword: keyword
    property alias listview: listview
    property alias suggestArea: suggestArea
    property alias trans: trans
    property alias webtrans: webtrans
    property int borderMargin: 10
    property int textMargin: 10
    property int webPadding: 10
    property int splitHeight: 2 /* two split line's height */

    property int listviewWidth: 0
    property int listviewHeight: 0
    
    Connections {
        target: suggestModel
        onFinished: {
            adjustSuggestionSize()
        }
    }
    
    function showTranslate() {
        adjustTranslateSize()
        autoSpeech()
    }
    
    function adjustTranslateSize() {
        var maxWidth = Math.max(
            trans.paintedWidth, 
            webtrans.paintedWidth, 
            usSpeech.getWidth() + ukSpeech.getWidth()
        ) + (borderMargin + container.blurRadius) * 2
        
        var maxHeight = keyword.height + trans.paintedHeight + webtrans.paintedHeight + ukSpeech.getHeight() + container.cornerHeight + (borderMargin + textMargin + container.blurRadius) * 2 + webPadding + splitHeight
        
        windowView.width = maxWidth
        windowView.height = maxHeight
        
        container.rectWidth = maxWidth
        container.rectHeight = maxHeight
        container.width = maxWidth
        container.height = maxHeight
    }
    
    function adjustSuggestionSize() {
        var maxWidth = container.listviewWidth + (borderMargin + container.blurRadius) * 2
        var maxHeight = keyword.height + listviewHeight + container.cornerHeight + (borderMargin + textMargin + container.blurRadius) * 2 + splitHeight
        
        windowView.width = maxWidth
        windowView.height = maxHeight
        
        container.rectWidth = maxWidth
        container.rectHeight = maxHeight
        container.width = maxWidth
        container.height = maxHeight
    }
    
    function autoSpeech() {
        var speechlink = translateInfo.uslink ? translateInfo.uslink : translateInfo.uklink
        if (speechlink) {
		    audioPlayer.source = speechlink
            audioPlayer.play()
        }
    }
	
    Audio {
        id: audioPlayer
    }
    
	Rectangle {
        id: border
        radius: 6
	    anchors.fill: parent
        anchors.topMargin: borderMargin + container.cornerHeight
		anchors.bottomMargin: borderMargin
		anchors.leftMargin: borderMargin
		anchors.rightMargin: borderMargin
        color: Qt.rgba(0, 0, 0, 0)
        
	    Column {
		    spacing: 5
		    anchors.fill: parent
		    anchors.topMargin: textMargin
		    anchors.bottomMargin: textMargin
		    
            Entry {
                id: keyword
                objectName: "textInput"
                text: translateInfo.keyword
                anchors.left: parent.left
                anchors.right: parent.right
		        anchors.leftMargin: textMargin
		        anchors.rightMargin: textMargin
                
                onAccepted: {
                    windowView.get_translate(text)
                    adjustTranslateSize()
                    suggestArea.visible = false
                }
                
                onInputChanged: {
                    container.listviewWidth = 0
                    container.listviewHeight = 0
                    
                    suggestModel.suggest(keyword.text)
                    suggestArea.visible = true
                }
            }
            
            Rectangle {
                anchors.left: parent.left
                anchors.right: parent.right
                height: 1
                color: "#11000000"
            }

            Rectangle {
                anchors.left: parent.left
                anchors.right: parent.right
                height: 1
                color: "#11FFFFFF"
            }
            
            Rectangle {
                id: suggestArea
                anchors.left: parent.left
                anchors.right: parent.right
		        anchors.leftMargin: textMargin
		        anchors.rightMargin: textMargin
                width: 200
                height: 300
                color: Qt.rgba(0, 0, 0, 0)
                visible: false
                
                Component {
                    id: contactDelegate
                    Item {
                        width: 200
                        height: 40
                        
                        Column {
                            Text {
                                id: titleText
                                text: title
                                color: "#ffffff"

                                Component.onCompleted: {
                                    if (titleText.paintedWidth > container.listviewWidth) {
                                        container.listviewWidth = titleText.paintedWidth
                                    }
                                    
                                    container.listviewHeight = container.listviewHeight + titleText.paintedHeight
                                }
                            }
                            
                            Text {
                                id: explainText
                                text: explain
                                color: "#ffffff"
                                
                                Component.onCompleted: {
                                    if (explainText.paintedWidth > container.listviewWidth) {
                                        container.listviewWidth = explainText.paintedWidth
                                    }
                                    
                                    container.listviewHeight = container.listviewHeight + titleText.paintedHeight
                                }
                            }
                        }
                    }
                }

                ListView {
                    id: listview
                    anchors.fill: parent
                    model: suggestModel
                    delegate: contactDelegate
                    highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
                    focus: true
                }
            }
            
		    Row {
                id: speech
			    spacing: 10
                anchors.left: parent.left
                anchors.right: parent.right
		        anchors.leftMargin: textMargin
		        anchors.rightMargin: textMargin
                visible: !suggestArea.visible
			    
			    Speech { 
                    id: usSpeech
                    text: translateInfo.usphone
                    type: "[美]"
                    
					onClicked: {
						audioPlayer.source = translateInfo.uslink
						audioPlayer.play()
					}
                }			
                
			    Speech { 
                    id: ukSpeech
                    text: translateInfo.ukphone 
                    type: "[英]"
					onClicked: {
						audioPlayer.source = translateInfo.uklink
						audioPlayer.play()
					}
                }
		    }
            
            Rectangle {
                anchors.left: parent.left
                anchors.right: parent.right
                height: 10
                color: Qt.rgba(0, 0, 0, 0)
                visible: !suggestArea.visible
            }
            
            Column {
                anchors.left: parent.left
                anchors.right: parent.right
		        anchors.leftMargin: textMargin
		        anchors.rightMargin: textMargin
                spacing: webPadding
                visible: !suggestArea.visible
                
		        TextEdit { 
                    id: trans
			        text: translateInfo.trans
                    textFormat: TextEdit.RichText
			        wrapMode: TextEdit.Wrap
			        selectByMouse: true
			        font { pixelSize: 14 }
			        color: "#FFFFFF"
                    
                    onTextChanged: {
                        cursorPosition: 0
                        cursorVislble: false
                    }
		        }		
		        
		        TextEdit {
                    id: webtrans
			        text: translateInfo.webtrans
                    textFormat: TextEdit.RichText
			        wrapMode: TextEdit.Wrap
			        selectByMouse: true
			        font { pixelSize: 14 }
			        color: "#FFFFFF"

                    onTextChanged: {
                        cursorPosition: 0
                        cursorVislble: false
                    }
		        }
            }
	    }        
	}
}
