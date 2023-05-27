# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "D:/USR/Mathematical-Modeling/practice/C++warmup/0_CppPratices/samples/build/_deps/ucmake-src"
  "D:/USR/Mathematical-Modeling/practice/C++warmup/0_CppPratices/samples/build/_deps/ucmake-build"
  "D:/USR/Mathematical-Modeling/practice/C++warmup/0_CppPratices/samples/build/_deps/ucmake-subbuild/ucmake-populate-prefix"
  "D:/USR/Mathematical-Modeling/practice/C++warmup/0_CppPratices/samples/build/_deps/ucmake-subbuild/ucmake-populate-prefix/tmp"
  "D:/USR/Mathematical-Modeling/practice/C++warmup/0_CppPratices/samples/build/_deps/ucmake-subbuild/ucmake-populate-prefix/src/ucmake-populate-stamp"
  "D:/USR/Mathematical-Modeling/practice/C++warmup/0_CppPratices/samples/build/_deps/ucmake-subbuild/ucmake-populate-prefix/src"
  "D:/USR/Mathematical-Modeling/practice/C++warmup/0_CppPratices/samples/build/_deps/ucmake-subbuild/ucmake-populate-prefix/src/ucmake-populate-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "D:/USR/Mathematical-Modeling/practice/C++warmup/0_CppPratices/samples/build/_deps/ucmake-subbuild/ucmake-populate-prefix/src/ucmake-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "D:/USR/Mathematical-Modeling/practice/C++warmup/0_CppPratices/samples/build/_deps/ucmake-subbuild/ucmake-populate-prefix/src/ucmake-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
