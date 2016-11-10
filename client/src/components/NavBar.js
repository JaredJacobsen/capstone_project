import React, { Component } from 'react'
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap'

class NavBar extends Component {

  render() {
    return (
      <Navbar inverse staticTop fluid>
        <Navbar.Header>
          <Navbar.Brand>
            <a href="#" style={{color: 'DarkCyan'}}>Protein Classification Predictor</a>
          </Navbar.Brand>
          <Navbar.Toggle />
        </Navbar.Header>
        <Navbar.Collapse>
          <Nav>
            <NavDropdown eventKey={3} title="Demos" id="basic-nav-dropdown">
              <MenuItem eventKey={3.2} href="">Enzyme Demo</MenuItem>
              <MenuItem eventKey={3.2} href="">Allergy Demo</MenuItem>
            </NavDropdown>
            <NavItem eventKey={2} href="#">About</NavItem>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  }
}

export default NavBar;
