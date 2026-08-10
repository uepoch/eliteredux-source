# syntax=docker/dockerfile:1.7

ARG DEBIAN_IMAGE=debian:bookworm-slim
ARG BUILD_IMAGE=debian:trixie-slim

FROM ${DEBIAN_IMAGE} AS tool-downloads

ARG PORYSCRIPT_VERSION=3.5.2
ARG PORYSCRIPT_SHA256=cda085d4662b630a6645f33cf8773602821b35977ccaafbb02513b36008cdf5c
ARG PROTOC_VERSION=29.2
ARG PROTOC_SHA256=52e9e7ece55c7e30e7e8bbd254b4b21b408a5309bca826763c7124b696a132e9

RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl unzip \
 && rm -rf /var/lib/apt/lists/* \
 && curl -fsSL "https://github.com/huderlem/poryscript/releases/download/${PORYSCRIPT_VERSION}/poryscript-linux.zip" -o /tmp/poryscript.zip \
 && echo "${PORYSCRIPT_SHA256}  /tmp/poryscript.zip" | sha256sum -c - \
 && unzip -q /tmp/poryscript.zip -d /tmp \
 && mkdir -p /out/poryscript \
 && cp "/tmp/poryscript-linux/poryscript" "/tmp/poryscript-linux/command_config.json" "/tmp/poryscript-linux/font_config.json" /out/poryscript/ \
 && chmod 0755 /out/poryscript/poryscript \
 && curl -fsSL "https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOC_VERSION}/protoc-${PROTOC_VERSION}-linux-x86_64.zip" -o /tmp/protoc.zip \
 && echo "${PROTOC_SHA256}  /tmp/protoc.zip" | sha256sum -c - \
 && unzip -q /tmp/protoc.zip bin/protoc -d /out \
 && chmod 0755 /out/bin/protoc

FROM ${DEBIAN_IMAGE} AS vanilla-builder

ARG AGBCC_REF=da598c1d918402c42c0c0d7128ba14567f3175e9
ARG POKEEMERALD_REF=9a83a2bbe8e097e62c00f1dbd56849766775d7b6

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      binutils-arm-none-eabi \
      build-essential \
      ca-certificates \
      git \
      libpng-dev \
      pkg-config \
 && rm -rf /var/lib/apt/lists/*

RUN git init /src/pokeemerald \
 && git -C /src/pokeemerald remote add origin https://github.com/pret/pokeemerald.git \
 && git -C /src/pokeemerald fetch --depth 1 origin "${POKEEMERALD_REF}" \
 && git -C /src/pokeemerald checkout --detach FETCH_HEAD \
 && git init /src/agbcc \
 && git -C /src/agbcc remote add origin https://github.com/pret/agbcc.git \
 && git -C /src/agbcc fetch --depth 1 origin "${AGBCC_REF}" \
 && git -C /src/agbcc checkout --detach FETCH_HEAD \
 && cd /src/agbcc \
 && ./build.sh \
 && /src/agbcc/install.sh /src/pokeemerald \
 && make -C /src/pokeemerald -j"$(nproc)" \
 && cd /src/pokeemerald \
 && sha1sum -c rom.sha1

ARG FLIPS_REF=ff216a75df0987047a67d7923567dc4482ce07ac

RUN git init /src/flips \
 && git -C /src/flips remote add origin https://github.com/Alcaro/Flips.git \
 && git -C /src/flips fetch --depth 1 origin "${FLIPS_REF}" \
 && git -C /src/flips checkout -b master FETCH_HEAD \
 && make -C /src/flips -j"$(nproc)" TARGET=cli CFLAGS=-O3

FROM ghcr.io/astral-sh/uv:0.8.8 AS uv

FROM ${BUILD_IMAGE} AS build

ARG TARGETARCH
ARG PROTOBUF_VERSION=5.29.2

RUN test "${TARGETARCH}" = amd64 \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
      binutils-arm-none-eabi \
      build-essential \
      gcc-arm-none-eabi \
      libnewlib-arm-none-eabi \
      libpng-dev \
      libstdc++-arm-none-eabi-dev \
      pkg-config \
      python3 \
 && rm -rf /var/lib/apt/lists/*

RUN --mount=from=uv,source=/uv,target=/usr/local/bin/uv \
    UV_NO_CACHE=1 uv venv --python /usr/bin/python3 /opt/venv \
 && UV_NO_CACHE=1 uv pip install --python /opt/venv/bin/python "protobuf==${PROTOBUF_VERSION}"

COPY --from=tool-downloads /out/poryscript /opt/poryscript
COPY --from=tool-downloads /out/bin/protoc /usr/local/bin/protoc
COPY --from=vanilla-builder /src/pokeemerald/pokeemerald.gba /opt/pokeemerald.gba
COPY --from=vanilla-builder /src/flips/flips /usr/local/bin/flips
COPY docker/build-bps-in-container.sh /usr/local/bin/eliteredux-build

ENV PATH="/opt/venv/bin:${PATH}"
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/eliteredux-build"]
