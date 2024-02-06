const { io } = require("socket.io-client");

const socket = io("https://timely.work", {
  path: "/socket-io",
});

socket.on("connect", () => {
  //   if (err) {
  //     console.log(err);
  //   } else {
  //     console.log("connected");
  //   }

  socket.on("refresh", () => {
    console.log("received leadRefresh event inside");
  });

  console.log("connected");
});

socket.on("refresh", () => {
  console.log("received leadRefresh event outside");
});

console.log("on ended");
