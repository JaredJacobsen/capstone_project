import React, { Component } from 'react'
import axios from 'axios'
import ProteinsForm from './ProteinsForm'
import Predictions from './Predictions'

const h1Style = {
  width: '50%',
  margin: 'auto',
  textAlign: 'center'
}

// should by modified to allow input of true class labels, to calculate accuracy
class AllergenDemo extends Component {

  constructor(props) {
    super(props)
    this.state = {
      predictions: false
    }
  }

  newPredictionHandler() {
    this.setState({predictions: false})
  }

  onSubmitANums(text_input) {
    if (this.text_input != '') {
      axios.post('http://127.0.0.1:5000/predict-allergens', {
        text_input: text_input
      })
      .then((response) => {
        this.setState({predictions: response.data})
      })
      .catch((error) => {
        console.log('error ', error)
      })
    }
  }

  render() {
    console.log('render')
    return (
      <div>
        <h1 style={h1Style}>Allergen Prediction</h1>
        {!this.state.predictions
          ? <ProteinsForm onSubmitANums={this.onSubmitANums.bind(this)} />
          : <Predictions predictions={this.state.predictions}
                         targetVariableName='Allergen'
                         newPredictionHandler={this.newPredictionHandler.bind(this)} />}
      </div>
    )
  }

}


export default AllergenDemo
