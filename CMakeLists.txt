PROJECT(cserver)
SET (SRC
    server.c)
ADD_EXECUTABLE(server ${SRC})
TARGET_LINK_LIBRARIES(server zmq)
