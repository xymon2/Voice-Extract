package com.mltmaker.stt

import io.grpc.ManagedChannel
import com.mltmaker.library.proto.stt.STTGrpcKt
import com.mltmaker.library.proto.stt.STTProto.*
import org.springframework.stereotype.Component

@Component
class SttGrpcClient(private val sttChannel: ManagedChannel) {
    private val sttStub: STTGrpcKt.STTCoroutineStub by lazy {
        STTGrpcKt.STTCoroutineStub(sttChannel)
    }


    suspend fun requestSTTonAllClips(audioId:String,clipIdAndPathMap:Map<String,String>): String {
        val sttRequest = TranslateAllRequest.newBuilder()
            .setAudioId(audioId)
            .putAllClipIdsAndPaths(clipIdAndPathMap)
            .build()

        return sttStub.translateAll(sttRequest).status
    }
}