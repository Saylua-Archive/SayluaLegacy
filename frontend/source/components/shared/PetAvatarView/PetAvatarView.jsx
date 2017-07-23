import Inferno from 'inferno';
import Component from 'inferno-component';
import './PetAvatarView.scss';

export default class PetAvatarView extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div class="pet-avatar-view">
        <div class="avatar-view">
          <a href="">
            <img src="" alt="human avatar" title="'s Avatar'" aria-label="'s Avatar'" />
          </a>
        </div>
        <a href="" class="active-pet-view">
          <img src="" class="active-pet-image" alt="active companion" title="" aria-label="" />
        </a>
      </div>
    );
  }
}
