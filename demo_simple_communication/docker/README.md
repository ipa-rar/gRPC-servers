A Demo gRPC server to test simple request response service

To build the server docker image
```
docker build -t simple_server_app -f docker/Dockerfile-server .
```

To build the client docker image
```
docker build -t simple_client_app -f docker/Dockerfile-client .
```