const paths = {
  es6: 'saylua/**/static-source/es6',
  sass: 'saylua/**/static-source/scss'
};

const dests = {
  scripts: 'static/js',           // Relative to script location
  sass: 'saylua/static/css/'      // All sass styles compile to style.min.css at the application root.
};

module.exports = {
  'dests': dests,
  'paths': paths
};
