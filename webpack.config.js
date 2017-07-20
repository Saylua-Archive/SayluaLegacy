const path = require('path');
const webpack = require('webpack');

module.exports = {
  entry: './frontend/source/Main.js',
  output: {
    path: path.resolve('frontend/static/js'),
    filename: './saylua.min.js'
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        use: 'babel-loader'
      }
    ]
  },
  plugins: [
    new webpack.ProvidePlugin({
      'Promise': 'es6-promise'
    })
  ],
  resolve: {
    extensions: ['.js', '.jsx']
  }
}
