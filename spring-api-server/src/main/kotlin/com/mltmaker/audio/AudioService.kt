package com.mltmaker.audio

import com.mltmaker.dynamodb.model.Audio
import com.mltmaker.dynamodb.repository.AudioRepository
import org.springframework.stereotype.Service

@Service
class AudioService(private val audioGrpcClient: AudioGrpcClient, private val audioRepository: AudioRepository){
    suspend fun requestAudioDownloadFromYoutube(link:String): String {
        val audioId = audioGrpcClient.requestYoutubeDownload(link)

        audioId?.let{
//          TODO: reject if link is not unique using GSI
            val audio = Audio(
                id = audioId,
                link = link,
                youtube = true,
                downloaded = false
            )
            audioRepository.putItem(audio)
        }

        return audioId
    }


    suspend fun updateAudioData(audioId:String, name:String, creator:String, filepath:String): String {

        val audio = audioRepository.findById(audioId)

        audio?.let{
            audio.apply{
                it.name = name
                it.creator = creator
                it.filepath = filepath
                it.downloaded = true
            }
            audioRepository.updateItem(audio)
        }

        return "200"
    }
}