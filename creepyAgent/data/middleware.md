# Middleware

Middleware functions are functions that have access to the request object (`req`) and the response object (`res`) in the application's request-response cycle.

## next()

Express middleware functions also have access to a third parameter, the `next` middleware function.

The `next` middleware function can be used to move onto the *next* middleware function in the chain. For example, the following code would log the time before passing control on to the following middleware function that logs `I am logged next`:

```js
const express = require('express');
const app = express();

app.use((req, res, next) => {
  console.log('Time:', Date.now());
  next();
});

app.use((req, res, next) => {
  console.log('I am logged next');
  next(); // Without invoking next, the request and response would not be passed on to the routes
});

app.get('/api/cats', getCats);
```

## express.json()

Express comes with some built-in middleware methods to perform common tasks. [express.json()](http://expressjs.com/en/api.html#express.json) can be used to parse requests with JSON bodies.

The middleware will parse the request body and attach it to the request on a key of `req.body`.

```js
// POST /api/users with a body of { "name": "new user", "likes": [ "coding" ] }

const express = require('express');
const app = express();

app.use(express.json());

app.post('/api/users', (req, res, next) => {
  console.log(req.body); // { name: "new user", likes: [ "coding" ] }
})
```