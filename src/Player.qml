import QtQuick 2.1
import QtMultimedia 5.0

Audio {
    id: player
    
    property variant voices
    
	property int voiceIndex: 0
	property bool isManualStop: false
    
    onStopped: {
        if (!isManualStop) {
            voiceIndex += 1
            if (voiceIndex <= voices.length) {
                if (voices[voiceIndex] != undefined) {
                    player.source = voices[voiceIndex]
                    player.play()
                }
            } else {
                voiceIndex = 0
            }
        }
    }
    
    function stopAudio() {
        isManualStop = true
        voiceIndex = 0
        player.stop()
        isManualStop = false
    }
    
    function playAudio() {
        isManualStop = true
        voiceIndex = 0
        player.stop()
        player.source = voices[voiceIndex]
        player.play()
        isManualStop = false
    }
    
    function autoplayAudio() {
        if (settingConfig.get_trayicon_config("toggle_speech")) {
            playAudio()
        }
    }
}