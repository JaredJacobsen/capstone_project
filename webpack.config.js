module.exports = {
  entry: './src/app.js',
  output: {
    path: __dirname,
    filename: "./dist/build.js"
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
