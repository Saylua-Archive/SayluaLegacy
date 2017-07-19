const path = require('path');
module.exports = {
  entry: './frontend/components/Main.js',
  output: {
    path: path.resolve('frontend/static'),
    filename: 'saylua.min.js'
  },
  module: {
    loaders: [
      { test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/ },
      { test: /\.jsx$/, loader: 'babel-loader', exclude: /node_modules/ }
    ]
  }
}
