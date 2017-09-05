import React, { Component } from 'react';

import './SayluaView.scss';

import Header from './Header';
import Footer from './Footer';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

// The main Saylua layout component.
export default class SayluaView extends Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    this.fixNavbar();

    window.addEventListener('scroll', this.fixNavbar);
  }

  fixNavbar() {
    let top = document.getElementById('header').offsetHeight;
    if (document.body.scrollTop > top ||
      document.documentElement.scrollTop > top) {
      document.getElementById('navbar').classList.add('navbar-fixed');
    } else {
      document.getElementById('navbar').classList.remove('navbar-fixed');
    }
  }

  render() {
    let content = this.props.children;
    let title = this.props.title;

    document.title = 'Saylua - ' + (title ? title : 'Adoptable Fantasy Pets');

    return (
      <div id="saylua">
        <Header />
        <Navbar />

        <div id="main-body" className="main-body">
          <Sidebar />
          <div id="main-body-column" className="main-body-column">
            <div id="main-body-content" className="main-body-content">
              { content }
            </div>
          </div>
        </div>

        <Footer />
      </div>
    );
  }
}
