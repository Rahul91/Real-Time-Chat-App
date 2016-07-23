#!/usr/bin/env bash

print_help() {
  echo "Usage:
  ./migrate_db.sh
  Options:
    upgrade <no.>                       Ex: upgrade 1 will upgrade 1 revision
    downgrade <no.>                     Ex: downgrade 2 will downgrade 2 next revision
  "
}

print_help

if [[ $# > 0 ]]; then
  if [[ "$1" == "upgrade" ]] && [[ ! -z "$2" ]]; then
    (cd ../healthify/models && alembic -c ../../system_config/dev/alembic.ini  upgrade +"$2" )
  elif [[ "$1" == "downgrade" ]] && [[ ! -z "$2" ]]; then
    (cd ../healthify/models && alembic -c ../../system_config/dev/alembic.ini  downgrade -"$2" )
  fi
else
    (cd ../healthify/models && alembic -c ../../system_config/dev/alembic.ini upgrade head )
  exit 1
fi
