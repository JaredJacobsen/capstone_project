import React from 'react'
import ReactDOM from 'react-dom'
import Root from './components/Root'
import { Router, Route, Link, browserHistory, IndexRoute, Match, BrowserRouter } from 'react-router'
import AllergenDemo from './components/AllergenDemo'
import About from './components/About'
import Index from './components/Index'
import ModelEvaluation from './components/ModelEvaluation'


ReactDOM.render((
  <Router history={browserHistory}>
    <Route path="http://54.214.109.92/" component={Root}>
      <IndexRoute component={Index}/>
      <Route path="allergen" component={AllergenDemo} />
      <Route path="model-evaluation" component={ModelEvaluation} />
      <Route path="about" component={About} />
    </Route>
  </Router>
), document.getElementById('react-application'))
