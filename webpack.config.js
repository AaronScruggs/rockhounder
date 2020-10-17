var path = require("path");
// var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,

  entry: './assets/js/app.js',

  output: {
    path: path.resolve(__dirname, './assets/bundles'),
    publicPath: "/static/",
    filename: "[name].js",
  },
  devServer: {
    writeToDisk: true,
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx'],
    alias: { vue: 'vue/dist/vue.esm.js' }
  }

};