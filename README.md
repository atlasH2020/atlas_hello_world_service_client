# Hello World Service Client

A FASTAPI client to pair with and consume the hello world service

# Building and Running the Image

In order to build the docker image, follow the below steps:

1. cd atlas_hello_world_service
2. docker build -t atlas_hello_world_service:latest .
3. In the file docker-compose.yml do following changes:
    
    Modify the REGISTRY_CLIENT_ID and REGISTRY_CLIENT_SECRET environment variable's value to the CLIENT_ID and CLIENT_SECRET values used to access the ATLAS service registry

4. Once the changes to the docker-compose file are done you can start the hello_world container by running the following command:

    docker-compose up -d

5. Once the container is up and running the hello_world service can be accessed from:

    http://localhost:8083/hello_world/login

6. Register a new user and login with that user.

7. Pick a service implementing sensor_data template to pair with.

8. In the keycloak page to which you are redirected, provide the username:testuser and password: test.

9. Once authentication is done you will be redirected to service picker page. Now click the hello world link above and you should be able to see the response from the sample service printed onto the screen.










