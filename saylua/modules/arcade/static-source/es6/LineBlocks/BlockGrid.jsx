import Inferno from "inferno";
import Component from "inferno-component";

// Renders an instance of the game matrix.
export default class BlockGrid extends Component {
  constructor(props) {
    super(props);
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      "triggerUpdate": true
    });
  }

  getColor(value) {
  	switch(value) {
  		case 1: return "#FFF";
  		case 2: return "#0FF";
  		case 3: return "#F0F";
  		case 4: return "#FF0";
  		case 5: return "#0F0";
  		case 6: return "#00F";
  		case 7: return "#F00";
  		default: return "#000";
  	}
  }

  render() {
    let model = this.props.matrix;
    let getColor = this.getColor;
    return (
      <table className="grid-container">
        {model.rows().map(function(col) {
          return (
            <tr className="grid-row">{col.map(function(num) {
              return <td className="grid-square" style={{backgroundColor: getColor(num)}} />;
            })}</tr>
          );
        })}
      </table>
    );
  }
}
