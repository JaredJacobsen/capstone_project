import React, { Component } from 'react'
import AllergenDemo from './AllergenDemo'
import NavBar from './NavBar'

class Application extends Component {

  render() {
    return (
      <div>
        <NavBar/>
        <AllergenDemo />
      </div>
    )
  }
}

export default Application;
