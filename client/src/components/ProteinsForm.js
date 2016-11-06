import React, { Component } from 'react'
import { FormGroup, ControlLabel, FormControl, FieldGroup, Button} from 'react-bootstrap'
import axios from 'axios'

class ProteinsForm extends Component {

  constructor(props) {
    super(props)
    this.text_input = ''
  }

  onChange(e) {
    this.text_input = e.target.value
  }

  render() {
    return (
      <form>
        <FormGroup controlId="formControlsTextarea">
          <ControlLabel>Textarea</ControlLabel>
          <FormControl componentClass="textarea" placeholder="textarea" onChange={this.onChange.bind(this)}/>
        </FormGroup>
        <Button type="submit" onClick={() => this.props.onSubmitHandler(this.text_input)}>
          Submit
        </Button>
      </form>
    )
  }
}

export default ProteinsForm
