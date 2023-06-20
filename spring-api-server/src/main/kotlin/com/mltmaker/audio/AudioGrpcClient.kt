package com.mltmaker.audio

import io.grpc.ManagedChannel
import com.mltmaker.library.proto.audio.AudioServiceGrpcKt
import com.mltmaker.library.proto.audio.AudioProto.*
import org.springframework.stereotype.Component
@Component
class AudioGrpcClient(private val audioDownloaderChannel: ManagedChannel) {
    private val audioStub: AudioServiceGrpcKt.AudioServiceCoroutineStub by lazy {
        AudioServiceGrpcKt.AudioServiceCoroutineStub(audioDownloaderChannel)
    }


    suspend fun requestYoutubeDownload(link:String):String{
        val audioRequest = DownloadYoutubeRequest.newBuilder()
            .setLink(link)
            .build()
        return audioStub.downloadYoutube(audioRequest).audioId
    }

}