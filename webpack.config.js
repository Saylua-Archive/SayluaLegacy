var webpack = require("webpack");
var sourceMaps = '';
var plugins = [];

if (process.env.NODE_ENV === "dev") {
  sourceMaps = 'source-map';
} else {
  // Only minify and de-dupe in prod, as this is expensive time-wise.
  plugins = [
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.UglifyJsPlugin({
      "compress": {
        "warnings": false
      }
    })
  ];
}

module.exports = {
  "plugins": plugins,
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