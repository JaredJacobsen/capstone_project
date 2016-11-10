import React, { Component } from 'react'
import { FormGroup, ControlLabel, FormControl, FieldGroup, Button} from 'react-bootstrap'
import axios from 'axios'

class ProteinsForm extends Component {

  constructor(props) {
    super(props)
    this.state = {
      text_input: ''
    }
  }

  onChange(e) {
    this.state.text_input = e.target.value
  }

  render() {
    return (
      <form>
        <FormGroup controlId="formControlsTextarea">
          <ControlLabel>Input protein accession numbers</ControlLabel>
          <FormControl componentClass="textarea" placeholder="e.g., P31946 P62258 ..." onChange={this.onChange.bind(this)}/>
        </FormGroup>
        <Button type="button" onClick={() => {this.props.submitANums(this.state.text_input)}}>Predict</Button>
      </form>
    )
  }
}

export default ProteinsForm
