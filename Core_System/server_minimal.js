const http = require('http');
const server = http.createServer((req, res) => {
    res.end('Hello');
});
server.listen(3002, () => {
    console.log('Server listening on 3002');
});
setInterval(() => {}, 1000);