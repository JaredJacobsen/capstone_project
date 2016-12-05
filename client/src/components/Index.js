import React, { Component } from 'react'
import { Link } from 'react-router'
import { Jumbotron, Button } from 'react-bootstrap'

const style = {
  marginTop: '50px',
  height: '700px',
  backgroundImage: 'url(https://static.pexels.com/photos/27715/pexels-photo.jpg)',
  // backgroundImage: 'url(' + '../public/wheat.jpg' + ')',
  backgroundSize: 'cover'
};

class Index extends Component {

  render() {
    return (
      <div>
        <Jumbotron style={style}>
          <h1 style={{color: 'White'}}>A Protein Allergen Classifier</h1>
          <p style={{color: 'LightGray'}}>Applying machine learning to predict allergens</p>
          <p><Link to='/allergen'><Button bsStyle="primary" >Make Predictions</Button></Link></p>
        </Jumbotron>
      </div>
    )
  }
}

export default Index;
