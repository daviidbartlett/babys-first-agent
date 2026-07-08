# Express Servers

Express.js, or simply Express, is a popular web framework for Node.js designed for building web applications and APIs.

## Creating a server

In order to create a server, initialise an Express app as an instance of the Express library:

```js
const express = require("express");
const app = express();
```

In order to ensure that the server listens for incoming requests, invoke the server's `listen` method.

The first argument is the port on which to listen, and the second optional argument is a callback function. This is useful for providing console feedback that the server is successfully listening:

```js
app.listen(9090, () => {
  console.log("Server is listening on port 9090...");
});
```

> **Note**: Separate listen functionality to a separate file. Testing packages for back end apps will establish their own listeners, and this will not work if listening happens as part of the app definition.

## Basic Express Endpoint

Express has methods that will mean specific functions are invoked when a particular **HTTP method** and route combination are matched.

```js
const express = require("express");
const app = express();

app.get("/", (req, res) => res.send("Hello World!"));

app.listen(9090, () => console.log("App listening on port 9090!"));
```

The first argument passed to the `.get()` method is the path, e.g. `"/"`.

Any time a `GET` request is received on the `"/"` route, Express will invoke the second argument.

This function is called a **middleware** function. Middleware functions are functions that have access to the request object (`req`) and the response object (`res`) in the application's request-response cycle.

### RESTful API

Express uses a RESTful API structure, meaning that routes are generic rather than being tied to a specific method. For example, both GET and POST requests can be made to the `/users` endpoint, rather than `/get-users` and `/add-user`.

The idea behind RESTful routing is that by just making `/users` available as an endpoint, depending on the HTTP method that is used, the behaviour and response provided will be different.

Have a read of [this article on freeCodeCamp](https://www.freecodecamp.org/news/rest-apis/) for some further explanation.

## Sending a response

In Express, a response can be sent with the `status` and `send` methods:

```js
app.get("/", (req, res) => {
  res.status(200).send({ msg: "Welcome" });
});
```

The status code is set with the `.status` method of the response object.

The `.send` method of the response object automatically sets the `Content-Type` header to `text/html` if passed a string, and to `application/json` if passed an object. It also deals with ending the response and will send a status code of `200` by default if no other status code is specified.

`res.json` can be used to explicitly set the headers so that `Content-Type` is `application/json`. It uses `JSON.stringify()` in the background, so it isn't necessary to stringify data before passing it into the `.send()` or `.json()` methods.

## Handling the request body

Express will not automatically handle the parsing of the request body. Express was designed with minimal functionality, stripping out anything that was not crucial to its use. That includes, by default, the ability to parse the body of the HTTP request.

The following will console.log `undefined`:

```js
app.post("/cats", (req, res) => {
  console.log(req.body); // undefined
});
```

In order to access the body of the request, **application-level middleware** will need to be used. Application-level middleware can be thought of as additional functions that are invoked before the request and response objects are passed.

`express.json()` is a built-in middleware function that will parse incoming request JSON bodies, making them available on the `req.body` property:

```js
const express = require("express");
const app = express();

app.use(express.json());

app.post('/', (req, res) => {
  console.log(req.body);
});
```

## Parametric endpoints

Express allows for passing in a variable value into the path of a parametric endpoint marked by `":"`. It will combine all of these parameters into a **params object**, and place it on the request.

For example, if a request was made to `/cats/1`, it would give the following:

```js
app.get("/cats/:catId", (req, res) => {
  console.log(req.params); // { catId: 1 }
});
```

The value given to the variable in the path will be the key in our `params` object, and the actual value the client has sent in the URL will be the value.

## Queries

Queries are made available by Express on the `query` property of the request object.

For example, a request to `GET /api/cats?grumpy=true` could be handled as follows:

```js
app.get("/cats", (req, res) => {
  const { grumpy } = req.query;
  console.log(grumpy) // true
});
```

The `req.query` object is built up from the key-value pairs defined in the query string. Any additional queries will be added to the object as key-value pairs.[2:35 PM]