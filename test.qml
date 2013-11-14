import QtQuick 2.1
import QtWebKit 3.0

Item {
    id: window
    
    property alias translateView: translateView
    property alias translateWindow: translateWindow
    
    function showTranslate(x, y, word) {
        windowView.showNormal()
        translateWindow.x = x
        translateWindow.y = y
        translateView.url = "http://dict.youdao.com/search?q=" + word
        console.log("**************", x, y, word)
    }
    
    function hideTranslate() {
        windowView.hide()
    }
    
    Rectangle {
        id: translateWindow
        anchors.fill: parent
        color: Qt.rgba(0, 0, 0, 0.8)
        width: 400
        height: 300
        radius: 3
        border.color: Qt.rgba(10, 10, 10, 0.5)
        
        Flickable {
            id: flickable
            anchors.fill: parent
            anchors.topMargin: 10
            anchors.bottomMargin: 10
            anchors.leftMargin: 10
            anchors.rightMargin: 10
            
            WebView {
                id: translateView
                anchors.fill: parent
                url: ""
            }
        }
    }    
}
