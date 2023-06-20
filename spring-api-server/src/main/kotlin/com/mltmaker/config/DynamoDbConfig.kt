package com.mltmaker.config

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import software.amazon.awssdk.auth.credentials.AwsCredentialsProviderChain
import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider
import software.amazon.awssdk.auth.credentials.WebIdentityTokenFileCredentialsProvider
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedAsyncClient
import software.amazon.awssdk.regions.Region
import software.amazon.awssdk.services.dynamodb.DynamoDbAsyncClient

@Configuration
class DynamoDbConfig {



    @Bean
    fun dynamoDbAsyncClient(): DynamoDbEnhancedAsyncClient {
        val ddb = DynamoDbAsyncClient.builder()
            .region(Region.AP_NORTHEAST_2)
//            .credentialsProvider(WebIdentityTokenFileCredentialsProvider.create())
            .credentialsProvider(DefaultCredentialsProvider.create())
            .build()

        return DynamoDbEnhancedAsyncClient.builder().dynamoDbClient(ddb).build()
    }

}