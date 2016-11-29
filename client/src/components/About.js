import React, { Component } from 'react'
import ReactBootstrapSlider from 'react-bootstrap-slider'

class About extends Component {

  changeValue() {
    console.log("value changed");
  }

  render() {
    return (
      <div>
        <h1>Coming Soon</h1>
        <ReactBootstrapSlider
          value={0}
          change={this.changeValue}
          step={1}
          max={100}
          min={10}
          orientation="vertical"
          reverse={true}
          disabled="disabled" />
      </div>
    )
  }
}

export default About;
