# CMake generated Testfile for 
# Source directory: /home/miguel/ws_moveit/src/pr2_common/pr2_description
# Build directory: /home/miguel/ws_moveit/build/pr2_description
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_pr2_description_gtest_test_urdf "/home/miguel/ws_moveit/build/pr2_description/catkin_generated/env_cached.sh" "/usr/bin/python" "/opt/ros/kinetic/share/catkin/cmake/test/run_tests.py" "/home/miguel/ws_moveit/build/pr2_description/test_results/pr2_description/gtest-test_urdf.xml" "--working-dir" "/home/miguel/ws_moveit/src/pr2_common/pr2_description" "--return-code" "/home/miguel/ws_moveit/devel/.private/pr2_description/lib/pr2_description/test_urdf --gtest_output=xml:/home/miguel/ws_moveit/build/pr2_description/test_results/pr2_description/gtest-test_urdf.xml")
subdirs(gtest)
