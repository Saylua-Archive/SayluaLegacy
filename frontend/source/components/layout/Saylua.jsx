import Inferno from 'inferno';
import Component from 'inferno-component';
import './Saylua.scss';

import Header from './Header/Header';
import Footer from './Footer/Footer';
import Navbar from './Navbar/Navbar';
import Sidebar from './Sidebar/Sidebar';

// The main Saylua layout component.
export default class Saylua extends Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    this.fixNavbar();

    window.addEventListener('scroll', this.fixNavbar);
  }

  fixNavbar() {
    let top = document.getElementById('banner').offsetHeight;
    if (document.body.scrollTop > top ||
      document.documentElement.scrollTop > top) {
      document.getElementById('navbar').classList.add('navbar-fixed');
    } else {
      document.getElementById('navbar').classList.remove('navbar-fixed');
    }
  }

  render() {
    let content = "Hello world";
    return (
      <div id="saylua">
        <Header id="header" />
        <Navbar id="navbar" />

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
