FROM python:3.8
LABEL maintainer "Ragesh Ramachandran <ragesh.ramachandran@ipa.fraunhofer.de>"
SHELL ["/bin/bash","-c"]
ENV WS=/root/ws
RUN apt-get update -y \
    && apt-get install -y python3-pip python3-dev \
    && pip3 install --upgrade pip

WORKDIR $WS/
COPY ./ ./
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade protobuf

RUN chmod +x /docker/entrypoint.sh
ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["bash"]
