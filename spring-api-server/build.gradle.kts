import org.jetbrains.kotlin.gradle.tasks.KotlinCompile
import com.google.protobuf.gradle.*

group = "com.mlt-maker"
version = "0.0.1-SNAPSHOT"
java.sourceCompatibility = JavaVersion.VERSION_17

buildscript {
	dependencies {
		classpath("com.google.protobuf:protobuf-gradle-plugin:0.9.3")
	}
}

plugins {
	id("org.springframework.boot") version "3.1.0"
	id("io.spring.dependency-management") version "1.1.0"
	kotlin("jvm") version "1.8.21"
	kotlin("plugin.spring") version "1.8.21"
	id("com.google.protobuf") version "0.9.3"
}

repositories {
	mavenCentral()
}

val kotlinXCoroutineVersion = "1.6.4"
val kotlinXSerializationVersion = "1.5.1"
val grpcVersion = "1.55.1"
val protobufVersion = "3.23.2"
val grpcKotlinVersion = "1.3.0"

dependencies {

	// Kotlin
	implementation("org.jetbrains.kotlin:kotlin-reflect")
	implementation ("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
	implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:$kotlinXCoroutineVersion")
	implementation("org.jetbrains.kotlinx:kotlinx-coroutines-jdk8:$kotlinXCoroutineVersion")
	implementation("org.jetbrains.kotlinx:kotlinx-coroutines-reactor:$kotlinXCoroutineVersion")
	implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:$kotlinXSerializationVersion")
	implementation("io.projectreactor.kotlin:reactor-kotlin-extensions:1.2.2")
	testImplementation("io.projectreactor:reactor-test:3.5.6")
	testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:$kotlinXCoroutineVersion")

	// Spring
	annotationProcessor("org.springframework.boot:spring-boot-configuration-processor")
	implementation("org.springframework:spring-context")
	implementation("org.springframework.boot:spring-boot-starter-actuator")
	implementation("org.springframework.boot:spring-boot-starter-webflux")
	testImplementation("org.springframework.boot:spring-boot-starter-test")

	// Armeria
	implementation(platform("com.linecorp.armeria:armeria-bom:1.19.0"))
	implementation(platform("io.netty:netty-bom:4.1.79.Final"))
	implementation("com.linecorp.armeria:armeria-kotlin")
	implementation("com.linecorp.armeria:armeria-spring-boot2-webflux-starter")
	testImplementation("com.ninja-squad:springmockk:3.1.1")

	//GRPC
	implementation("com.linecorp.armeria:armeria-grpc-protocol")
	implementation("com.linecorp.armeria:armeria-grpc")
	implementation("com.google.protobuf:protobuf-java:${protobufVersion}")
	implementation("com.google.protobuf:protobuf-kotlin:${protobufVersion}")
	implementation("io.grpc:grpc-protobuf:${grpcVersion}")
	implementation("io.grpc:grpc-stub:${grpcVersion}")
	implementation("io.grpc:grpc-netty-shaded:${grpcVersion}")
	api("io.grpc:grpc-kotlin-stub:${grpcKotlinVersion}")

//	implementation("org.springframework.boot:spring-boot-starter-web")
//	implementation("org.springframework.boot:spring-boot-starter-web-services")
//	implementation("org.springframework.boot:spring-boot-starter")
//	implementation("org.springframework.boot:spring-boot-starter-data-rest")
//	implementation("org.springframework.boot:spring-boot-starter-data-jpa")


	//AWS
	implementation(platform("software.amazon.awssdk:bom:2.20.78"))
	implementation("software.amazon.awssdk:dynamodb-enhanced")
	implementation("software.amazon.awssdk:s3")
	implementation("net.logstash.logback:logstash-logback-encoder:6.6")

}

tasks.withType<KotlinCompile> {
	kotlinOptions {
		freeCompilerArgs = listOf("-Xjsr305=strict")
		jvmTarget = "17"
	}
}

tasks.withType<Test> {
	useJUnitPlatform()
}

protobuf {
	protoc {
		artifact = "com.google.protobuf:protoc:${protobufVersion}"
	}
	plugins {
		id("grpc") {
			artifact = "io.grpc:protoc-gen-grpc-java:${grpcVersion}"
		}
		id("grpckt") {
			artifact = "io.grpc:protoc-gen-grpc-kotlin:${grpcKotlinVersion}:jdk8@jar"
		}
	}
	generateProtoTasks {
		all().forEach {
			it.plugins {
				id("grpc")
				id("grpckt")
			}
			it.builtins {
				id("kotlin")
			}
		}
	}
	sourceSets{
		main{
			proto {
				srcDir("../proto")
			}
			java {
				srcDir("build/generated/source/proto/main/java")
				srcDir("build/generated/source/proto/main/kotlin")
			}
		}
	}
}
