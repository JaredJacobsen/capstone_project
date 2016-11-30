module.exports = {
  entry: './client/src/app.js',
  output: {
    path: __dirname,
    filename: "./client/dist/build.js",
    publicPath: "/"
  },
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'babel',
        query: {
          presets: ['react', 'es2015']
        }
      }
    ]
  }
};
