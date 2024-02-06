const { io } = require("socket.io-client");

const socket = io(
  "http://chrone-dev-node-env.eba-t5g6xad2.us-east-1.elasticbeanstalk.com",
  {
    path: "/socket-io",
  }
);

io.on("connection", () => {
  console.log("connected");
  socket.emit("foo", "bar");
});

console.log("on ended");
