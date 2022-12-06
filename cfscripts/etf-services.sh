#!/usr/bin/env bash

if [ $1 ]; then
    CF_SPACE=$1
fi

autoscale_envs=(
    prod
    develop
    staging
    pentest
)

unencrypted_dbs_envs=(
    develop
    sandbox
    demo
    temp
)

buckets=()

autoscalers=(
    scale-etf-${CF_SPACE}
)

dbs=(
    etf-postgres-${CF_SPACE}
)

#################################### Set Envs and Services above this line only #################################


if [[ " ${autoscale_envs[*]} " =~ " ${CF_SPACE} " ]]; then
    autoscale=true
fi
if [[ " ${unencrypted_dbs_envs[*]} " =~ " ${CF_SPACE} " ]]; then
    unencrypted=true
fi

printf "Checking etf services in the ${CF_SPACE} environment... \n "

while read -r line; do
svcs=$(echo $line | head -n1 | cut -d " " -f1)
if [ "$svcs" != "Getting" ] && [ "$svcs" != "name" ] && [ "$svcs" ]; then
    cfservices+=($svcs)
fi
done < <(./cf services)

needed_svcs=(`echo ${buckets[@]}  ${dbs[@]} ${autoscalers[@]} `)

newservice=(`echo ${cfservices[@]}  ${cfservices[@]} ${needed_svcs[@]} | tr ' ' '\n' | sort | uniq -u `)


# Create new services that don't already exist
for value in "${newservice[@]}"
do
    if grep -q "postgres" <<< "$value"; then
        echo "Adding service ${value}..........."
        echo "Start Time: `date +%H:%M:%S`"
        if [ $unencrypted_dbs_envs ]; then
            $(./cf create-service postgres tiny-unencrypted-13 $value &> /dev/null)
        else
            $(./cf create-service postgres medium-13 $value &> /dev/null)
        fi
    elif grep -q "scale" <<< "$value" && [ $autoscale ]; then
        echo "Adding service ${value}..........."
        $(./cf create-service autoscaler autoscaler-free-plan $value &> /dev/null)
    elif grep -q "i-dot-ai" <<< "$value"; then
        echo "Adding service ${value}..........."
        $(./cf create-service aws-s3-bucket default $value -c '{"public_bucket":false}' &> /dev/null)
    fi
done

# Monitor and finish only when new DBs are created or timeout and fail
for value in "${newservice[@]}"
do
    if grep -q "postgres" <<< "$value"; then
        newdb+=($value)
    fi
done

echo "NEW DBs are: ${newdb[@]}"
count=${#newdb[@]}

end=$((SECONDS+900))

for value in ${newdb[@]};
do
    if grep -q "postgres" <<< "$value"; then
        printf "Waiting for Postgres services to be created........ \n"
        while [ "${count}" -gt 0 ] && [ "${SECONDS}" -lt "${end}" ];
        do
            for postgres_svc in ${newdb[@]}; do
                sleep 5
                SERVICE_STATE="$(./cf curl "/v3/service_instances?type=managed&names=${postgres_svc}" | jq -r '.resources[0].last_operation.state')"
                echo "DB service creation of '${postgres_svc}' ${SERVICE_STATE}......."
                if [ "${SERVICE_STATE}" == "succeeded" ]; then
                    newdb=( "${newdb[@]/$postgres_svc}" )
                    ((count -= 1 ))
                fi
            if [ "${SECONDS}" -gt "${end}" ]; then
                echo "The service creation timed out"
                exit 1
            fi
            done

        done
        echo "DB Services ready at: `date +%H:%M:%S`"
    fi
done

printf "All services created........ \n"
