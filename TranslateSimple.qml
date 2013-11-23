import QtQuick 2.1
import QtMultimedia 5.0
import QtGraphicalEffects 1.0

RectWithCorner {
	id: container
    radius: 6
    cornerPos: 50
    cornerDirection: "up"
    
    property alias keyword: keyword
    property alias splitline: splitline
    property alias itemHighlight: itemHighlight
    property alias border: border
    property alias listview: listview
    property alias suggestArea: suggestArea
    property alias trans: trans
    property alias webtrans: webtrans
    property int borderMargin: 10
    property int textMargin: 10
    property int webPadding: 10
    property int splitHeight: 2 /* two split line's height */
	property int itemHighlightHeight: 45
	property int itemHighlightIndex: 0
	property bool inItem: false

    property int listviewWidth: 0
    property int listviewHeight: 0
	property int listviewLength: 0
	property int listviewMinWidth: 200
    
    Connections {
        target: suggestModel
        onFinished: {
			if (suggestArea.visible) {
				adjustSuggestionSize()
			}
        }
    }
	
	Connections {
		target: windowView
		onHided: {
			keyword.textInput.focus = false
			keyword.cursorWidth = 0
		}
	}
	
    function showTranslate() {
		suggestArea.visible = false
		itemHighlight.visible = false
		
        adjustTranslateSize()
        autoSpeech()
    }
	
	function handleAccepted(text) {
		itemHighlightIndex = 0
        windowView.get_translate(text)
		showTranslate()
		historyModel.addSearchData(translateInfo.keyword, translateInfo.trans, translateInfo.webtrans)
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
		listviewLength = listview.model.total()
		listviewWidth = 0
		listviewHeight = 0
		
		for (var i = 0; i < listviewLength; i++) {
			var item = listview.contentItem.children[i]
			
			if (typeof item != 'undefined') {
				listviewWidth = Math.max(item.width, listviewWidth, listviewMinWidth)
				listviewHeight += item.height
			}
		}
		
        suggestArea.width = listviewWidth
        suggestArea.height = listviewHeight
        
        var maxWidth = listviewWidth + (borderMargin + container.blurRadius) * 2
        var maxHeight = keyword.height + listviewHeight + container.cornerHeight + (borderMargin + container.blurRadius) * 2 + splitHeight
        
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
        
		SelectEffect {
			id: itemHighlight
			y: parent.y + keyword.height + itemHighlightIndex * itemHighlightHeight
		}
                
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
                
				onPressUp: {
					if (itemHighlight.visible) {
						itemHighlightIndex = Math.max(0, itemHighlightIndex - 1)
					} else {
						itemHighlightIndex = listviewLength - 1
						itemHighlight.visible = true
					}
				}
				
				onPressDown: {
					if (itemHighlight.visible) {
						itemHighlightIndex = Math.min(listviewLength - 1, itemHighlightIndex + 1)
					} else {
						itemHighlightIndex = 0
						itemHighlight.visible = true
					}
				}
				
                onAccepted: {
					if (itemHighlight.visible) {
						handleAccepted(listview.model.getTitle(itemHighlightIndex))
					} else if (keyword.text != "") {
						handleAccepted(text)
					}
                }
                
                onInputChanged: {
					itemHighlight.visible = false
					
					if (keyword.text == "") {
						listview.model = historyModel
					} else {
                        suggestModel.suggestWithNum(keyword.text, 5)
                        suggestArea.visible = true
						
						listview.model = suggestModel
					}
                }
            }
            
            Rectangle {
                anchors.left: parent.left
                anchors.right: parent.right
                height: 1
                color: "#11000000"
            }

            Rectangle {
				id: splitline
                anchors.left: parent.left
                anchors.right: parent.right
                height: 1
                color: "#11FFFFFF"
            }
            
            Rectangle {
                id: suggestArea
                anchors.left: parent.left
                anchors.right: parent.right
		        anchors.margins: borderMargin
                width: 200
                height: 300
                color: Qt.rgba(0, 0, 0, 0)
                visible: false
                clip: true
				
                Component {
                    id: contactDelegate
                    Item {
                        id: item
                        width: Math.max(titleText.paintedWidth, explainText.paintedWidth)
						height: titleText.paintedHeight + explainText.paintedHeight + itemSplitline.height
						visible: suggestArea.visible
						
						MouseArea {
							id: itemArea
							anchors.fill: parent
							hoverEnabled: true
							
							onClicked: {
								handleAccepted(titleText.text)
							}
							
							onEntered: {
								inItem = true
								itemHighlightIndex = index
								itemHighlight.visible = true
								
								explainText.color = "#ffffff"
							}
							
							onExited: {
								inItem = false
								hideItemHighlight.restart()
								
								explainText.color = "#aaaaaa"
							}
							
							Timer {
								id: hideItemHighlight
								interval: 100
								repeat: false
								
								onTriggered: {
									if (!inItem) {
										itemHighlight.visible = false
										itemHighlightIndex = 0
									}
								}
							}
						}
						
                        Column {
                            Text {
                                id: titleText
                                text: title
                                color: "#FFFFFF"
								anchors.topMargin: 1
                            }
                            
                            Text {
                                id: explainText
                                text: explain
                                color: "#aaaaaa"
								font { pixelSize: 12 }
								anchors.topMargin: 1
                            }
							
							Rectangle {
								id: itemSplitline
								width: listviewWidth
								height: 11
								anchors.topMargin: height / 2
								anchors.bottomMargin: anchors.topMargin
								color: Qt.rgba(0, 0, 0, 0)
								
								Rectangle {
									width: parent.width
									anchors.verticalCenter: parent.verticalCenter
									height: 1
									color: "#11FFFFFF"
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
					focus: true
					visible: suggestArea.visible
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
