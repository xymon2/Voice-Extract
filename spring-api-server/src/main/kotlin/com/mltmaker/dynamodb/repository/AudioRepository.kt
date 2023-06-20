package com.mltmaker.dynamodb.repository

import com.mltmaker.dynamodb.model.Audio
import kotlinx.coroutines.future.await
import org.springframework.stereotype.Repository
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbAsyncTable
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedAsyncClient
import software.amazon.awssdk.enhanced.dynamodb.Key
import software.amazon.awssdk.enhanced.dynamodb.TableSchema
import software.amazon.awssdk.enhanced.dynamodb.model.GetItemEnhancedRequest
import software.amazon.awssdk.enhanced.dynamodb.model.ScanEnhancedRequest

@Repository
class AudioRepository(private val dynamoDbAsyncClient: DynamoDbEnhancedAsyncClient){
    private val audioTable: DynamoDbAsyncTable<Audio> = dynamoDbAsyncClient.table("mlt-audio", TableSchema.fromBean(
        Audio::class.java))

    suspend fun findById(id:String): Audio? {
        val getAudioRequest = GetItemEnhancedRequest.builder()
            .key(Key.builder().partitionValue(id).build())
            .build()

        return audioTable.getItem(getAudioRequest).await()
    }

//    suspend fun findAll(): List<Audio> {
//        val scanRequest = ScanEnhancedRequest.builder().build()
//
//        val items = mutableListOf<Audio>()
//
//        audioTable.scan(scanRequest)
//            .items()
//            .subscribe { item -> items.add(item) }
//            .await()
//
//        return items
//    }

    suspend fun putItem(audio: Audio):Void = audioTable.putItem(audio).await()

    // update title column of audio table which has "audioId" as primary key
    suspend fun updateItem(audio: Audio):Audio? = audioTable.updateItem(audio).await()
}