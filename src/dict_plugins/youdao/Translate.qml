import QtQuick 2.1
import QtQuick.Window 2.1
import Deepin.Locale 1.0
import QtMultimedia 5.0
import QtGraphicalEffects 1.0
import "../../../src"

TranslateWindow {
	id: container
    
    property alias keyword: keyword
    property alias splitline: splitline
    property alias itemHighlight: itemHighlight
    property alias border: border
    property alias listview: listview
    property alias listviewArea: listviewArea
    property alias trans: trans
    property alias webtrans: webtrans
    property int webPadding: 10
    property int splitHeight: 2 /* two split line's height */
	property int itemHighlightHeight: 45
	property int itemHighlightIndex: 0
	property int minWindowWidth: 200
	property bool inItem: false

    property int listviewWidth: 0
    property int listviewHeight: 0
	property int listviewLength: 0
    
    property int suggestionWidth: 0
    property int suggestionHeight: 0
	
    property variant dsslocale: DLocale {
        id: dsslocale
        dirname: "../../../locale"
        domain: "deepin-translator"
    }
    
    function dsTr(s){
        return dsslocale.dsTr(s)
    }
    
    Connections {
        target: suggestModel
        onFinished: {
			if (listviewArea.visible) {
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
	
	Connections {
		target: windowView
		onVisibleChanged: {
			if (!arg) {
                speechPlayer.stopAudio()
			}
		}
	}
    
    Player {
        id: speechPlayer
        voices: translateInfo.voices
    }
	
    function showTranslate(x, y, text) {
		mouseX = x
		mouseY = y
		
		/* Move window out of screen before adjust position */
		windowView.x = 100000
		windowView.y = 100000
		windowView.showNormal()
		windowView.get_translate(text)
		
		listviewArea.visible = false
		itemHighlight.visible = false
		
        adjustTranslateSize()
        speechPlayer.autoplayAudio()
    }
	
	function handleAccepted(text) {
		itemHighlightIndex = 0
        windowView.get_translate(text)
		
		listviewArea.visible = false
		itemHighlight.visible = false
		
        adjustTranslateSize()
        autoSpeech()
		
		historyModel.addSearchData(translateInfo.keyword, translateInfo.trans, translateInfo.webtrans)
	}
	
    function adjustTranslateSize() {
        var maxWidth = Math.max(
			minWindowWidth,
            trans.paintedWidth, 
            webtrans.paintedWidth, 
            usSpeech.getWidth()
        ) + (borderMargin + container.blurRadius) * 2
        
        var maxHeight = keyword.height + trans.paintedHeight + webtrans.paintedHeight + usSpeech.getHeight() + container.cornerHeight + (borderMargin + textMargin + container.blurRadius) * 2 + webPadding + splitHeight
        
        windowView.width = maxWidth
        windowView.height = maxHeight
		
        container.rectWidth = maxWidth
        container.rectHeight = maxHeight
        container.width = maxWidth
        container.height = maxHeight
		
		adjustPosition()		
    }
    
    function adjustSuggestionSize() {
		listviewLength = listview.model.total()
		listviewWidth = 0
		listviewHeight = 0
		
		for (var i = 0; i < listviewLength; i++) {
			var item = listview.contentItem.children[i]
			
			if (typeof item != 'undefined') {
				listviewWidth = Math.max(item.width, listviewWidth)
				listviewHeight += item.height
			}
		}
		
        listview.width = listviewWidth
        listview.height = listviewHeight
		
        suggestionWidth = Math.max(listviewWidth, minWindowWidth) + (borderMargin + container.blurRadius) * 2
        suggestionHeight = keyword.height + listviewHeight + container.cornerHeight + (borderMargin + container.blurRadius) * 2 + splitHeight

        adjustSuggestionTimer.restart()
    }
    
	Timer {
		id: adjustSuggestionTimer
		interval: 200
		repeat: false
		
		onTriggered: {
            windowView.width = suggestionWidth
            windowView.height = suggestionHeight
            
            container.rectWidth = suggestionWidth
            container.rectHeight = suggestionHeight
            container.width = suggestionWidth
            container.height = suggestionHeight
		    
		    adjustPosition()		
		}
	}
    
	Rectangle {
        id: border
        radius: 6
	    anchors.fill: parent
        anchors.topMargin: cornerDirection == "up" ? borderMargin + container.cornerHeight : borderMargin
		anchors.bottomMargin: borderMargin
		anchors.leftMargin: borderMargin
		anchors.rightMargin: borderMargin
        color: Qt.rgba(0, 0, 0, 0)
        
		SelectEffect {
			id: itemHighlight
			y: cornerDirection == "down" ? selectY + container.cornerHeight : selectY
            
            property int selectY: parent.y + keyword.height + itemHighlightIndex * itemHighlightHeight
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
					/* This is hacking way to make listview load models complete
					   Listview can't load models complete if it haven't enough space.
					 */
		            itemHighlightIndex = 0
					listviewArea.width = 1000
					listviewArea.height = 1000
		
					itemHighlight.visible = false
					
					if (keyword.text == "") {
                        listviewArea.visible = true
						itemHighlight.visible = false
						
						listview.model = historyModel
						
						adjustSuggestionSize()
					} else {
                        suggestModel.suggestWithNum(keyword.text, 5)
						
                        listviewArea.visible = true
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
                id: listviewArea
                width: parent.width
                height: listviewHeight
                color: Qt.rgba(0, 0, 0, 0)
                visible: false
                clip: true
				
                Component {
                    id: contactDelegate
                    Item {
                        id: item
                        width: Math.max(titleText.paintedWidth, explainText.paintedWidth)
						height: titleText.paintedHeight + explainText.paintedHeight + itemSplitline.height
						visible: listviewArea.visible
						
						MouseArea {
							id: itemArea
							width: listview.width
							height: parent.height
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
                            id: itemWrap
						    anchors.left: parent.left
						    anchors.right: parent.right
						    anchors.leftMargin: borderMargin
						    anchors.rightMargin: borderMargin
						
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
								width: container.width - (borderMargin + container.blurRadius) * 2
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
					visible: listviewArea.visible
				}
            }
            
			Speech { 
                id: usSpeech
				text: dsTr("Read")
                anchors.left: parent.left
		        anchors.leftMargin: textMargin
                
				onClicked: {
                    speechPlayer.playAudio()
				}
            }
            
            Rectangle {
                anchors.left: parent.left
                anchors.right: parent.right
                height: 10
                color: Qt.rgba(0, 0, 0, 0)
                visible: !listviewArea.visible
            }
            
            Column {
                anchors.left: parent.left
                anchors.right: parent.right
		        anchors.leftMargin: textMargin
		        anchors.rightMargin: textMargin
                spacing: webPadding
                visible: !listviewArea.visible
                
		        TextEdit { 
                    id: trans
			        text: translateInfo.trans
                    textFormat: TextEdit.RichText
			        wrapMode: TextEdit.Wrap
			        selectByMouse: true
			        font { pixelSize: 14 }
			        color: "#FFFFFF"
					selectionColor: "#11ffffff"
					selectedTextColor: "#5da6ce"
                    
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
					selectionColor: "#11ffffff"
					selectedTextColor: "#5da6ce"

                    onTextChanged: {
                        cursorPosition: 0
                        cursorVislble: false
                    }
		        }
            }
	    }        
	}
}
