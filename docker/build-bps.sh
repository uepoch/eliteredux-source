#!/bin/sh
set -eu

repository=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
engine=${DOCKER:-docker}
image=${DOCKER_IMAGE:-eliteredux-bps-build:local}
platform=${DOCKER_PLATFORM:-linux/amd64}

if ! command -v "${engine}" >/dev/null 2>&1; then
    echo "container engine not found: ${engine}" >&2
    exit 1
fi

"${engine}" build \
    --platform "${platform}" \
    --tag "${image}" \
    --file "${repository}/Dockerfile" \
    "${repository}"

tty=
if [ -t 0 ] && [ -t 1 ]; then
    tty=-it
fi

# The image is amd64 because the Poryscript 3.5.2 release is an amd64 executable.
# Docker transparently uses emulation on ARM hosts.
# shellcheck disable=SC2086
exec "${engine}" run ${tty} --rm --init \
    --platform "${platform}" \
    --user "$(id -u):$(id -g)" \
    --env BPS_OUTPUT \
    --env HOME=/tmp \
    --env JOBS \
    --mount "type=bind,source=${repository},target=/workspace" \
    "${image}" "${1:-bps}"
