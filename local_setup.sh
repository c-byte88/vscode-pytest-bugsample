
#!/usr/bin/env bash
HOST="https://westeurope.azuredatabricks.net/"
TOKEN=""
CLUSTERID=""
ORGID=""
PORT="8787"

function exit_message () {
    echo "Press Enter to close the terminal"                     
    read line
    exit 0 
    }

function render_template() {
  eval "echo \"$(cat $1)\""
}

function generate_databricks_connect {
  echo "Populating [.databricks-connect]"
  render_template .databricks-connect.tmpl > .databricks-connect
}


function configure_db_connect {
    echo 'Enter the following paramerters to configure local databricks connect'
    echo -n "Workspace personal access token:"   
    read TOKEN
    echo -n "Dev ClusterID:"   
    read CLUSTERID
    echo -n "Dev Orgid:"   
    read ORGID
    generate_databricks_connect
}

cd ./docker/dbrks_dev/

declare dbconfig=$(<.databricks-connect)
if [[ $dbconfig = *"\"token\": "* && $dbconfig = *"\"cluster_id\": "* && $dbconfig = *"\"org_id\": "* ]]
  then
  echo "File [.databricks-connect] is already configured"
  echo "Do you want to re-configure? (Y/N)"
  read CONTINUE
  if [ $CONTINUE = "Y" ]
    then configure_db_connect
  fi
  else
  configure_db_connect
fi

dockerup=$( docker stats --no-stream )

if ! [[ -n "$dockerup" ]]; 
 then
  echo "Please Start docker on your machine"
  exit_message
fi

built=$( docker images -q "dbrks_dev*" )

if [[ -n "$built" ]]; 
then
  echo "Dev Container is already built."
  echo "Do you want to re-build? (Y/N)"
  read CONTINUE
  if [ $CONTINUE = "Y" ]
    then docker-compose --env-file ../../.env up --build -d 
    echo "Prune old image"
    docker image prune -f
    else
      docker-compose --env-file ../../.env up -d
  fi
else
  docker-compose --env-file ../../.env up -d  
fi

#copy vs code settings for remote container connection
echo
echo "Copying container settings"
d=~/AppData/Roaming/Code/User/globalStorage/ms-vscode-remote.remote-containers/nameConfigs/
mkdir -p "$d" && yes | cp dbrks_dev_local.json  "$d" -v
echo
#docker-compose down

#docker-compose start

#docker-compose stop
echo "Container created, please attach vscode to running container /dbrks_dev_local"
echo
docker images

echo
echo "Creating dev packages for notebooks"
cd ..; cd ..; cd ./src/python/project/ 
pip install -e .
echo

exit_message