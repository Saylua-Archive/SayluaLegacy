import Inferno from 'inferno';
import Saylua from './components/layout/Saylua';

import page from 'page';

page('/', () => {
  Inferno.render(<Saylua content="Hello world." />, document.getElementById('app'));
});

page('*', () => {
  Inferno.render(<Saylua content="Not Found." />, document.getElementById('app'));
});

page();
