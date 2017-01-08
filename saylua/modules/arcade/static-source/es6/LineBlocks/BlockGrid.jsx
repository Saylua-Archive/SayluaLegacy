import Inferno from "inferno";
import Component from "inferno-component";

// Renders an instance of the game matrix.
export default class BlockGrid extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let model = this.props.matrix;
    let getColor = this.getColor;
    let rows = model.rows().map(function(col) {
      return (
        <tr>{col.map(function(num) {
          return <td className={"grid-square-" + num} />;
        })}</tr>
      );
    });
    return (
      <table className="grid-container">
        { rows }
      </table>
    );
  }
}
