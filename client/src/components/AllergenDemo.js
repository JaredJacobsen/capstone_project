import React, { Component } from 'react'
import axios from 'axios'
import ProteinsForm from './ProteinsForm'
import Predictions from './Predictions'

class AllergenDemo extends Component {

  constructor(props) {
    super(props)
    this.predictions = []
  }

  submitANums(text_input) {
    if (this.text_input != '') {
      axios.post('http://127.0.0.1:5000/predict_allergens', {
        text_input: text_input
      })
      .then((response) => {
        this.predictions = response.predictions
      })
      .catch((error) => {
        console.log(error)
      })
    }
  }

  render() {
    return (
      <div>
        <h1>Allergen Demo</h1>
        <ProteinsForm submitANums={this.submitANums.bind(this)} />
      </div>
    )
  }

}


export default AllergenDemo
