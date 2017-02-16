var path = require('path');
var glob = require('glob');
var webpack = require('webpack');

var tempConfig = require('./temporary.config.js');
var pkgGlob = "./" + tempConfig.paths.es6 + "/**/Main.js*";
var packages = glob.sync(pkgGlob);


// Create hashmap of entries from globbed paths
var formattedEntries = {};

for (var pkg of packages) {
  // First, we grab the name of the package
  var pkgName = pkg
    .split("/")
    .splice(-2)[0];

  // Then, we separate the module path, name from the absolute path.
  var modulePath = pkg.split("/static-source/")[0];
  var moduleName = modulePath.split("/").splice(-1)[0];

  // Filter deprecated / hidden packages
  if (pkgName.indexOf("_") == -1) {
    var entryName = moduleName + "." + pkgName;
    formattedEntries[entryName] = pkg;
  }
}


// Chef's Special Sauce
function DynamicPathPlugin(options) {
  this.options = options;

  this.apply = (compiler) => {
    compiler.plugin("compilation", (compilation) => {
      const mainTemplate = compilation.mainTemplate;

      mainTemplate.plugin("asset-path", (_path, data) => {
        // Match [name:sep]
        const REGEXP = new RegExp("\\[name:(\\d+)\\]", "ig");

        var match = _path.match(REGEXP);
        if (match !== null) {
          var newPath = path.normalize(_path);

          // Loop through each occurrence of [name:sep] in a given
          // output path and replace accordingly.
          for (var matchInstance of match) {
            // Determine our name index
            var nameIndex = matchInstance.replace(/\[\]/g, "").split(":")[1];
            nameIndex = Math.max(0, parseInt(nameIndex) - 1);

            // Grab our name values
            var entryName = data.chunk.name.split(".");
            var isRootPackage = (entryName[0] == this.options.root);

            // Replace and return
            if (isRootPackage && nameIndex == 0) {
              newPath = newPath.replace(matchInstance, this.options.root);
            } else {
              if (!isRootPackage && nameIndex == 0) {
                var pathAddendum = path.join(this.options.root, "modules", entryName[nameIndex]);
                newPath = newPath.replace(matchInstance, pathAddendum);
              } else {
                var pathAddendum = entryName[nameIndex];
                newPath = newPath.replace(matchInstance, pathAddendum);
              }
            }
          }

          return newPath;
        }

        return _path;
      });
    });
  };
}


// Default Webpack Config
const config = {
  "entry": formattedEntries,
  "module": {
    "rules": [
      {
        "test": /\.(js|jsx)$/,
        "use": 'babel-loader'
      }
    ]
  },
  "output": {
    "path": path.resolve(__dirname),
    "filename": "./[name:1]/static/js/[name:2].min.js"
  },
  "plugins": [
    new DynamicPathPlugin({ "root": "saylua" }),
    new webpack.ProvidePlugin({
      'Promise': 'es6-promise'
    })
  ],
  "resolve": {
    "extensions": [".js", ".min.js", ".jsx"],
    "modules": ["./saylua/static-source/lib", "./node_modules"],
  }
};


module.exports = config;
