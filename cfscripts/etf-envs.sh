#!/bin/bash

if [ $1 ]; then
    CF_SPACE=$1
fi

while read -r line; do
apps=$(echo $line | head -n1 | cut -d " " -f1)
if [ "$apps" != "Getting" ] && [ "$apps" != "name" ] && [ "$apps" ]; then
    cfapps+=($apps)
fi
done < <(./cf apps)

#remove proxy apps
for value in "${cfapps[@]}"
do
    if grep -q "proxy" <<< "$value"; then
        cfapps=("${cfapps[@]/$value}")
    fi
done

#Apply required variables
for value in "${cfapps[@]}"
do
    if grep -q "etf" <<< "$value"; then
        echo "Adding envs to: ${value}..........."
        if [ "$value" == "etf" ]; then
            $(./cf set-env ${value} DJANGO_SECRET_KEY ${PROD_DJANGO_SECRET_KEY} &> /dev/null)
        else
            $(./cf set-env ${value} DJANGO_SECRET_KEY ${DJANGO_SECRET_KEY} &> /dev/null)
        fi
    fi
done


for value in "${cfapps[@]}"
do
    if grep -q "etf" <<< "$value"; then
        echo "Starting ${value}....."
        $(./cf restage ${value} &> /dev/null)
    fi
done
