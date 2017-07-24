import Inferno from 'inferno';
import Component from 'inferno-component';
import './UserLink.scss';

export default class UserLink extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let user = this.props.user;
    if (!user) {
      return;
    }
    return (
      <span>
        <a href={ url } className={ titleClass }>{ name }</a>
          <small>{ status }</small>
      </span>
    );
  }
}
