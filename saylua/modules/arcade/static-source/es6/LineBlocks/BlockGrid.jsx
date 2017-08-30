import Inferno from "inferno";
import Component from "inferno-component";

// Renders an instance of the game matrix.
export default class BlockGrid extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let model = this.props.matrix;
    let rows = model.rows().map(function(col) {
      return (
        <tr key={ col }>{col.map(function(num) {
          return <td key={ num } className={"grid-square-" + num} />;
        })}</tr>
      );
    });
    return (
      <table className="grid-table">
        { rows }
      </table>
    );
  }
}
