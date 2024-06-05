FROM ubuntu:latest
LABEL authors="ivanmatveev"

ENTRYPOINT ["top", "-b"]