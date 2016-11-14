import React, { Component } from 'react'
import { Table, Button } from 'react-bootstrap'

class Predictions extends Component {

  render() {
    return (
      <div>
        <h1>Predictions</h1>
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
