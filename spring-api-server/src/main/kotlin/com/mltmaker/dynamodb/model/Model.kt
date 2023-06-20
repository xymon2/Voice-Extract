package com.mltmaker.dynamodb.model

import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbBean
import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbPartitionKey

@DynamoDbBean
data class Model(
    @get:DynamoDbPartitionKey
    var id: String? = null,
    var name : String? = null,
    var audioIds: Map<String, Number>? = null
)