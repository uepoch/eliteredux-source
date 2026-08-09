#!/bin/sh
set -eu

workspace=${WORKSPACE:-/workspace}
jobs=${JOBS:-$(nproc)}

if [ ! -f "${workspace}/Makefile" ]; then
    echo "Elite Redux source is not mounted at ${workspace}" >&2
    exit 1
fi

cd "${workspace}"

case "${1:-bps}" in
    bps)
        make -j"${jobs}" tools
        make -j"${jobs}" PORYSCRIPT_DIR=/opt/poryscript
        flips --create /opt/pokeemerald.gba pokeemerald_modern.gba "${BPS_OUTPUT:-EliteRedux.bps}"
        ;;
    codegen)
        make -C tools/codegen PYTHON=python3 regenerate
        ;;
    protos)
        make -C tools/codegen PYTHON=python3 PROTOC=/usr/local/bin/protoc protos
        ;;
    check-protos)
        make -C tools/codegen PYTHON=python3 PROTOC=/usr/local/bin/protoc check-protos
        ;;
    test-codegen)
        make -C tools/codegen PYTHON=python3 test
        ;;
    shell)
        exec /bin/bash
        ;;
    *)
        echo "usage: eliteredux-build {bps|codegen|protos|check-protos|test-codegen|shell}" >&2
        exit 2
        ;;
esac
