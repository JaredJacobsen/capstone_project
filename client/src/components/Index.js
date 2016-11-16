import React, { Component } from 'react'
import { Link } from 'react-router'
import { Jumbotron, Button } from 'react-bootstrap'

// const divStyle = {
//   backgroundImage: 'url(' + '../public/wheat.jpg' + ')',
//   backgroundSize: 'cover'
// };

class Index extends Component {

  render() {
    return (
      <div>
        <Jumbotron>
          <h1>A Protein Allergen Classifier</h1>
          <p>An advanced machine learning model that predicts the allergenicity of proteins</p>
          <p><Link to='client/dist/allergen'><Button bsStyle="primary" >Make Predictions</Button></Link></p>
        </Jumbotron>
      </div>
    )
  }
}

export default Index;
