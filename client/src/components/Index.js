import React, { Component } from 'react'
import { Link } from 'react-router'
import { Jumbotron, Button } from 'react-bootstrap'

const style = {
  marginTop: '10px',
  height: '600px',
  backgroundImage: 'url(' + '../public/wheat.jpg' + ')',
  backgroundSize: 'cover'
};

class Index extends Component {

  render() {
    return (
      <div>
        <Jumbotron style={style}>
          <h1 style={{color: 'LightGray'}}>A Protein Allergen Classifier</h1>
          <p style={{color: 'LightGray'}}>An advanced machine learning model that predicts the allergenicity of proteins</p>
          <p><Link to='client/dist/allergen'><Button bsStyle="primary" >Make Predictions</Button></Link></p>
        </Jumbotron>
      </div>
    )
  }
}

export default Index;
