#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/miguel/ws_moveit/src/universal_robot/ur_driver"

# snsure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/miguel/ws_moveit/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/miguel/ws_moveit/install/lib/python2.7/dist-packages:/home/miguel/ws_moveit/build/ur_driver/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/miguel/ws_moveit/build/ur_driver" \
    "/usr/bin/python" \
    "/home/miguel/ws_moveit/src/universal_robot/ur_driver/setup.py" \
    build --build-base "/home/miguel/ws_moveit/build/ur_driver" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/miguel/ws_moveit/install" --install-scripts="/home/miguel/ws_moveit/install/bin"
