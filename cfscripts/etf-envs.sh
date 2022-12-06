#!/bin/bash

if [ $1 ]; then
    CF_SPACE=$1
fi

sentry_envs=(
    prod
    develop
    staging
    pentest
)
govuk_email_backend=(
    prod
    staging
    develop
    pentest
)

live_notify_api=(
    staging
)

if [[ " ${govuk_email_backend[*]} " =~ " ${CF_SPACE} " ]]; then
    gov_notify=true
fi

if [[ " ${sentry_envs[*]} " =~ " ${CF_SPACE} " ]]; then
    sentry=true
fi

if [[ " ${live_notify_api[*]} " =~ " ${CF_SPACE} " ]]; then
    live_api_key=true
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
    if grep -q "ellandi-api" <<< "$value"; then
        echo "Adding envs to: ${value}..........."
        if [ "$value" == "ellandi-api" ]; then
            $(./cf set-env ${value} DJANGO_SECRET_KEY ${PROD_DJANGO_SECRET_KEY} &> /dev/null)
        else
            $(./cf set-env ${value} DJANGO_SECRET_KEY ${DJANGO_SECRET_KEY} &> /dev/null)
        fi
        if [ $gov_notify ] || [ "$value" == "ellandi-api" ]; then
            if [ $live_api_key ] || [ "$value" == "ellandi-api" ]; then
                $(./cf set-env ${value} GOVUK_NOTIFY_API_KEY ${LIVE_NOTIFY_API_KEY} &> /dev/null)
            else
                $(./cf set-env ${value} GOVUK_NOTIFY_API_KEY ${TEAM_NOTIFY_API_KEY} &> /dev/null)
            fi

            $(./cf set-env ${value} EMAIL_BACKEND_TYPE GOVUKNOTIFY &> /dev/null)
            $(./cf set-env ${value} GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID ${NOTIFY_PLAIN_EMAIL_TEMPLATE_ID} &> /dev/null)
        else
            $(./cf set-env ${value} EMAIL_BACKEND_TYPE CONSOLE &> /dev/null)
        fi
        if [ $autoscale ]; then
            $(./cf set-env ${value} SENTRY_DSN ${SENTRY_DSN}  &> /dev/null)
            $(./cf set-env ${value} SENTRY_ENVIRONMENT ${CF_SPACE} &> /dev/null)
        fi
    elif grep -q "organogram" <<< "$value"; then
        echo "Adding organogram env to: ${value}..........."
        if [ "$value" == "digital-organogram" ]; then
            $(./cf set-env ${value} DJANGO_SECRET_KEY ${PROD_DJANGO_SECRET_KEY} &> /dev/null)
        else
            $(./cf set-env ${value} DJANGO_SECRET_KEY ${DJANGO_SECRET_KEY} &> /dev/null)
        fi
        $(./cf set-env ${value} EMAIL_BACKEND_TYPE CONSOLE &> /dev/null)
    elif grep -q "ellandi-${CF_SPACE}" <<< "$value"; then
        echo "Adding network policy to: ${value}..........."
        $(./cf add-network-policy ${value} ellandi-api-${CF_SPACE} --protocol tcp --port 8000 &> /dev/null)
    fi
done


for value in "${cfapps[@]}"
do
    echo "Starting ${value}....."
    $(./cf restage ${value} &> /dev/null)
done
