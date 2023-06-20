package com.mltmaker.vad

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

@RestController
class VadController(private val vadService: VadService) {

    @PostMapping("/vad/audios")
    suspend fun requestVad(@RequestBody vadRequest: VadRequest){
        val audioId = vadRequest.audioId
        val minDuration = vadRequest.minDuration
        val maxDuration = vadRequest.maxDuration

        vadService.requestVADtoGRPCServer(audioId, minDuration, maxDuration)

        return
    }

    @PostMapping("/vad/audios/{audioId}/results")
    suspend fun updateVadResult(@PathVariable audioId: String, @RequestBody vadResultRequest: VadResultRequest){
        val idPathMap = vadResultRequest.idPathMap

        vadService.updateVADResultAndInsertClipsToDb(audioId, idPathMap)

        return
    }


    @GetMapping("/vad/audios/{audioId}/models/{modelId}")
    suspend fun getVadResultOfAudioOfModel
                (@PathVariable audioId: String,
                 @PathVariable modelId: String,
                 @RequestBody vadResultRequest: VadResultRequest){
        val idPathMap = vadResultRequest.idPathMap
//        vadService.updateVADResultAndInsertClipsToDb(idPathMap)
    }
}

data class VadRequest(
    val audioId:String,
    val minDuration:Number,
    val maxDuration:Number
)

data class VadResultRequest (
    val idPathMap: Map<String, String>
)


