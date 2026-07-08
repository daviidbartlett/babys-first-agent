# HTTP Servers

## Clients and servers

A **client** is an application making a request for external data, typically a browser.

A **server** is any program listening for requests on a computer **port**, that then processes these requests and sends responses accordingly.

For web development purposes, both request and response will usually follow the HTTP protocol.

## Building a server from scratch

The built-in http library in Node can be used to build a server.

### createServer()

The `.createServer` method is used to create a server and takes a callback function as the only argument. This callback function takes a request and response argument and will be called each time the server receives a request.

```js
const server = http.createServer((request, response) => {
  console.log("request received");
});
```

### listen()

For a server to receive and handle requests, it must be **listening**. To make a http server listen, invoke the server's `.listen` method with the port number that the server will listen on.

```js
const server = http.createServer((request, response) => {
  console.log(request);
});

server.listen(9090);
```

To start the server listening, run the file with `node`, e.g. `node server.js`.

The `listen` method can also take a a callback function as the second argument. This callback function can be used to handle any errors when `.listen` is invoked:

```js
const server = http.createServer((request, response) => {
  console.log(request);
});

server.listen(9090, (err) => {
  if (err) console.log(err);
  else console.log("Server listening on port: 9090");
});
```

### Sending a response

Once the server is listening and receives a request from a client, `createServer`'s request/response callback function will be invoked. The `response` parameter should be configured to send an appropriate **header**, **status code**, and **body** back to the client:

```js
const server = http.createServer((request, response) => {
  response.setHeader("Content-Type", "application/json");
  response.statusCode = 200;
  response.write(JSON.stringify({ msg: "hello world" }));
  response.end();
});
```

Invoking `response.end()` sends the response back to the client.

### Using the method and URL

Clients can make requests to different endpoints on a server or using different methods. Custom responses should be sent back based on the request's method and URL:

```js
const server = http.createServer((request, response) => {
  const { method, url } = request;
  if (url === "/" && method === "GET") {
    response.setHeader("Content-Type", "application/json");
    response.statusCode = 200;
    response.write(JSON.stringify({ msg: "Server up and running" }));
    response.end();
  };

  if (url === "/users" && method === "GET") {
    // Logic to retrieve users and send the appropriate response
  };

  if (url === "/users" && method === "POST") {
    // Logic to add a new user and send the appropriate response
  };
});
```

### Assembling the request body

If receiving a POST, PATCH or PUT request, the request should contain a `body` with the appropriate data to be handled. However, this data comes in multiple packets that must be pieced together from the `request` object.

```js
  if (url === "/users" && method === "POST") {
    let body = "";

    request.on("data", (packet) => {
      body += packet.toString();
    });

    request.on("end", () => {
      // The body can be handled here as a complete object
    });
  };
```