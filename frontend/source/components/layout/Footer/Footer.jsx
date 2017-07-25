import Inferno from 'inferno';
import Component from 'inferno-component';
import './Footer.scss';

import StaffActions from './StaffActions';
import Clock from './Clock';

// The main Saylua layout component.
export default class Footer extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let separator = ' \u2022 ';
    return (
      <footer id="footer">
        <div className="sidebar-filler"></div>
        <div className="footer-content">
          <StaffActions level="moderation" />
          <StaffActions level="admin" />
          <p>
            <a href="/online/">1 Online</a> { separator }
            <a href="#">Back to Top</a> { separator }
            <a href="/page/about/">About</a> { separator }
            <a href="/page/credits/">Credits</a> { separator }
            <a href="/page/terms/">Terms of Service</a> { separator }
            <a href="/page/rules/">Site Rules</a> { separator }
            <a href="/page/contact/">Contact Us</a> { separator }
            <span id="social-icons">
              <a href="https://www.facebook.com/officialsaylua/" target="_blank" rel="noopener">
                <i className="fa fa-fw fa-facebook" aria-hidden="true"></i>
              </a>
              <a href="https://twitter.com/officialsaylua" target="_blank" rel="noopener">
                <i className="fa fa-fw fa-twitter" aria-hidden="true"></i>
              </a>
              <a href="http://saylua.tumblr.com/" target="_blank" rel="noopener">
                <i className="fa fa-fw fa-tumblr" aria-hidden="true"></i>
              </a>
              <a href="https://www.reddit.com/r/saylua" target="_blank" rel="noopener">
                <i className="fa fa-fw fa-reddit" aria-hidden="true"></i>
              </a>
            </span>
          </p>
          <form method="post" action="">
            <Clock />
            { separator }
            <button className="link-button" name="theme_id" value="0">
              <i className="fa fa-fw fa-sun-o" aria-hidden="true"></i>
            </button>
            { separator }
            <button className="link-button" name="theme_id" value="1">
              <i className="fa fa-fw fa-moon-o" aria-hidden="true"></i>
            </button>
          </form>
          <p>
            &copy; 2016 <a href="/">Saylua</a>
          </p>
          <p>
            <a href="/admin/">Admin Panel</a>
          </p>
        </div>
      </footer>
    );
  }
}
