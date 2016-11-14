import React, { Component } from 'react'
import { FormGroup, ControlLabel, FormControl, FieldGroup, Button} from 'react-bootstrap'
import axios from 'axios'

class GOForm extends Component {

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
      <form onSubmit={(e) => {e.preventDefault()}}>
        <FormGroup controlId="formControlsTextarea">
          <ControlLabel>Input Gene Ontology ID</ControlLabel>
          <FormControl type="text" placeholder="e.g., 0004738" onChange={this.onChange.bind(this)}/>
        </FormGroup>
        <Button type="button" onClick={() => {this.props.onSubmitGONum(this.state.text_input)}}>Build Model</Button>
      </form>
    )
  }
}

export default GOForm
