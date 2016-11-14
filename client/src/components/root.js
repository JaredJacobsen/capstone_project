import React, { Component } from 'react'
import NavBar from './NavBar'

class Root extends Component {

  render() {
    return (
      <div>
        <NavBar/>
        {this.props.children}
      </div>
    )
  }
}

export default Root;
