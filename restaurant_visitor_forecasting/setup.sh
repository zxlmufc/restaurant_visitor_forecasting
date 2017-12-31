#!/usr/bin/env bash


setup_project_directory(){

    echo "Setting up project $1"

    if [ -d $1 ]

    then

        cd $1
        mkdir -p {resources/{raw,cache,configuration,data/{target,feature,prediction,schema,train_output}},models,eda,preparation,documentation}
        echo "Setting up completed!"

        tree $1

    else
        echo "Project root does not exist!"
    fi

}

setup_project_directory "/home/xiaolan/project/private/contest/restaurant_visitor_forecasting/"
