import React from 'react'
import ReactDOM from 'react-dom'
import Root from './components/Root'
import { Router, Route, Link, browserHistory, IndexRoute } from 'react-router'
import AllergenDemo from './components/AllergenDemo'
import EnzymeDemo from './components/EnzymeDemo'
import GeneOntology from './components/GeneOntology'
import About from './components/About'
import CustomClassifier from './components/CustomClassifier'
import Index from './components/Index'


ReactDOM.render((
  <Router history={browserHistory}>
    <Route path="/client/dist" component={Root}>
      <IndexRoute component={Index}/>
      <Route path="allergen" component={AllergenDemo} />
      <Route path="enzyme" component={EnzymeDemo} />
      <Route path="gene-ontology" component={GeneOntology} />
      <Route path="custom-classifier" component={CustomClassifier} />
      <Route path="about" component={About} />
    </Route>
  </Router>
), document.getElementById('react-application'))
