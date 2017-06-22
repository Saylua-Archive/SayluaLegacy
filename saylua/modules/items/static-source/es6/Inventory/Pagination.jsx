import Inferno from "inferno";
import Component from "inferno-component";

export default class Pagination extends Component {
  constructor(props) {
    super(props);
    this.state = {
      'currentPage': this.props.currentPage || 1,
      'pageBuffer': this.props.pageBuffer || 2,
      'pageCount': this.props.pageCount || 1,
      'onPageChange': this.props.onPageChange,
    };
  }

  setPage(number) {
    this.state.currentPage = number;
    this.state.onPageChange(number);
  }

  render() {
    let currentPage = this.state.currentPage;
    let pageCount = this.state.pageCount;
    let pageBuffer = this.state.pageBuffer;

    let prevButton = <span>&#8592; Prev</span>;
    if (currentPage > 1) {
      prevButton = (
        <span className="link" onClick={ this.setPage.bind(this, currentPage - 1) }>
          &#8592; Prev
        </span>
      );
    }

    let nextButton = <span>Next &#8594;</span>;
    if (currentPage < pageCount) {
      nextButton = (
        <span className="link" onClick={ this.setPage.bind(this, currentPage + 1) }>
          Next &#8594;
        </span>
      );
    }

    let startPageRange = currentPage - pageBuffer;
    let endPageRange = currentPage + pageBuffer;

    if (startPageRange < 1) {
      endPageRange = endPageRange - (startPageRange - 1);
      startPageRange = 1;
    }

    if (endPageRange > pageCount) {
      startPageRange = startPageRange - (endPageRange - pageCount);
      if (startPageRange < 1) {
        startPageRange = 1;
      }
      endPageRange = pageCount;
    }

    let startPages = [];
    let mainPages = [];
    let endPages = [];

    if (startPageRange > 1) {
      startPages.push(<span className="link" onClick={ this.setPage.bind(this, 1) }>1</span>);
      startPages.push(<span>...</span>);
    }

    for (let i = startPageRange; i <= endPageRange; i++) {
      if (i == currentPage) {
        mainPages.push(<span class="active">{ i }</span>);
      } else {
        mainPages.push(<span className="link" onClick={ this.setPage.bind(this, i) }>{ i }</span>);
      }
    }

    if (endPageRange < pageCount) {
      endPages.push(<span>...</span>);
      endPages.push(<span className="link" onClick={ this.setPage.bind(this, pageCount) }>{ pageCount }</span>);
    }
    return (
      <div className="pagination center">
        { prevButton }
        { startPages }
        { mainPages }
        { endPages }
        { nextButton }
      </div>
    );
  }
}
