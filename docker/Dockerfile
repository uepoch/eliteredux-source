# syntax=docker/dockerfile:1
#
# Runs the Kotlin codegen (tools/codegen) on proto/ and nothing else: no ARM toolchain,
# no ROM build. Used by .github/workflows/sync-proto.yml to check that a new er-config
# version still generates, without needing Java or Kotlin on the runner.
# Pinned, checksummed downloads, trimmed down from the Docker build in PR #13.
#
# Stages, from least to most often rebuilt:
#   fetch-*        pinned downloads (kotlinc, protoc, protobuf jars)
#   builder        JDK + make + perl + the tools above
#   codegen-jars   Kotlin codegen compiled from tools/codegen + proto/*.proto
#   codegen        generated headers; reruns on textproto edits without recompiling Kotlin
#   headers-artifact  scratch stage: the generated headers, for `--output type=local`

ARG DEBIAN_IMAGE=debian:bookworm-slim

FROM ${DEBIAN_IMAGE} AS fetch
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl unzip \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /dl

FROM fetch AS fetch-kotlin
ARG KOTLIN_VERSION=2.4.21
ARG KOTLIN_SHA256=7cc140e76daf416a0424a5557f99afd7ca89ebd463ea1101261e3e01c33e75cd
RUN curl -fsSL -o kotlin.zip "https://github.com/JetBrains/kotlin/releases/download/v${KOTLIN_VERSION}/kotlin-compiler-${KOTLIN_VERSION}.zip" \
 && echo "${KOTLIN_SHA256}  kotlin.zip" | sha256sum -c - \
 && unzip -q kotlin.zip -d /opt \
 && rm kotlin.zip

FROM fetch AS fetch-codegen-deps
# The exact files tools/codegen/makefile would otherwise download on every fresh checkout.
ARG PROTOC_VERSION=29.2
ARG PROTOC_SHA256=52e9e7ece55c7e30e7e8bbd254b4b21b408a5309bca826763c7124b696a132e9
ARG PROTOBUF_JAVA_VERSION=4.29.2
ARG PROTOBUF_JAVA_SHA256=7441a6394dca477b3f8b7c86f17bef035f705a8aaa11f53065d380300158177c
ARG PROTOBUF_KOTLIN_SHA256=2fbdd6977f446b1030fbdc2eb083d8eb54b41cdc854bfba996245e4b68c9152e
RUN mkdir -p /opt/codegen-deps \
 && curl -fsSL -o protoc.zip "https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOC_VERSION}/protoc-${PROTOC_VERSION}-linux-x86_64.zip" \
 && echo "${PROTOC_SHA256}  protoc.zip" | sha256sum -c - \
 && unzip -p protoc.zip bin/protoc > /opt/codegen-deps/protoc \
 && chmod 0755 /opt/codegen-deps/protoc \
 && cp protoc.zip /opt/codegen-deps/protoc.zip \
 && curl -fsSL -o /opt/codegen-deps/protobuf-java.jar "https://repo1.maven.org/maven2/com/google/protobuf/protobuf-java/${PROTOBUF_JAVA_VERSION}/protobuf-java-${PROTOBUF_JAVA_VERSION}.jar" \
 && curl -fsSL -o /opt/codegen-deps/protobuf-kotlin.jar "https://repo1.maven.org/maven2/com/google/protobuf/protobuf-kotlin/${PROTOBUF_JAVA_VERSION}/protobuf-kotlin-${PROTOBUF_JAVA_VERSION}.jar" \
 && echo "${PROTOBUF_JAVA_SHA256}  /opt/codegen-deps/protobuf-java.jar" | sha256sum -c - \
 && echo "${PROTOBUF_KOTLIN_SHA256}  /opt/codegen-deps/protobuf-kotlin.jar" | sha256sum -c -

FROM ${DEBIAN_IMAGE} AS builder
RUN apt-get update \
 && apt-get install -y --no-install-recommends make openjdk-17-jdk-headless perl \
 && rm -rf /var/lib/apt/lists/* /usr/lib/jvm/*/jmods
COPY --from=fetch-kotlin /opt/kotlinc /opt/kotlinc
COPY --from=fetch-codegen-deps /opt/codegen-deps /opt/codegen-deps
ENV PATH=/opt/kotlinc/bin:${PATH}
WORKDIR /src

FROM builder AS codegen-jars
# Only the Kotlin sources and .proto schemas: data (.textproto) edits don't recompile Kotlin.
COPY tools/codegen/makefile tools/codegen/
COPY tools/codegen/src/ tools/codegen/src/
COPY proto/*.proto proto/
COPY proto/google/ proto/google/
RUN cp -p /opt/codegen-deps/* tools/codegen/ \
 && make -C tools/codegen codegen.jar codegenkt.jar preproc.jar

FROM codegen-jars AS codegen
# The generators also read the font width tables (text wrapping).
COPY graphics/fonts/*_latin_widths.inc graphics/fonts/
COPY proto/ proto/
RUN make -C tools/codegen -j"$(nproc)"

FROM scratch AS headers-artifact
COPY --from=codegen /src/include/generated/ /include/generated/
COPY --from=codegen /src/asm/generated/ /asm/generated/
