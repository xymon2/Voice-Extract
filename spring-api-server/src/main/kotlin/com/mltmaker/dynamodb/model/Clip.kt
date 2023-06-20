package com.mltmaker.dynamodb.model

import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbBean
import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbPartitionKey
import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbSortKey

@DynamoDbBean
data class Clip(
    @get:DynamoDbPartitionKey
    var audioId: String = "",
    @get:DynamoDbSortKey
    var id: String = "",
    var filepath : String = "",
    var text : String? = null,
)