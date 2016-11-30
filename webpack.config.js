import path from 'path'

module.exports = {
  entry: './client/src/app.js',
  output: {
    path: path.join(__dirname, 'dist'),
    filename: "build.js",
    publicPath: '/client/dist/'
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
