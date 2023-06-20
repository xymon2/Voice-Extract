package com.mltmaker.vad

import com.mltmaker.dynamodb.model.Clip
import com.mltmaker.dynamodb.repository.AudioRepository
import com.mltmaker.dynamodb.repository.ClipRepository
import org.springframework.stereotype.Service

@Service
class VadService(private val vadGrpcClient: VadGrpcClient,
                 private val audioRepository: AudioRepository,
                 private val clipRepository: ClipRepository) {

    suspend fun requestVADtoGRPCServer(audioId:String, minDuration:Number, maxDuration:Number): String {

        val audio = audioRepository.findById(audioId)
        audio?.let{
            val filepath = it.filepath
            requireNotNull(filepath) { "Filepath is null." }
            return vadGrpcClient.requestVAD(filepath, minDuration, maxDuration)
        }

         return "error"
    }

    suspend fun updateVADResultAndInsertClipsToDb(audioId:String,idAndClipIds:Map<String,String>):String{
//        TODO: reject if audioId does not exist.
        val filepath = audioRepository.findById(audioId)?.filepath

        for (entry in idAndClipIds.entries) {
            val clipId = entry.key
            val text = entry.value

            val clip = Clip().apply {
                this.id = clipId
                this.audioId = audioId
                this.text = text
                this.filepath = "${filepath}/clips/${clipId}.wav"
            }
            clipRepository.putItem(clip)
        }

        return "200"
    }


}