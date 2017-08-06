import Inferno from 'inferno';
import Saylua from './components/layout/Saylua';

import page from 'page';

import Newspaper from './components/modules/General/Newspaper/Newspaper';
import Page from './components/modules/General/StaticPage/StaticPage';

page('/', () => {
  Inferno.render(<Saylua title="Home">Hello world</Saylua>, document.getElementById('app'));
});

page('/news', () => {
  Inferno.render(<Newspaper />, document.getElementById('app'));
});

page('/page/:page', (data) => {
  Inferno.render(<Page pageName={ data.params.page } />, document.getElementById('app'));
});

page('*', () => {
  Inferno.render(<Saylua>Not Found</Saylua>, document.getElementById('app'));
});

page();
