import Inferno from "inferno";
import Component from "inferno-component";

export default class DungeonInfo extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentWillMount() {
    this.props.miniMap.bindComponent(this);
  }

  render() {
    return (
      <div className="dungeon-info-wrapper">
        <img className='testing-image' src="/static/img/habitats/flat-bambooforest.jpg"/>
        <div className='dungeon-mini-map'>{ this.props.miniMap.get() }</div>
        <p>
          This place is truly beautiful. You look around and revel in the beauty that surrounds you.
          You become one with the beauty. The beauty conquers all.
        </p>
        <p>
          You found a pile of rocks.
        </p>
      </div>
    );
  }
}
