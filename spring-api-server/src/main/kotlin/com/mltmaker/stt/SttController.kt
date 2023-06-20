package com.mltmaker.stt

import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController


@RestController
class SttController(private val sttService: SttService) {

    @PostMapping("/stt/{audioId}")
    suspend fun requestSttToAllClips(@PathVariable audioId: String): String {
        sttService.requestSttAllToGRPCServer(audioId)
        return "Success"
    }

    @PostMapping("/stt/{audioId}/results")
    suspend fun updateSttResultOfAllClips(@PathVariable audioId: String, @RequestBody sttResult:SttAllResultRequest): String {
        sttService.updateSttResultOfAllClips(audioId, sttResult.clipIdAndPathMap)
        return "Success"
    }
}

data class SttAllResultRequest(
    val clipIdAndPathMap : Map<String, String>
)
