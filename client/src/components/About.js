import React, { Component } from 'react'
import ReactBootstrapSlider from 'react-bootstrap-slider'

class About extends Component {

  constructor(props) {
    super(props)
    this.state = {
      currentValue: 0
    }
  }

  changeValue(e) {
    console.log("value changed", this.state.currentValue);
    this.setState({currentValue: e.target.value})
  }

  render() {
    return (
      <div style={{marginLeft: '100px'}}>
        <h1>Coming Soon</h1>
        <ReactBootstrapSlider
          value={this.state.currentValue}
          change={this.changeValue.bind(this)}
          step={0.005}
          max={1}
          min={0}
          orientation="horizontal"
          reverse={true}
           />
      </div>
    )
  }
}

export default About;
