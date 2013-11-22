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
    
    Connections {
        target: suggestModel
        onFinished: {
            adjustSuggestionSize()
        }
    }
    
    function showTranslate() {
		suggestArea.visible = false
        adjustTranslateSize()
        autoSpeech()
    }
	
	function handleAccepted(text) {
        windowView.get_translate(text)
        adjustTranslateSize()
        suggestArea.visible = false
					
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
        suggestArea.width = listviewWidth
        suggestArea.height = listviewHeight
        
        var maxWidth = container.listviewWidth + (borderMargin + container.blurRadius) * 2
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
        
		Rectangle {
			id: itemHighlight
			width: parent.width
			height: itemHighlightHeight
			y: parent.y + keyword.height + itemHighlightIndex * itemHighlightHeight
			color: "#22FF0000"
			visible: false
			
            RadialGradient {
				id: highlightMiddle
                anchors.fill: parent
                horizontalRadius: parent.width * 1.54
                horizontalOffset: 0
                verticalRadius: parent.height * 3
                verticalOffset: -70
                
                gradient: Gradient {
                    GradientStop { position: 0.0; color: Qt.rgba(255 / 255.0, 243 / 255.0, 77 / 255.0, 0.5)}
                    GradientStop { position: 1.0; color: Qt.rgba(0, 0, 0, 0.4)}
                }
                
            }
			LinearGradient {
				id: highlightTopline
				width: parent.width
				height: 1
				anchors.top: parent.top
				start: Qt.point(0, 0)
				end: Qt.point(width, 0)
				gradient: Gradient {
					GradientStop { position: 0.0; color: Qt.rgba(255 / 255.0, 192 / 255.0, 0 / 255.0, 0.05)}
					GradientStop { position: 0.5; color: Qt.rgba(255 / 255.0, 243 / 255.0, 77 / 255.0, 0.45)}
					GradientStop { position: 1.0; color: Qt.rgba(255 / 255.0, 192 / 255.0, 0 / 255.0, 0.05)}
				}
				visible: itemHighlight.visible
			}

			LinearGradient {
				id: highlightBottomline
				width: parent.width
				height: 1
				anchors.bottom: parent.bottom
				start: Qt.point(0, 0)
				end: Qt.point(width, 0)
				gradient: Gradient {
					GradientStop { position: 0.0; color: Qt.rgba(255 / 255.0, 192 / 255.0, 0 / 255.0, 0.05)}
					GradientStop { position: 0.5; color: Qt.rgba(255 / 255.0, 243 / 255.0, 77 / 255.0, 0.15)}
					GradientStop { position: 1.0; color: Qt.rgba(255 / 255.0, 192 / 255.0, 0 / 255.0, 0.05)}
				}
				visible: itemHighlight.visible
			}
			
            Behavior on y {
                NumberAnimation {
                    duration: 200
                    easing.type: Easing.OutQuint
                }
            }
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
                
                onAccepted: {
					if (keyword.text != "") {
						handleAccepted(text)
					}
                }
                
                onInputChanged: {
                    container.listviewWidth = 0
                    container.listviewHeight = 0
					
					if (keyword.text == "") {
						listview.model = historyModel
						
					} else {
						listview.model = suggestModel
						
                        suggestModel.suggestWithNum(keyword.text, 5)
                        suggestArea.visible = true
                        
                        /* NOTE: we set enough size to make ListModel Component.onCompleted can calcuate before `finished` signal emit
                           DO NOT DELETE below code!!!
                           */
                        suggestArea.width = 1000
                        suggestArea.height = 1000
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
                        width: parent.width
                        height: titleText.paintedHeight + explainText.paintedHeight + itemSplitline.height
                        
						MouseArea {
							id: itemArea
							anchors.fill: parent
							hoverEnabled: true
							
							onPressed: {
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

                                Component.onCompleted: {
                                    if (titleText.paintedWidth > container.listviewWidth) {
                                        container.listviewWidth = titleText.paintedWidth
                                    }
                                    
                                    container.listviewHeight += titleText.paintedHeight
                                }
                            }
                            
                            Text {
                                id: explainText
                                text: explain
                                color: "#aaaaaa"
								font { pixelSize: 12 }
								anchors.topMargin: 1
								
                                Component.onCompleted: {
                                    if (explainText.paintedWidth > container.listviewWidth) {
                                        container.listviewWidth = explainText.paintedWidth
                                    }
                                    
                                    container.listviewHeight += explainText.paintedHeight
                                }
                            }
							
							Rectangle {
								id: itemSplitline
								width: listviewWidth
								height: 11
								anchors.topMargin: height / 2
								anchors.bottomMargin: anchors.topMargin
								color: Qt.rgba(0, 0, 0, 0)
								
								Component.onCompleted: {
									container.listviewHeight += itemSplitline.height
								}
								
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
                    /* model: keyword.text == "" ? historyModel : suggestModel */
                    model: suggestModel
                    delegate: contactDelegate
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
