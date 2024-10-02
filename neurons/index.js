const {WebSocketServer} = require("ws")

const wss = new WebSocketServer({
    port:3456
})
var cons = []
wss.on("connection", (ws) => {
    cons.push(ws)

    ws.on("message", (message) => {
        console.log(message.toString())
        for (let con of cons) {
            if(con !== ws){
                con.send(message.toString())
            }
        }
    })
})

