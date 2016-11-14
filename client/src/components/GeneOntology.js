import React, { Component } from 'react'
import axios from 'axios'
import GOForm from './GOForm'
import ProteinsForm from './ProteinsForm'
import Predictions from './Predictions'

class GeneOntology extends Component {

  constructor(props) {
    super(props)
    this.state = {
      ModelBuildError: false,
      predictions: false,
      modelBuilt: false
    }
  }

  newPredictionHandler() {
    this.setState({predictions: false})
  }

  onSubmitGONum(go_id) {
    if (this.text_input != '') {
      axios.post('http://127.0.0.1:5000/build-GO-model', {
        go_id: go_id
      })
      .then((response) => {
        if (response.data.success) {
          this.setState({modelBuilt: true, ModelBuildError: false})
        } else {
          this.setState({ModelBuildError: !response.success})
        }
      })
      .catch((error) => {
        console.log(error)
      })
    }
  }

  onSubmitANums(text_input) {
    if (this.text_input != '') {
      axios.post('http://127.0.0.1:5000/predict-GO', {
        text_input: text_input
      })
      .then((response) => {
        this.setState({predictions: response.data})
      })
      .catch((error) => {
        console.log(error)
      })
    }
  }

  render() {
    if (!this.state.modelBuilt) {
      return (
        <div>
          {this.state.ModelBuildError ? <h2>There was an error building the model. Please enter another GO id</h2> : undefined}
          <GOForm onSubmitGONum={this.onSubmitGONum.bind(this)} />
        </div>
      )
    }
    return (
      <div>
        {!this.state.predictions
          ? <ProteinsForm onSubmitANums={this.onSubmitANums.bind(this)} />
          : <Predictions predictions={this.state.predictions}
                         targetVariableName='Class Prediction'
                         newPredictionHandler={this.newPredictionHandler.bind(this)} />}
      </div>
    )
  }
}

export default GeneOntology;
