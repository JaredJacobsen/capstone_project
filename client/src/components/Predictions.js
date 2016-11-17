import React, { Component } from 'react'
import { Table, Button } from 'react-bootstrap'

const style = {
  width: '65%',
  marginLeft: 'auto',
  marginRight: 'auto',
  marginTop: '20px'
}

class Predictions extends Component {

  render() {
    return (
      <div style={style}>
        <h3>Predictions</h3>
        <Table striped bordered condensed hover>
          <thead>
            <tr>
              <th>Accession #</th>
              <th>Protein Name</th>
              <th>Organism Name</th>
              <th>{this.props.targetVariableName}</th>
            </tr>
          </thead>
          <tbody>
            {Object.values(this.props.predictions).map((p, index) => {
              return (
                <tr key={index}>
                  <td>{p.acc_num}</td>
                  <td>{p.protein_name}</td>
                  <td>{p.organism_name}</td>
                  <td>{p.prediction}</td>
                </tr>
              )
            })}
          </tbody>
        </Table>
        <Button type="button" onClick={() => {this.props.newPredictionHandler()}}>New Predictions</Button>

      </div>
    )
  }

}

export default Predictions
