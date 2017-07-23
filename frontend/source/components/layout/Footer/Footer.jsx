import Inferno from 'inferno';
import Component from 'inferno-component';
import './Footer.scss';

// The main Saylua layout component.
export default class Footer extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <footer id="footer">
        <div className="sidebar-filler"></div>
        <div className="footer-content">
          <p>
            <a href="/online/">1 Online</a> &bull;
            <a href="#">Back to Top</a> &bull;
            <a href="/page/about/">About</a> &bull;
            <a href="/page/credits/">Credits</a> &bull;
            <a href="/page/terms/">Terms of Service</a> &bull;
            <a href="/page/rules/">Site Rules</a> &bull;
            <a href="/page/contact/">Contact Us</a> &bull;
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
            <i className="fa fa-clock-o" aria-hidden="true"></i>
            <span id="site-time"></span>
            &bull;
            <button className="link-button" name="theme_id" value="0">
              <i className="fa fa-fw fa-sun-o" aria-hidden="true"></i>
            </button>
            &bull;
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
