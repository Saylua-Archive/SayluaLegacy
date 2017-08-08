import Inferno from 'inferno';
import Component from 'inferno-component';
import './Newspaper.scss';

import Saylua from 'components/layout/Saylua';


export default class Newspaper extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Saylua title="The Sayluan Gazette">
        <h1 class="news-header">The Sayluan Gazette</h1>
        <div class="news-navigation">
          <a href="/news/">Headlines</a>{ ' / ' }
          <a href="/news/puzzle/">Daily Puzzle</a>
        </div>
        <div class="newspaper-body">
          <div class="newspaper-main">
          </div>
          <div class="newspaper-side">
          </div>
        </div>
      </Saylua>
    );
  }
}
