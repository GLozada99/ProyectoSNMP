#!/bin/bash

_snmpmonitor_completions()
{
  if [ "${#COMP_WORDS[@]}" != "2" ]; then
    return
  fi

  local IFS=$'\n'
  local suggestions=($(compgen -W "$(cat /home/pi/Documents/.Hidden/Help/.help | sed 's/\t//')" -- "${COMP_WORDS[1]}"))

  if [ "${#suggestions[@]}" == "1" ]; then
    local number="${suggestions[0]/%\ */}"
    COMPREPLY=("$number")
  else
    for i in "${!suggestions[@]}"; do
      suggestions[$i]="$(printf '%*s' "-$COLUMNS"  "${suggestions[$i]}")"
    done
  
    COMPREPLY=("${suggestions[@]}")
  fi
}

complete -F _snmpmonitor_completions snmpmonitor
