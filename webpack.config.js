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
      },
      {
        test: /\.scss$/,
        use: [
          {
            loader: 'style-loader'
          }, {
            loader: 'css-loader'
          }, {
            loader: 'sass-loader',
            options: {
              includePaths: [path.resolve(__dirname, 'frontend/source/scss/')]
            }
          }
        ]
      }
    ]
  },
  plugins: [
    new webpack.ProvidePlugin({
      'Promise': 'es6-promise'
    }),
    new webpack.ProvidePlugin({
        'Inferno': 'react'
    })
  ],
  resolve: {
    extensions: ['.js', '.jsx'],
    modules: ['./node_modules', './frontend/source'],
    alias: {
			'react': 'inferno-compat',
			'react-dom': 'inferno-compat',
      'react-dom/server': 'inferno-compat',
		},
  }
}
