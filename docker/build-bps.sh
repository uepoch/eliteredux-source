#!/bin/sh
set -eu

repository=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
engine=${DOCKER:-docker}
image=${DOCKER_IMAGE:-eliteredux-bps-build:local}
platform=${DOCKER_PLATFORM:-linux/amd64}

usage() {
    cat <<'EOF'
usage: docker/build-bps.sh [--rom|--bps|--codegen|--protos|--check-protos|--test-codegen|--shell]

  --rom           build pokeemerald_modern.gba
  --bps           build the ROM and EliteRedux.bps (default)
  --codegen       regenerate generated C headers
  --protos        regenerate committed Python protobuf bindings
  --check-protos  verify committed Python protobuf bindings
  --test-codegen  run the Python codegen tests
  --shell         open a shell in the build container
EOF
}

case "${1:---bps}" in
    --rom|rom) action=rom ;;
    --bps|bps) action=bps ;;
    --codegen|codegen) action=codegen ;;
    --protos|protos) action=protos ;;
    --check-protos|check-protos) action=check-protos ;;
    --test-codegen|test-codegen) action=test-codegen ;;
    --shell|shell) action=shell ;;
    --help|-h) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
esac

if [ "$#" -gt 1 ]; then
    usage >&2
    exit 2
fi

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
    "${image}" "${action}"
