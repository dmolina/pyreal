CMAKE_MINIMUM_REQUIRED(VERSION 2.8)
ADD_DEFINITIONS("-Wall")
SET(SRC
    pycec2005.cc
    cec2005/srandom.cc
    cec2005/random.cc
    )

IF(NOT CMAKE_BUILD_TYPE)
  SET(CMAKE_BUILD_TYPE "DEBUG")
ENDIF()

FIND_PACKAGE(Boost 1.46.0 COMPONENTS python REQUIRED)
find_package(PythonLibs REQUIRED)
ADD_SUBDIRECTORY(cec2005)

link_directories (
    ${Boost_LIBRARIES} 
    ${PYTHON_LIBRARIES}
    cec2005/
)
include_directories ( 
    ${Boost_INCLUDE_DIRS} 
    ${PYTHON_INCLUDE_DIRS}
    "/usr/include/python2.7"
)

#ADD_LIBRARY (testExtractor SHARED TestExtractor.cc)
#TARGET_LINK_LIBRARIES(testExtractor ${Boost_LIBRARIES})
ADD_LIBRARY (pycec2005 SHARED ${SRC})
TARGET_LINK_LIBRARIES(pycec2005 ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} cec2005 python2.6
    boost_python
)
