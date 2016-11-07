import React, { Component } from 'react'
import AllergenDemo from './AllergenDemo'

class Application extends Component {

  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div>
        <h1>Protein Prediction Application</h1>
        <AllergenDemo />
      </div>
    )
  }
}

export default Application;
