# Model-View-Controller

The **MVC** (Model-View-Controller) pattern is a software design pattern commonly used for developing web servers. It separates applications into three main components that allow for resuability of components and promiting a modular approach to development.

## Model

The Model respresents the data and business logic of an application, handling the fetching, updating, creation and deletion of data. It is responsible for sending the relevant data in the required format to the Controller.

## View

The view is the interface that displays data from the Model to the user and sends user inputs to the Controller. _Views will not be covered as part of the Back End block._

## Controller

The Controller handles the **client** request. Using the information contained on the request (path, params, queries and body), it will invoke the **model** that will interact with the dataset. The controller is also responsible for sending a response back to the client.

## Project structure

Functions can become complex and deeply nested when building a web server, whether with http, Express or any other framework. In order to be able to clearly identify what is going on in the server and help debug errors, logic can be abstracted away into separate functions.

To do this consistently, the MVC pattern can be used, splitting code up into separate functions that are responsible for different things within a server:

```js
// app.js
app.get("/api/cats/:catId", getCatById);
```

The controller is responsible for handling the request, invoking the model, and sending the response:

```js
// controllers.js
exports.getCatById = (req, res) => {
 const { catId } = req.params;
 selectCatById(catId).then((cat) => {
   res.status(200).send({ cat });
 });
};
```

The model is responsible for interacting with the data and sending data back to the controller:

```js
// models.js
exports.selectCatById = (catId) => {
 return readFile(`data/cats/${catId}.json`, "utf8").then((catString, err) => {
     const parsedCat = JSON.parse(catString);
     return parsedCat;
   }).catch((err) => {
     return err;
   });
 };
```