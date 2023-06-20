package com.mltmaker.dynamodb.model

import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbBean
import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbPartitionKey


@DynamoDbBean
data class Audio(
    @get:DynamoDbPartitionKey
    var id: String? = null,
    var filepath: String? = null,
    var link: String? = null,
    var name: String? = null,
    var creator: String? = null,
    var youtube: Boolean? = null,
    var downloaded: Boolean? = null
)