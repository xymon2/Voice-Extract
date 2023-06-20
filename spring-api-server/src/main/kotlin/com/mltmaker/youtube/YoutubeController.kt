package com.mltmaker.youtube

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController;

data class TestRequest(val test: String, val test2: String)

@RestController
class YoutubeController {
    @GetMapping("/youtubes")
    fun getHello(): String {
        return "Hello World!"
    }

    @PostMapping("/youtubes")
    fun postHello(@RequestBody testRequest: TestRequest): String {
        println(testRequest.test)
        return "wtf"
    }
}