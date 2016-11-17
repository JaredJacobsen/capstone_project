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
            <Link style={{color: 'DarkCyan'}} to="/client/dist/">
              AutoProt Classifier
            </Link>
          </Navbar.Brand>
          <Navbar.Toggle />
        </Navbar.Header>
        <Navbar.Collapse>
          <Nav>
            <NavDropdown eventKey={1} title="Demos" id="basic-nav-dropdown">
              <LinkContainer to="/client/dist/allergen">
                <MenuItem eventKey={1.1} href="allergen">Allergen Demo</MenuItem>
              </LinkContainer>
              <LinkContainer to="/client/dist/enzyme">
                <MenuItem eventKey={1.2} href="enzyme">Enzyme Demo</MenuItem>
              </LinkContainer>
              <LinkContainer to="/client/dist/gene-ontology">
                <MenuItem eventKey={1.3} href="gene-ontology">Gene Ontology Demo</MenuItem>
              </LinkContainer>
            </NavDropdown>
            <LinkContainer to="client/dist/custom-classifier">
              <NavItem eventKey={3} href="custom-classifier">Custom Classifier</NavItem>
            </LinkContainer>
            <LinkContainer to="/client/dist/about">
              <NavItem eventKey={2} href="about">About</NavItem>
            </LinkContainer>
          </Nav>
          <Nav pullRight>
            <NavItem eventKey={1} href="https://github.com/JaredJacobsen/capstone_project">Github</NavItem>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  }
}

export default NavBar;
