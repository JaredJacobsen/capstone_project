import React, { Component } from 'react'
import axios from 'axios'
import ProteinsForm from './ProteinsForm'
import Predictions from './Predictions'

const h1Style = {
  width: '50%',
  margin: 'auto',
  textAlign: 'center'
}

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

  onSubmitANums(textInput) {
    if (this.text_input != '') {
      axios.post('http://www.jaredjacobsen.space/api/predict-allergens', {
        textInput: textInput
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
    return (
      <div>
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
