# Testing

All testing must run using a ZFSSA emulator/demo, based on OS86 and OS87, downloaded from Oracle Web Site.

## ZFSSA requirements to run tests

- pool: pool_0
- project: unittest, pool: pool_0
- lun: lun10, project: unittest, pool: pool_0
- filesystem: fs01, project: unittest, pool: pool_0

**Note**: Response times depends on your zfssa assigned resources.

* Testing Common.

```sh
python -m unittest test.test_zfssa -v
test_get_real_blocksize (test.test_zfssa.TestCommon)
Test get_real_blocksize function to convert a string to integer ... ok
test_get_real_size (test.test_zfssa.TestCommon)
Test get_real_size function to convert input sizes ... ok
test_read_csv_file (test.test_zfssa.TestCommon)
Test read_csv_file function to read a regular csv file ... ok
test_read_yaml_file (test.test_zfssa.TestCommon)
Test read_yaml_file function to read a regular yml file ... ok
test_response_size (test.test_zfssa.TestCommon)
Test response_size function to print human readable sizes ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.013s

OK
```

* Testing Projects.

```sh
python -m unittest test.test_projects --buffer -v
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

* Testing LUNS.

```sh
python -m unittest test.test_luns --buffer -v
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

* Testing Snapshots.

```sh
python -m unittest test.test_snapshots --buffer -v
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