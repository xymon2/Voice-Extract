package com.mltmaker.config

import org.slf4j.LoggerFactory
import org.springframework.core.io.buffer.DataBuffer
import org.springframework.core.io.buffer.DataBufferFactory
import org.springframework.core.io.buffer.DataBufferUtils
import org.springframework.http.server.reactive.ServerHttpRequestDecorator
import org.springframework.web.server.ServerWebExchange
import org.springframework.web.server.WebFilter
import org.springframework.web.server.WebFilterChain
import reactor.core.publisher.Flux
import reactor.core.publisher.Mono
import java.nio.charset.StandardCharsets
import kotlinx.serialization.json.Json
class AccessLoggingFilter : WebFilter {

    private val logger = LoggerFactory.getLogger("accessLogger")
    private val json = Json { prettyPrint = false }
    override fun filter(exchange: ServerWebExchange, chain: WebFilterChain): Mono<Void> {
        val request = exchange.request
        val cachedBody = cacheRequestBody(exchange)

        val decoratedRequest = object : ServerHttpRequestDecorator(request) {
            override fun getBody(): Flux<DataBuffer> {
                return cachedBody
            }
        }

        return chain.filter(exchange.mutate().request(decoratedRequest).build())
    }

    private fun cacheRequestBody(exchange: ServerWebExchange): Flux<DataBuffer> {
        val request = exchange.request
        val bufferFactory: DataBufferFactory = exchange.response.bufferFactory()

        return DataBufferUtils.join(request.body)
            .flatMapMany { dataBuffer: DataBuffer ->
                val bytes = ByteArray(dataBuffer.readableByteCount())
                dataBuffer.read(bytes)
                DataBufferUtils.release(dataBuffer)
                val requestBody = String(bytes, StandardCharsets.UTF_8)

                // Parse the request body as a JSON object and make in one line string
                val jsonObject = json.parseToJsonElement(requestBody)
                val oneLineRequestBody = jsonObject.toString()

                logger.info("Access - Method: ${request.method}, URI: ${request.uri}, Request Body: $oneLineRequestBody")

                Flux.just(bufferFactory.wrap(bytes))
            }
    }
}
