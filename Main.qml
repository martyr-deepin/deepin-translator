import QtQuick 2.1
import QtWebKit 3.0

Item {
    id: window
    
    property bool inTranslateArea: false
    property alias translateArea: translateArea
    property alias translateView: translateView
    property alias translateWindow: translateWindow
    property alias selectArea: selectArea
    property alias windowArea: windowArea
    
    Rectangle {
        anchors.fill: parent
        color: Qt.rgba(0, 0, 0, 0)
        
        MouseArea {
            id: windowArea
            anchors.fill: parent
            hoverEnabled: true
                        
            property bool isHover: false
            property bool isDoubleClick: false
            
            onPressed: {
                isHover = false
                isDoubleClick = false
            }
            
            onClicked: {
                hidingTranslateTimer.interval = 200
                hidingTranslateTimer.restart()
            }
            
            onDoubleClicked: {
                isDoubleClick = true
                qApp.quit()
            }
        
            onPositionChanged: {
                isHover = true
                
                selectArea.visible = false
                
                testTimer.testMouseX = mouseX
                testTimer.testMouseY = mouseY
                
                testTimer.restart()
            }
            
            Component.onCompleted: {
                var point = JSON.parse(ocr.get_cursor_pos())
                testTimer.testMouseX = point[0]
                testTimer.testMouseY = point[1]
                testTimer.restart()
            }
            
            Rectangle {
                id: selectArea
                color: Qt.rgba(100, 0, 0, 0.5)
                visible: false
                height: 3
                
            }
        
            Rectangle {
                id: translateWindow
                anchors.left: selectArea.right
                anchors.top: selectArea.bottom
                color: Qt.rgba(0, 0, 0, 0.8)
                width: 800
                height: 400
                radius: 3
                border.color: Qt.rgba(10, 10, 10, 0.5)
                visible: false
                
                WebView {
                    id: translateView
                    anchors.fill: parent
                    anchors.topMargin: 10
                    anchors.bottomMargin: 10
                    anchors.leftMargin: 10
                    anchors.rightMargin: 10
                    url: ""
                }
                
                MouseArea {
                    id: translateArea
                    anchors.fill: parent
                    hoverEnabled: true
                    
                    onEntered: {
                        testTimer.stop()
                        selectArea.visible = true
                    }
                    
                    onExited: {
                        hidingTranslateTimer.interval = 200
                        hidingTranslateTimer.restart()
                    }
                }
            }            
        }

        Timer {
            id: testTimer
            interval: 500
            repeat: false
            
            property int testMouseX: 0
            property int testMouseY: 0
           
            onTriggered: {
                var wordInfo = JSON.parse(ocr.get_word_rect(testMouseX, testMouseY))
                if (wordInfo != "") {
                    selectArea.x = wordInfo[0] 
                    selectArea.y = wordInfo[1]  + wordInfo[3] + wordInfo[3] / 10
                    selectArea.width = wordInfo[2]
                    
                    translateView.url = "http://cn.bing.com/dict/search?q=" + wordInfo[4]
                    
                    selectArea.visible = true
                    translateWindow.visible = true
                                    
                    hidingTranslateTimer.interval = 10000
                    hidingTranslateTimer.restart()
                }
             }
        }
        
        Timer {
            id: hidingTranslateTimer
            interval: 200
            repeat: false
            
            onTriggered: {
                console.log(translateArea.containsMouse)
                if (!translateArea.containsMouse) {
                    selectArea.visible = false
                    translateWindow.visible = false
                }
            }
        }
    }
    
}
