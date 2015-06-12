# polymer_d3_ws
Trying to get polymer to work with d3 and websockets

To run this (WORK IN PROGRESS!) demo you need to run ythe socket and HTTP server using the command:

```
$ twistd -ny streamer.py
```

this will serve the content in localhost:8080/
You should see a main page, where I'm intgerating the components at index.html

To interact with the web socket server run 

Must to have twisted and txws installed for this. (might have to install six as well)
