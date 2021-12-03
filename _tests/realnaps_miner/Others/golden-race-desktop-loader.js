var LoaderConfig = function () {
    function LoaderConfig() {
        this.checkScroll = true;
        this.containerId = "golden-race-desktop-app";
        this.profile = undefined;
        this.funMode = undefined;
        this.language = undefined;
        this.oddFormat = undefined;
        this.hwId = undefined;
        this.pinHash = undefined;
        this.onlineHash = undefined;
        this.showBetHistory = undefined;
        this.showTicketTransactions = undefined;
        this.showLanguageSelector = undefined;
        this.showAppsNavigation = undefined;
        this.showMenu = undefined;
        this.showMenuOnDemand = undefined;
        this.showMenuInfo = undefined;
        this.showBreadcrumb = undefined;
        this.showOddFormatSelector = undefined;
        this.showUserCredit = undefined;
        this.showUserName = undefined;
        this.showGameSession = undefined;
        this.showHeader = undefined;
        this.showBetslip = undefined;
        this.showClock = undefined;
        this.showTotalOdd = undefined;
        this.hideLiveEventPanel = undefined;
        this.isFullScreenPlayer = undefined;
        this.bettingLimits = undefined;
        this.forceDisplayCurrencyCode = undefined;
        this.theme = undefined;
        this.spin2WinCoinsMode = undefined;
        this.spin2WinShowRules = undefined;
        this.spin2WinSecondsTransitionStats = undefined;
        this.spin2WinShowPlayAgain = undefined;
        this.allowMultipleBetsByEvent = undefined;
        this.customLinks = undefined;
        this.profileByGame = undefined;
        this.height = undefined;
        this.hideJackpotWinner = undefined
    }
    return LoaderConfig
}();
var GoldenRaceDesktopLoader = function () {
    function GoldenRaceDesktopLoader(config) {
        this.callbacks = {};
        this.scriptId = "golden-race-desktop-loader";
        console.log("GR: Running Loader 2.20.102", config);
        this.setConfig(config);
        this.path = this.calculatePath();
        this.host = this.calculateHost(this.path)
    }
    GoldenRaceDesktopLoader.createInstance = function (data) {
        return grDesktopLoader(data)
    }
        ;
    GoldenRaceDesktopLoader.prototype.init = function () {
        this.listenEvents();
        this.load();
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.setConfig = function (config) {
        if (typeof config !== "object") {
            throw new Error("GR: Config must be an object")
        }
        this.config = new LoaderConfig;
        for (var property in this.config) {
            if (this.config.hasOwnProperty(property) && config.hasOwnProperty(property)) {
                this.config[property] = config[property]
            }
        }
    }
        ;
    GoldenRaceDesktopLoader.prototype.setEventHandlers = function (handlers) {
        var _this = this;
        var events = ["onBetHistory", "onAccountInfo", "onRefreshCredit", "onTicketCreated", "onLogin", "onLogout", "onNewAccount", "onAppReady", "onMenuAvailable", "onRestart", "onWalletNotification", "onCatchError", "onCustomLinkClick", "onHeight"];
        events.forEach(function (method) {
            if (typeof handlers[method] !== "undefined") {
                _this[method](handlers[method])
            }
        })
    }
        ;
    GoldenRaceDesktopLoader.prototype.reload = function () {
        this.dispose();
        this.load();
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.navigate = function (path) {
        var message = {
            navigate: {
                path: path
            }
        };
        this.iframe.contentWindow.postMessage(message, this.path)
    }
        ;
    GoldenRaceDesktopLoader.prototype.changeLanguage = function (language) {
        var message = {
            changeLanguage: {
                language: language
            }
        };
        this.iframe.contentWindow.postMessage(message, this.path)
    }
        ;
    GoldenRaceDesktopLoader.prototype.openBetHistory = function () {
        var message = {
            openBetHistory: {}
        };
        this.iframe.contentWindow.postMessage(message, this.path)
    }
        ;
    GoldenRaceDesktopLoader.prototype.test = function (command) {
        var message = {
            test: {
                name: command
            }
        };
        this.iframe.contentWindow.postMessage(message, this.path)
    }
        ;
    GoldenRaceDesktopLoader.prototype.onAppReady = function (callback) {
        this.setEventListener("appReady", callback);
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.onRestart = function (callback) {
        this.setEventListener("restart", callback);
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.onBetHistory = function (callback) {
        this.setEventListener("betHistory", callback);
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.onAccountInfo = function (callback) {
        this.setEventListener("accountInfo", callback);
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.onTicketCreated = function (callback) {
        this.setEventListener("ticketCreated", callback);
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.onWalletNotification = function (callback) {
        this.setEventListener("walletNotification", callback);
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.onCatchError = function (callback) {
        this.setEventListener("catchError", callback);
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.onRefreshCredit = function (callback) {
        this.setEventListener("refreshCredit", callback);
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.onLogin = function (callback) {
        this.setEventListener("logIn", callback);
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.onLogout = function (callback) {
        this.setEventListener("logOut", callback);
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.onNewAccount = function (callback) {
        this.setEventListener("registerNewAccount", callback);
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.onMenuAvailable = function (callback) {
        this.setEventListener("menuAvailable", callback);
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.onCustomLinkClick = function (callback) {
        this.setEventListener("customLinks", callback);
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.onHeight = function (callback) {
        var _this = this;
        window.addEventListener("message", function (event) {
            if (event.origin === _this.host) {
                try {
                    var data = JSON.parse(event.data);
                    for (var name_1 in data) {
                        if (data.hasOwnProperty(name_1)) {
                            switch (name_1) {
                                case "resizeBody":
                                    _this.container.style.height = data[name_1];
                                    callback("height", data[name_1]);
                                    _this.setEventListener("height", callback);
                                    break
                            }
                        }
                    }
                } catch (error) { }
            }
        });
        return this
    }
        ;
    GoldenRaceDesktopLoader.prototype.load = function () {
        this.injectIframe()
    }
        ;
    GoldenRaceDesktopLoader.prototype.dispose = function () {
        this.iframe.remove();
        this.iframe = undefined
    }
        ;
    GoldenRaceDesktopLoader.prototype.injectIframe = function () {
        var _this = this;
        this.container = document.getElementById(this.config.containerId);
        if (!this.container) {
            throw new Error("GR: Can't find #" + this.config.containerId + ". Did you forget to add the element or wait until DOMContentLoaded?")
        }
        if (this.iframe) {
            this.dispose()
        }
        this.iframe = document.createElement("iframe");
        this.iframe.src = this.path + "/?" + this.buildParams();
        this.iframe.frameBorder = "0";
        this.iframe.scrolling = "no";
        this.iframe.style.display = "block";
        this.iframe.style.height = "100%";
        this.iframe.style.width = "100%";
        this.iframe.setAttribute("allow", "autoplay encrypted-media");
        this.iframe.onload = function () {
            return _this.sendScrollEvent()
        }
            ;
        this.container.appendChild(this.iframe)
    }
        ;
    GoldenRaceDesktopLoader.prototype.buildParams = function () {
        var parameters = [];
        for (var index in this.config) {
            if (this.config.hasOwnProperty(index) && this.config[index] !== undefined) {
                var key = encodeURIComponent(index);
                var value = encodeURIComponent(this.config[index]);
                parameters.push(key + "=" + value)
            }
        }
        return parameters.join("&")
    }
        ;
    GoldenRaceDesktopLoader.prototype.listenEvents = function () {
        var _this = this;
        if (this.config.checkScroll) {
            this.checkScroll()
        }
        window.addEventListener("message", function (event) {
            if (event.origin === _this.host) {
                try {
                    var data = JSON.parse(event.data);
                    for (var name_2 in data) {
                        if (data.hasOwnProperty(name_2)) {
                            switch (name_2) {
                                case "resizeBody":
                                    _this.resizeFrame(data[name_2]);
                                    break;
                                default:
                                    _this.triggerEvent(name_2, data[name_2])
                            }
                        }
                    }
                } catch (error) { }
            }
        })
    }
        ;
    GoldenRaceDesktopLoader.prototype.checkScroll = function () {
        var _this = this;
        window.addEventListener("scroll", function () {
            _this.sendScrollEvent()
        })
    }
        ;
    GoldenRaceDesktopLoader.prototype.sendScrollEvent = function () {
        var boundingRect = this.container.getBoundingClientRect();
        var boundingRectTop = Math.round(boundingRect.top);
        var bottom = boundingRectTop + this.iframe.offsetHeight;
        var scrollTop = 0;
        if (boundingRectTop >= 0) {
            scrollTop = 0
        } else {
            scrollTop = Math.abs(boundingRectTop)
        }
        var scrollHeight;
        if (scrollTop + this.iframe.offsetHeight < window.innerHeight) {
            scrollHeight = this.iframe.offsetHeight
        } else {
            scrollHeight = window.innerHeight;
            if (boundingRectTop > 0) {
                scrollHeight -= boundingRectTop
            }
            if (scrollHeight > bottom) {
                var bottomDifferenced = scrollHeight - bottom;
                scrollHeight -= bottomDifferenced
            }
        }
        var message = {
            scroll: {
                top: scrollTop,
                height: scrollHeight
            }
        };
        this.iframe.contentWindow.postMessage(message, this.path)
    }
        ;
    GoldenRaceDesktopLoader.prototype.setEventListener = function (name, callback) {
        if (callback) {
            if (typeof callback !== "function") {
                throw new Error("GR: Callback must be a function.")
            }
            this.callbacks[name] = callback
        } else {
            delete this.callbacks[name]
        }
    }
        ;
    GoldenRaceDesktopLoader.prototype.resizeFrame = function (height) {
        if (this.iframe) {
            this.container.style.height = height;
            this.sendScrollEvent()
        }
    }
        ;
    GoldenRaceDesktopLoader.prototype.triggerEvent = function (name, data) {
        if (this.callbacks[name]) {
            this.callbacks[name](name, data)
        }
    }
        ;
    GoldenRaceDesktopLoader.prototype.calculatePath = function () {
        var a = document.createElement("a");
        var script = document.getElementById(this.scriptId);
        if (!script) {
            throw new Error("GR: Can't find #" + this.scriptId + ". Did you forget to add the ID?")
        }
        a.href = script.getAttribute("src");
        var parts = a.href.split("/");
        parts.pop();
        return parts.join("/")
    }
        ;
    GoldenRaceDesktopLoader.prototype.calculateHost = function (path) {
        return path.split("/").slice(0, 3).join("/")
    }
        ;
    return GoldenRaceDesktopLoader
}();
function grDesktopLoader(data) {
    var loader = new GoldenRaceDesktopLoader(data);
    loader.setEventHandlers(data);
    return loader.init()
}
