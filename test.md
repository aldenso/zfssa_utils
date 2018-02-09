# Testing

All testing must run using a ZFSSA emulator/demo, based on OS86 and OS87, downloaded from Oracle Web Site.

## ZFSSA requirements to run tests

- ip, username and password like those in the file serverOS86.yml.
- pool: pool_0
- project: unittest, pool: pool_0
- lun: lun10, project: unittest, pool: pool_0
- filesystem: fs01, project: unittest, pool: pool_0

**Note**: Response times depends on your zfssa assigned resources.

- Testing Common.

```sh
python -m unittest -v test.test_zfssa
test_read_csv_file (test.test_zfssa.TestCommon)
Test read_csv_file function to read a regular csv file ... ok
test_read_csv_file_fail (test.test_zfssa.TestCommon)
Test read_csv_file function to read a file not in csv format ... expected failure
test_read_yaml_file (test.test_zfssa.TestCommon)
Test read_yaml_file function to read a regular yml file ... ok
test_read_yaml_file_fail (test.test_zfssa.TestCommon)
Test read_yaml_file function to read a file not in yml format. ... expected failure
test_response_size (test.test_zfssa.TestCommon)
Test response_size function to print human readable sizes ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.008s

OK (expected failures=2)
```

- Testing Projects.

```sh
python -m unittest --buffer -v test.test_projects
test_00_create_projects (test.test_projects.TestProjects)
Test projects with arguments to use create_projects function ... ok
test_01_list_projects (test.test_projects.TestProjects)
Test projects with arguments to use list_projects function ... ok
test_02_delete_projects (test.test_projects.TestProjects)
Test projects with arguments to use delete_projects function ... ok

----------------------------------------------------------------------
Ran 3 tests in 49.510s

OK
```

- Testing LUNS.

```sh
python -m unittest --buffer -v test.test_luns
test_00_create_lun (test.test_luns.TestLUNS)
Test luns with arguments to use create_lun function ... ok
test_01_list_lun (test.test_luns.TestLUNS)
Test luns with arguments to use list_lun function ... ok
test_02_delete_lun (test.test_luns.TestLUNS)
Test luns with arguments to use delete_lun function ... ok

----------------------------------------------------------------------
Ran 3 tests in 51.019s

OK
```

- Testing Snapshots.

```sh
python -m unittest --buffer -v test.test_snapshots
test_00_create_snap_project (test.test_snapshots.TestSnapshots)
Test snapshots with arguments to create a project snap. ... ok
test_01_list_snap_project (test.test_snapshots.TestSnapshots)
Test snapshots with arguments to list/show a project snap. ... ok
test_02_delete_snap_projects (test.test_snapshots.TestSnapshots)
Test snapshots with arguments to delete a project snap. ... ok
test_03_create_snap_filesystem (test.test_snapshots.TestSnapshots)
Test snapshots with arguments to create a filesystem snap. ... ok
test_04_list_snap_filesystem (test.test_snapshots.TestSnapshots)
Test snapshots with arguments to list/show a filesystem snap. ... ok
test_05_delete_snap_filesystem (test.test_snapshots.TestSnapshots)
Test snapshots with arguments to delete a filesystem snap. ... ok
test_06_create_snap_lun (test.test_snapshots.TestSnapshots)
Test snapshots with arguments to create a lun snap. ... ok
test_07_list_snap_lun (test.test_snapshots.TestSnapshots)
Test snapshots with arguments to list/show a lun snap. ... ok
test_08_delete_snap_lun (test.test_snapshots.TestSnapshots)
Test snapshots with arguments to delete a lun snap. ... ok

----------------------------------------------------------------------
Ran 9 tests in 64.694s

OK
```

- Testing Filesystems.

```sh
python -m unittest --buffer -v test.test_filesystems
test_00_create_filesystems (test.test_filesystems.TestFilesystems)
Test filesystems with args to use create_filesystems function ... ok
test_01_list_filesystems (test.test_filesystems.TestFilesystems)
Test filesystems with args to use list_filesystems function ... ok
test_02_delete_filesystems (test.test_filesystems.TestFilesystems)
Test filesystems with args to use delete_filesystems function ... ok

----------------------------------------------------------------------
Ran 3 tests in 33.022s

OK
```

## Run all tests for python 2 and python 3

Create 2 virtual environments, called venv and ENV.

```sh
virtualenv --python=python3.6 venv
virtualenv --python=python2.7 ENV
```

Install requirements.

```sh
source venv/bin/activate
pip install -r requirements.txt
deactivate
source ENV/bin/activate
pip install -r requirements.txt
deactivate
```

Then run the script **run_test.sh**.

```sh
./run_test.sh
```

## Testing with coverage

```sh
coverage run --source zfssa_utils -m unittest --buffer -v \
test.test_zfssa test.test_projects test.test_filesystems \
test.test_luns test.test_snapshots test.test_explorer
```

**TODO**: Include Docker to test more python versions.