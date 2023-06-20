package com.mltmaker.audio

import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

@RestController
class AudioController(private val audioService: AudioService) {

    @PostMapping("/audios/youtubes")
    suspend fun requestAudioDownload(link:String):String{
        return audioService.requestAudioDownloadFromYoutube(link)
    }

    @PostMapping("/audios/{audioId}/results")
    suspend fun updateAudioData(@PathVariable audioId: String, @RequestBody audioData:RequestAudioDataUpdate):String{
        return audioService.updateAudioData(audioId, audioData.name, audioData.creator, audioData.filepath)
    }

}

data class RequestAudioDataUpdate(
    val name:String,
    val creator:String,
    val filepath:String
)