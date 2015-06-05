# polymer_d3_ws
Trying to get polymer to work with d3 and websockets

To run this (IN PROGRESS) demo you need to run two things

```
$ python -m SimpleHTTPServer 8080
``` 

this will serve the content in localhost:8080/
You should see a main page, where I'm intgerating the components at index.html

To interact with the web socket server run 
```
$ twistd -ny streamer.py
```

Must to have twisted and txws installed for this.
