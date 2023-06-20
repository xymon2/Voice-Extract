package com.mltmaker.stt

import com.mltmaker.dynamodb.repository.ClipRepository
import org.springframework.stereotype.Service

@Service
class SttService(private val sttGrpcClient: SttGrpcClient,
    private val clipRepository: ClipRepository) {

    suspend fun requestSttAllToGRPCServer(audioId:String): String {

        val clips = clipRepository.findAllByAudioId(audioId)

        val clipIdsAndPathsMap = mutableMapOf<String,String>()
        for (clip in clips) {
            clipIdsAndPathsMap[clip.id] = clip.filepath
        }

        return sttGrpcClient.requestSTTonAllClips(audioId,clipIdsAndPathsMap)
        return ""
    }

    suspend fun updateSttResultOfAllClips(audioId:String, idAndTextMap:Map<String,String>){

        for (entry in idAndTextMap.entries) {
            val clipId = entry.key
            val text = entry.value
            val clip = clipRepository.findByClipIdAndAudioId(audioId, clipId)
            clip.let{
                it?.text = text
                clipRepository.updateItem(it)
            }
        }

        return
    }
}