
/*
 |--------------------------------------------------------------------------
 | Browser-sync config file
 |--------------------------------------------------------------------------
 |
 | For up-to-date information about the options:
 |   http://www.browsersync.io/docs/options/
 |
 | There are more options than you see here, these are just the ones that are
 | set internally. See the website for more info.
 |
 |
 | http://doc.jsfiddle.net/use/echo.html
 */
module.exports = {
    "ui": {
        "port": 3001,
        "weinre": {
            "port": 8080
        }
    },
    "files": ["/tmp/_fiddle/index.css", "/tmp/_fiddle/index.html", "/tmp/_fiddle/index.js"],
    "watchOptions": {},
    "server": "/tmp/_fiddle",
    "proxy": false,
    "port": 3000,
    "middleware": [
        {
            route: "/echo/html",
            handle: function (req, res, next) {
                // method: post
                // params: html, delay
                // response: html
                let body = [];
                req.on('data', function(chunk) {
                    body.push(chunk);
                }).on('end', function() {
                    body = Buffer.concat(body).toString();
                    let qs = require('querystring');
                    let params = qs.parse(body);
                    res.setHeader('Content-Type', 'text/html');
                    let delay = (params['delay'] || 0) * 1000;
                    setTimeout(function () {
                        res.end(params['html'] || '');
                    }, delay);
                });
            },
        },
        {
            route: '/echo/jsonp',
            handle: function(req, res, next) {
                //  method: get
                //  params: jsonp, delay, callback
                //  response: callback(jsonp);
                let body = [];
                let parsed_url = require('url').parse(req.url);
                let qs = require('querystring');
                let params = qs.parse(parsed_url['query'] || '');
                res.setHeader('Content-Type', 'application/javascript');
                let delay = (params['delay'] || 0) * 1000;
                setTimeout(function () {
                    let callback = params['callback'] || "callback";
                    res.end(callback + "(" + (params['jsonp'] || '') + ");");
                }, delay);
            },
        },
        {
            route: "/echo/json",
            handle: function (req, res, next) {
                // method: post
                // params: json, delay
                // response: json
                let body = [];
                req.on('data', function(chunk) {
                    body.push(chunk);
                }).on('end', function() {
                    body = Buffer.concat(body).toString();
                    let qs = require('querystring');
                    let params = qs.parse(body);
                    res.setHeader('Content-Type', 'application/json');
                    let delay = (params['delay'] || 0) * 1000;
                    setTimeout(function () {
                        res.end(params['json'] || '');
                    }, delay);
                });
            },
        },
        {
            route: '/echo/xml',
            handle: function (req, res, next) {
                // method: post
                // params: xml, delay
                // response: xml
                let body = [];
                req.on('data', function(chunk) {
                    body.push(chunk);
                }).on('end', function() {
                    body = Buffer.concat(body).toString();
                    let qs = require('querystring');
                    let params = qs.parse(body);
                    res.setHeader('Content-Type', 'text/xml');
                    let delay = (params['delay'] || 0) * 1000;
                    setTimeout(function () {
                        res.end(params['xml'] || '');
                    }, delay);
                });
            }
        },
        {
            route: '/echo/js',
            handle: function (req, res, next) {
                // method: get
                // params: js, delay
                // response: js
                let body = [];
                let parsed_url = require('url').parse(req.url);
                let qs = require('querystring');
                let params = qs.parse(parsed_url['query'] || '');
                res.setHeader('Content-Type', 'application/javascript');
                let delay = (params['delay'] || 0) * 1000;
                setTimeout(function () {
                    res.end(params['js'] || '');
                }, delay);
            },
        },
        {
            route: "/echo",
            handle: function (req, res, next) {
                // method: get or post
                // query: delay
                // response: request body
                let body = [];
                req.on('data', function(chunk) {
                    body.push(chunk);
                }).on('end', function() {
                    body = Buffer.concat(body).toString();
                    res.setHeader('Content-Type', req.headers['content-type'] || 'text/html');
                    let parsed_url = require('url').parse(req.url);
                    let qs = require('querystring');
                    let params = qs.parse(parsed_url['query'] || '');
                    let delay = (params['delay'] || 0) * 1000;
                    setTimeout(function () {
                        res.end(body);
                    }, delay);
                });
            },
        },
    ],
    "serveStatic": [],
    "ghostMode": {
        "clicks": true,
        "scroll": true,
        "forms": {
            "submit": true,
            "inputs": true,
            "toggles": true
        }
    },
    "logLevel": "info",
    "logPrefix": "BS",
    "logConnections": false,
    "logFileChanges": true,
    "logSnippet": true,
    "rewriteRules": [],
    "open": true,
    "browser": "default",
    "cors": true,
    "xip": false,
    "hostnameSuffix": false,
    "reloadOnRestart": false,
    "notify": false,
    "scrollProportionally": true,
    "scrollThrottle": 0,
    "scrollRestoreTechnique": "window.name",
    "scrollElements": [],
    "scrollElementMapping": [],
    "reloadDelay": 0,
    "reloadDebounce": 500,
    "reloadThrottle": 0,
    "plugins": [],
    "injectChanges": true,
    "startPath": null,
    "minify": true,
    "host": null,
    "localOnly": false,
    "codeSync": true,
    "timestamps": true,
    "clientEvents": [
        "scroll",
        "scroll:element",
        "input:text",
        "input:toggles",
        "form:submit",
        "form:reset",
        "click"
    ],
    "socket": {
        "socketIoOptions": {
            "log": false
        },
        "socketIoClientConfig": {
            "reconnectionAttempts": 50
        },
        "path": "/browser-sync/socket.io",
        "clientPath": "/browser-sync",
        "namespace": "/browser-sync",
        "clients": {
            "heartbeatTimeout": 5000
        }
    },
    "tagNames": {
        "less": "link",
        "scss": "link",
        "css": "link",
        "jpg": "img",
        "jpeg": "img",
        "png": "img",
        "svg": "img",
        "gif": "img",
        "js": "script"
    }
};
