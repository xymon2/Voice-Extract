package com.mltmaker.config

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder

@Configuration
class GrpcConfiguration {
    @Bean
    fun vadChannel(): ManagedChannel {
        return ManagedChannelBuilder.forAddress("15.165.161.1", 8001)
            .usePlaintext()
            .build()
    }

    @Bean
    fun sttChannel(): ManagedChannel {
        return ManagedChannelBuilder.forAddress("15.165.161.1", 8002)
            .usePlaintext()
            .build()
    }

    @Bean
    fun audioDownloaderChannel(): ManagedChannel {
        return ManagedChannelBuilder.forAddress("15.165.161.1", 8003)
            .usePlaintext()
            .build()
    }
}