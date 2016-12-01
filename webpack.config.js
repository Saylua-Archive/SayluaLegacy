module.exports = {
  "module": {
    "loaders": [
      {
        "es6": "saylua/static/source/es6/",
        "loader": "babel-loader"
      }
    ]
  },
  "output": {
    "filename": "[name].min.js",
  },
  "resolve": {
    "extensions": ["", ".js", ".min.js", ".jsx"],
    "modulesDirectories": ["./saylua/static/js/lib", "./node_modules"],
  }
};
