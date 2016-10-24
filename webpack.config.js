var webpack = require("webpack");
var sourceMaps = '';

if (process.env.NODE_ENV === "dev") {
  sourceMaps = 'source-map';
}

module.exports = {
  "plugins": [
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.UglifyJsPlugin({
      "compress": {
        "warnings": false
      }
    })
  ],
  "devtool": sourceMaps,
  "module": {
    "loaders": [
      {
        "es6": "saylua/static/source/es6/",
        "loader": "babel-loader"
      }
    ]
  },
  "resolve": {
    "extensions": ["", ".js", ".min.js", ".jsx"],
    "modulesDirectories": ["./saylua/static/js/lib", "./node_modules"],
  }
};