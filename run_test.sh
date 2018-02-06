#!/bin/bash

SEP1="##########################################################"
SEP2="**********************************************************"

warning(){
    echo "$SEP2"
    echo "WARNING: Failed some tests"
    echo "$SEP2"
}

run_tests(){
    # test common
    if [ "$(python -m unittest -v test.test_zfssa)" ]
    then
        warning
    fi

    # test projects
    if [ "$(python -m unittest --buffer -v test.test_projects)" ]
    then
        warning
    fi

    # test luns
    if [ "$(python -m unittest --buffer -v test.test_luns)" ]
    then
        warning
    fi

    # test snapshots
    if [ "$(python -m unittest --buffer -v test.test_snapshots)" ]
    then
        warning
    fi
}

source venv/bin/activate
echo "$SEP1"
echo "Running test for:"
python -V
echo "$SEP1"
run_tests
deactivate
sleep 3
source ENV/bin/activate
echo "$SEP1"
echo "Running test for:"
python -V
echo "$SEP1"
run_tests
deactivate
