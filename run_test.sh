#!/bin/bash

SEP="##########################################################"

run_tests(){

    # test common
    python -m unittest -v test.test_zfssa

    # test projects
    python -m unittest --buffer -v test.test_projects

    # test luns
    python -m unittest --buffer -v test.test_luns

    # test snapshots
    python -m unittest --buffer -v test.test_snapshots
}

source venv/bin/activate
echo "$SEP"
echo "Running test for:"
python -V
echo "$SEP"
run_tests
deactivate
sleep 3
source ENV/bin/activate
echo "$SEP"
echo "Running test for:"
python -V
echo "$SEP"
run_tests
deactivate
