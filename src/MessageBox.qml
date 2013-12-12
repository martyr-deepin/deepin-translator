import QtQuick 2.1
import "./widgets"

WindowFrame {
    id: window
    
    property int defaultWidth: 300
    property int defaultHeight: 200
    
    Component.onCompleted: {
        windowView.width = defaultWidth
        windowView.height = defaultHeight
        windowView.x = (screenWidth - defaultWidth) / 2
        windowView.y = (screenHeight - defaultHeight) / 2
    }
    
    Column {
        anchors.fill: parent
        
        Text {
            text: "需要安装 sdcv 以开启星际译王翻译功能"
        }
        
        Row {
            DTextButton {
                text: "取消"
            }

            DTextButton {
                text: "安装"
            }
        }
    }
}