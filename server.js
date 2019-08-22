const app = require("./api");

const ip = process.env.IP || "0.0.0.0";
const port = process.env.PORT || 3000;

// listen for requests
app.listen(port, ip, () => {
  console.log(`Server listening on http://${ip}:${port}`);
});
