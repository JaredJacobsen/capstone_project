import React, { Component } from 'react'
import { FormGroup, ControlLabel, FormControl, FieldGroup, Button} from 'react-bootstrap'
import axios from 'axios'

const style = {
  marginTop: '100px',
  width: '65%',
  marginRight: 'auto',
  marginLeft: 'auto'
}

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
      <form onSubmit={(e) => {e.preventDefault()}} style={style}>
        <FormGroup controlId="formControlsTextarea">
          <ControlLabel style={{marginBottom: '20px'}}>Input protein sequences</ControlLabel>
          <FormControl componentClass="textarea" placeholder="e.g., MQDRLSTYR..., MDRYQWRD..." onChange={this.onChange.bind(this)}/>
        </FormGroup>
        <Button type="button" onClick={() => {this.props.onSubmitANums(this.state.text_input)}}>Predict</Button>
      </form>
    )
  }
}

export default ProteinsForm
