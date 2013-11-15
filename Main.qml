import QtQuick 2.1

Rectangle {
	id: container
	
	width: 300; height: 200
	
	Rectangle {
		border { width: 1; color: "#d3d3d3"}
		anchors.fill: parent
		anchors.margins: 1
        color: Qt.rgba(0.9, 0.9, 0.9, 0.8)
	}
	
	Column {
		
		/* anchors.fill: parent */
		spacing: 10
		anchors.margins: 5
		anchors.fill: parent
		
		Text { 
			id: keyword
			text: simpleinfo.keyword
			font { pixelSize: 30; bold: true }
			color: "#0066AA"
		}
		
		Row {
			spacing: 10
			
			Speech { text: simpleinfo.ukphone }
			Speech { text: simpleinfo.usphone }			
		}
		
		TextEdit { 
			text: simpleinfo.trans
			wrapMode: TextEdit.Wrap
			selectByMouse: true
			font { pixelSize: 12 }
			color: "#636363"
		}		
		
		TextEdit {
			text: simpleinfo.webtrans
			wrapMode: TextEdit.Wrap
			selectByMouse: true
			font { pixelSize: 12 }
			color: "#636363"
		}
		
	}
	
}