import Inferno from 'inferno';
import Saylua from './components/layout/Saylua';

import page from 'page';

import Newspaper from './components/modules/Newspaper/Newspaper';

page('/', () => {
  Inferno.render(<Saylua>Hello world</Saylua>, document.getElementById('app'));
});

page('/news', () => {
  Inferno.render(<Newspaper />, document.getElementById('app'));
});

page('*', () => {
  Inferno.render(<Saylua>Not Found</Saylua>, document.getElementById('app'));
});

page();
