package com.mltmaker

import com.mltmaker.config.AccessLoggingFilter
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.cache.annotation.EnableCaching
import org.springframework.context.annotation.Bean
import org.springframework.scheduling.annotation.EnableScheduling

@EnableScheduling
@EnableCaching
@SpringBootApplication
class BelugaApplication{
	@Bean
	fun accessLoggingFilter(): AccessLoggingFilter {
		return AccessLoggingFilter()
	}
	companion object {
		@JvmStatic
		fun main(args: Array<String>) {
			println("Hello World!")
			runApplication<BelugaApplication>(*args)
		}
	}
}

