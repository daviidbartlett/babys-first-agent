# Error-handling middleware

In Express, error-handling middleware functions are similar to regular middleware but must include four arguments: (`err, req, res, next`). Express uses the number of parameters to distinguish error-handling middleware from other types.

Calling `next()` without an argument passes control to the next middleware function. Calling `next` with an argument e.g., `next(err)` skips any remaining non-error middleware and passes the error to the next error-handling middleware in the stack.

From Express 5 onwards, thrown errors and rejected Promises in async route handlers or controllers are automatically forwarded to error-handling middleware, without needing to manually call `next(err)`.

### Passing an error

The first argument of an error-handling middleware function is the error that the `next` function inside the controller is invoked with.

For example, the below controller will invoke the `next` function if there is an error from the `fetchPetsByOwnerId` function, which will in turn invoke the error-handling middleware function inside `app.js`:

```js
// controller.js
exports.getPetsByOwnerId = (req, res, next) => {
  const { ownerId } = req.params;
  fetchPetsByOwnerId(ownerId).then((ownersPets) => {
    res.status(200).send({ownersPets: ownersPets})
  }).catch((err) => {
    next(err)
  })
};

// app.js
app.get("/pets/:ownerId", getPetsByOwnerId)

app.use((err, req, res, next) => {
  console.log(err);
  res.status(500).send({ msg: "Server Error!"});
});
```

The benefit of being able to pass errors to specific error-handling functions, it that it saves duplicate code and allows concerns to be separated.

Express has a default error-handler for if another error-handling middleware function has not been defined, which by default will send a status `500` with whatever error that `next` has been invoked with.

#### Express 5 and Thrown Errors

As mentioned above, in Express 5, if an error is thrown or a Promise is rejected inside an async controller or route handler, it is automatically forwarded to the nearest error-handling middleware. There is no need to call `next(err)` manually.

For example:

```js
exports.getPetsByOwnerId = (req, res) => {
  const { ownerId } = req.params;
  return fetchPetsByOwnerId(ownerId).then((ownersPets) => {
    res.status(200).send({ ownersPets });
  });
};
```
If `fetchPetsByOwnerId` rejects, Express 5 will catch the rejection and pass the error to any error-handling middleware - even though `next` is not used explicitly.

> Note: The Promise must be returned from the controller. If it is not returned, Express will not be able to catch the rejection automatically.

However, `.catch(next)` can still be used when more control is needed. Examples of when this would be useful include:
- Logging errors in development.
- Transforming the error before it hits the error-handling middleware.
- Preventing certain errors from reaching the client.

If the error is caught inside a `.catch` block, `next` _must_ be invoked manually in order to pass the error to the next middleware function.

### Separate error-handling middleware functions

Error-handling middleware functions can quickly become complex and unwieldy. To manage this, it is good practice to split the error-handling logic between multiple error-handling blocks that will be responsible for dealing with different types of errors and responses.

Errors can be passed down these blocks using `next(err)` if the condition to send a specific error status and message is not met:

```js
// app.js
app.use((err, req, res, next) => {
  if (err.status) {
    res.status(err.status).send({ msg: err.msg });
  } else next(err);
});

app.use((err, req, res, next) => {
  if (err.code === "22P02") {
    res.status(400).send({ msg: "Invalid input" });
  } else next(err);
});

app.use((err, req, res, next) => {
  console.log(err);
  res.status(500).send({ msg: "Internal Server Error" });
});
//...
```

Error-handling middleware functions can be further separated into a different file in order to keep the app tidy and maintain all of the error-handling logic in one place:

```js
// app.js
const {
  handleCustomErrors,
  handleServerErrors
} = require("./errors/index.js");

app.use(handleCustomErrors);
app.use(handleServerErrors);

// errors/index.js
exports.handleCustomErrors = (err, req, res, next) => {
  if (err.status && err.msg) {
    res.status(err.status).send({ msg: err.msg });
  } else next(err);
};

exports.handleServerErrors = (err, req, res, next) => {
  console.log(err);
  res.status(500).send({ msg: "Internal Server Error" });
};
```

## PostgreSQL errors

PostgreSQL throws errors which are assigned five-character error codes. These are *not* to be confused with HTTP status codes.

  An example PostgreSQL error object looks similar to the following:

```js
{
  error: 'invalid input syntax for integer: "notAnID"'
    at ...
  // ...
  name: 'error',
  length: 96,
  severity: 'ERROR',
  code: '22P02',
  // ...
}
```

Some common instances in which PostgreSQL may throw an error include:

- Missing required fields (`NOT NULL` violation)
- Invalid input
- Column name does not exist
- Table name does not exist

A full list of error codes can be found in the [PostgreSQL documentation](https://www.postgresql.org/docs/current/errcodes-appendix.html).

### Handling PostgreSQL errors

Based on the error that has been thrown by PostgreSQL, an error-handling middleware function can be configured to send a custom response.

The code below would cause a response to be sent with a status `500` and an appropriate error message based on the PostgreSQL error code of `22P02`.

```js
// app.js
app.use((err, req, res, next) => {
  if (err.code === "22P02") {
    res.status(400).send({ msg: "Bad Request" });
  } else res.status(500).send({ msg: "Internal Server Error" });
});
```

## Custom errors

In instances where PostgreSQL does not throw an error, but an error-status and message should be sent by the server, a custom error can be defined and thrown to the `catch` block for `next` to be invoked with.

### Creating a custom error

An example where this may occur is when there is no error in the SQL query, but the query does not return any data/rows.

This can be identified in the model function, where the **promise** can be rejected with a custom error (including a status code and message) which would be caught by the `.catch(next)` block in the controller function:

```js
// models/users.js
exports.selectUserById = (user_id) => {
  return db
    .query('SELECT * FROM users WHERE user_id = $1;', [user_id])
    .then(({ rows }) => {
      const user = rows[0];
      if (!user) {
        return Promise.reject({
          status: 404,
          msg: `No user found for user_id: ${user_id}`,
        });
      }
      return user;
    });
};
```

### Handling the custom error

Once `next` is invoked with the custom error status code and message in the controller, the error is passed to the next error-handling middleware function, where the appropriate HTTP status and response can be sent based on what went wrong.

For example:

```js
// app.js
app.use((err, req, res, next) => {
  // handle custom errors
  if (err.status && err.msg) {
    res.status(err.status).send({ msg: err.msg });
  } else {
    console.log(err);
    res.status(500).send({ msg: "Internal Server Error" });
  }
});
```

## Testing errors

When it comes to testing errors, follow the normal **test-driven development** cycle (Red, Green, Refactor). Write a test, and watch it fail:

```js
// app.test.js
test("status:400, responds with an error message when passed a bad user ID", () => {
  return request(app)
    .get("/api/users/notAnID")
    .expect(400)
    .then(({ body }) => {
      expect(body.msg).toBe("Invalid input");
    });
});
```

Once the test has failed, ensure that the controller function has a `.catch` block that will invoke `next` with any error that occurs in the promise chain:

```js
// controllers/users.js
exports.sendUserById = (req, res, next) => {
  const { user_id } = req.params;
  selectUserById(user_id)
    .then((user) => res.status(200).send({ user }))
    .catch(next);
};
```

This will pass the error to the next error-handling middleware function:

```js
// app.js
app.use((err, req, res, next) => {
  console.log(err);
  res.status(500).send({ msg: "Internal Server Error" });
});
```