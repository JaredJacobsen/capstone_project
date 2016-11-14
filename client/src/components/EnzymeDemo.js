import React, { Component } from 'react'
import axios from 'axios'
import ProteinsForm from './ProteinsForm'
import Predictions from './Predictions'

class EnzymeDemo extends Component {

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
      axios.post('http://127.0.0.1:5000/predict-Enzymes', {
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
        <h1>Enzyme Predictor</h1>
        {!this.state.predictions
          ? <ProteinsForm onSubmitANums={this.onSubmitANums.bind(this)} />
          : <Predictions predictions={this.state.predictions}
                         targetVariableName='Enzyme'
                         newPredictionHandler={this.newPredictionHandler.bind(this)} />}
      </div>
    )
  }

}


export default EnzymeDemo
