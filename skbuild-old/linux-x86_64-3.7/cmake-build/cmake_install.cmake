# Install script for directory: /hydrogen/home/zhy/Documents/qcqc-project/qiskit/qiskit-code/qiskit-aer

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/hydrogen/home/zhy/Documents/qcqc-project/qiskit/qiskit-code/qiskit-aer/_skbuild/linux-x86_64-3.7/cmake-install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/hydrogen/home/zhy/Documents/qcqc-project/qiskit/qiskit-code/qiskit-aer/_skbuild/linux-x86_64-3.7/cmake-build/qiskit/providers/aer/pulse/cy/cmake_install.cmake")
  include("/hydrogen/home/zhy/Documents/qcqc-project/qiskit/qiskit-code/qiskit-aer/_skbuild/linux-x86_64-3.7/cmake-build/qiskit/providers/aer/pulse/qutip_lite/cy/cmake_install.cmake")
  include("/hydrogen/home/zhy/Documents/qcqc-project/qiskit/qiskit-code/qiskit-aer/_skbuild/linux-x86_64-3.7/cmake-build/qiskit/providers/aer/backends/wrappers/cmake_install.cmake")
  include("/hydrogen/home/zhy/Documents/qcqc-project/qiskit/qiskit-code/qiskit-aer/_skbuild/linux-x86_64-3.7/cmake-build/src/open_pulse/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/hydrogen/home/zhy/Documents/qcqc-project/qiskit/qiskit-code/qiskit-aer/_skbuild/linux-x86_64-3.7/cmake-build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
