#!/bin/bash

set -euo pipefail


if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Use serve, scheduler or stats-fetcher."
    exit 1
fi


case "$1" in
    serve)
        shift
        echo "Starting api server on ${wbmp_redis_stat_host}:${wbmp_redis_stat_port}"
        export wbmp_redis_stat=src-serve
        python -m src serve
        ;;
    -*|--*=) # unsupported flags
        echo "ERROR::Unsupported flag $1"
        exit 1
        ;;
    *) # preserve positional arguments
        echo "ERROR::Unsupported flag $1"
        exit 1
        ;;
esac
