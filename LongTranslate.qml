import QtQuick 2.1
import QtMultimedia 5.0

Rectangle {
	id: container
    radius: 6
    color: "#AA000000"
	border { 
        width: 1
        color: "#AAFFFFFF"
    }
    
    property int borderMarin: 10
    property int textMargin: 10
    
    width: 300
    height: 200
    
	Rectangle {
        id: border
        radius: 6
	    anchors.fill: parent
		anchors.margins: borderMarin
        color: "#EEFFFFFF"
        
	    Column {
		    spacing: 10
		    anchors.fill: parent
		    anchors.margins: textMargin
		    
		    TextEdit { 
                id: trans
			    text: googleinfo.translate
                textFormat: TextEdit.RichText
			    wrapMode: TextEdit.Wrap
			    selectByMouse: true
			    font { pixelSize: 12 }
			    color: "#333333"
                width: parent.width
                
                onTextChanged: {
                    cursorPosition: 0
                    cursorVislble: false
                }
		    }		
	    }        
	}
}
