package com.mltmaker.vad

import com.mltmaker.library.proto.vad.VADGrpcKt
import com.mltmaker.library.proto.vad.VADProto.*
import io.grpc.ManagedChannel
import org.springframework.stereotype.Component

@Component
class VadGrpcClient(private val vadChannel: ManagedChannel) {
    private val vadStub: VADGrpcKt.VADCoroutineStub by lazy {
        VADGrpcKt.VADCoroutineStub(vadChannel)
    }

    suspend fun requestVAD(filePath:String, minDuration:Number, maxDuration:Number): String {
        val vadRequest = DetectRequest.newBuilder()
            .setFilepath(filePath)
            .setMinDuration(minDuration.toInt())
            .setMaxDuration(maxDuration.toInt())
            .build()

        val response = vadStub.detect(vadRequest)
        return response.status
    }


}