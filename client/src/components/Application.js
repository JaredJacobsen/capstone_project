import React, { Component } from 'react'
import axios from 'axios'
import ProteinsForm from './ProteinsForm'
import Predictions from './Predictions'

class Application extends Component {

  constructor(props) {
    super(props)
    this.predictions = []
  }

  onSubmitHandler(text_input) {
    if (this.text_input != '') {
      axios.post('http://127.0.0.1:5000/predict', {
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
        <h1>hey</h1>
        {this.predictions.length == 0
          ? <ProteinsForm onSubmitHandler={this.onSubmitHandler.bind(this)}/>
          : <Predictions predictions={this.predictions} />
        }
      </div>
    )
  }
}

export default Application;
