import React, { Component } from 'react'
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap'
import { Link } from 'react-router'
import { LinkContainer } from 'react-router-bootstrap'


const style = {
  width: '80%',
  margin: 'auto'
}

class NavBar extends Component {

  render() {
    return (
      <Navbar staticTop >
        <Navbar.Header>
          <Navbar.Brand>
            <Link style={{color: '#52a4f2', fontWeight: 'bold'}} to="/client/dist/">
              Allergen Classifier
            </Link>
          </Navbar.Brand>
          <Navbar.Toggle />
        </Navbar.Header>
        <Navbar.Collapse>
          <Nav>
            <LinkContainer to="/client/dist/allergen">
              <NavItem eventKey={1}>Make Predictions</NavItem>
            </LinkContainer>
            <LinkContainer to="client/dist/model-evaluation">
              <NavItem eventKey={2}>Model Evaluation</NavItem>
            </LinkContainer>
            <LinkContainer to="/client/dist/about">
              <NavItem eventKey={3}>About</NavItem>
            </LinkContainer>
          </Nav>
          <Nav pullRight>
            <NavItem eventKey={1} href="https://github.com/JaredJacobsen/capstone_project/tree/allergen">Github</NavItem>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  }
}

export default NavBar;
