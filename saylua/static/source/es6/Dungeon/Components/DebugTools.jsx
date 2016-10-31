import Inferno from "inferno";
import Component from "inferno-component";

export default class DebugTools extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div class="dungeon-debug-tools">
        <p>IT'S DEBUGGING TIME, BABY</p> <br />
        <button onClick={ this.props.regenerate }>Regenerate Dungeon</button>
        <button onClick={ this.props.reveal }>Reveal Dungeon</button>
      </div>
    );
  }
}
