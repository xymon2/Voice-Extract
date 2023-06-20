package com.mltmaker.dynamodb.repository

import com.mltmaker.dynamodb.model.Audio
import com.mltmaker.dynamodb.model.Clip
import kotlinx.coroutines.future.await
import org.springframework.stereotype.Repository
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbAsyncTable
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedAsyncClient
import software.amazon.awssdk.enhanced.dynamodb.Key
import software.amazon.awssdk.enhanced.dynamodb.TableSchema
import software.amazon.awssdk.enhanced.dynamodb.model.ScanEnhancedRequest
import software.amazon.awssdk.enhanced.dynamodb.model.UpdateItemEnhancedRequest

@Repository
class ClipRepository(private val dynamoDbAsyncClient: DynamoDbEnhancedAsyncClient){
    private val clipTable: DynamoDbAsyncTable<Clip> = dynamoDbAsyncClient.table("mlt-clip", TableSchema.fromBean(
        Clip::class.java))

    suspend fun putItem(clip: Clip):Void = clipTable.putItem(clip).await()
    suspend fun updateItem(clip: Clip):Clip? = clipTable.updateItem(clip).await()
    suspend fun findByClipIdAndAudioId(audioId:String, clipId:String): Clip = clipTable.getItem(
        Key.builder().partitionValue(audioId).sortValue(clipId).build()).await()
    suspend fun findAllByAudioId(audioId:String): List<Clip> {
        val scanRequest = ScanEnhancedRequest.builder().build()

        val clips = mutableListOf<Clip>()

        clipTable.scan(scanRequest)
            .items()
            .subscribe { item -> clips.add(item) }
            .await()

        return clips
    }

}