import Inferno from "inferno";
import Component from "inferno-component";

export default class Pagination extends Component {
  constructor(props) {
    super(props);
  }

  setPage(number) {
    this.props.currentPage = number;
    this.props.onPageChange(number);
  }

  render() {
    let currentPage = this.props.currentPage || 1;
    let pageCount = this.props.pageCount || 1;
    let pageBuffer = this.props.pageBuffer || 2;

    let prevClass = "previous-link";
    let prevOnClick = null;
    if (currentPage > 1) {
      prevClass += " link";
      prevOnClick = this.setPage.bind(this, currentPage - 1);
    }
    let prevButton = (
      <span className={ prevClass } onClick={ prevOnClick }>
        &#8592; Prev
      </span>
    );

    let nextClass = "next-link";
    let nextOnClick = null;
    if (currentPage < pageCount) {
      nextClass += " link";
      nextOnClick = this.setPage.bind(this, currentPage + 1);
    }
    let nextButton = (
      <span className={ nextClass } onClick={ nextOnClick }>
        Next &#8594;
      </span>
    );

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
      <div className="pagination pagination-ajax">
        { prevButton }
        { startPages }
        { mainPages }
        { endPages }
        { nextButton }
      </div>
    );
  }
}
