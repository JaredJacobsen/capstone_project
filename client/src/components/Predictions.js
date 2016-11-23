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
              {this.props.predictions[0].acc_num ? <th>Accession #</th> : undefined}
              {this.props.predictions[0].protein_name ? <th>Protein Name</th> : undefined}
              {this.props.predictions[0].organism_name ? <th>Organism Name</th> : undefined}
              <th>Sequence</th>
              <th>Prediction</th>
            </tr>
          </thead>
          <tbody>
            {Object.values(this.props.predictions).map((p, index) => {
              return (
                <tr key={index}>
                  {p.acc_num ? <td>{p.acc_num}</td> : undefined}
                  {p.protein_name ? <td>{p.protein_name}</td> : undefined}
                  {p.organism_name ? <td>{p.organism_name}</td> : undefined}
                  <td>{p.sequence}</td>
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
