// graphics -> Required by Core/init
// --------------------------------------
// App level and graphics related utility functions.

function getDataURI(url) {
  let image = new Image();
  image.src = url;

  return new Promise((resolve, reject) => {
    image.onload = () => {
      let canvas = document.createElement('canvas');

      canvas.width = image.naturalWidth;
      canvas.height = image.naturalHeight;
      canvas.getContext('2d').drawImage(image, 0, 0);

      let dataURI = canvas.toDataURL('image/png');
      resolve(dataURI);
    };
  });
}


export function resolveImage(itemSlug) {
  let [type, ...parts] = itemSlug.split('_');

  // Hardcoded for now, these should use a resolving API in the future.
  if (type == 'interface') {
    if (parts[0] == 'hp') {
      if (parts[1] == 'positive') {
        return `/static/img/dungeons/interface/hp_positive.png`;
      } else if (parts[1] == 'negative') {
        return `/static/img/dungeons/interface/hp_negative.png`;
      }
    } else if (parts[0] == 'tile') {
      if (itemSlug == 'interface_tile_hover_green') {
        return `/static/img/dungeons/interface/tileselect_green.png`;
      } else if (itemSlug == 'interface_tile_hover_red') {
        return `/static/img/dungeons/interface/tileselect_red.png`;
      }
    }
  }

  if (type == 'entity') {
    if (parts[0] == 'default') {
      if (parts[1] == 'player') {
        return `/static/img/velbird.png`;
      } else if (parts[1] == 'portal') {
        return `/static/img/dungeons/tiles/test/portal.png`;
      } else if (parts[1] == 'item') {
        return `/static/img/dungeons/item/${ parts.slice(-1) }.png`;
      } else if (parts[1] == 'enemy') {
        return `/static/img/dungeons/enemies/${ parts.slice(-1) }.png`;
      }
    }
  }

  if (type == 'tile') {
    if (parts[0] == 'fog') {
      return `/static/img/dungeons/tiles/test/null.png`;
    }

    return `/static/img/dungeons/tiles/test/${ parts.join('_') }.png`;
  }

  if (type == 'debug') {
    if (parts[0] == 'x') {
      return `/static/img/dungeons/debug/debug_x.png`;
    }
  }

  throw(`Couldn't resolve '${itemSlug}' to image.`);
}


export function getTexture(itemSlug) {
  // Initialize textures if necessary
  window.textures = window.textures || {};

  // Try returning an existing Texture first.
  if (window.textures[itemSlug] !== undefined) {
    return window.textures[itemSlug];
  }

  // Attempt to retrieve from localStorage
  if (typeof(Storage) !== 'undefined') {
    let result = localStorage.getItem("saylua_texture_" +  itemSlug);

    if (result !== null) {
      // Create a texture from the matching localStorage entry,
      // then add it to the library and return.
      window.textures[itemSlug] = PIXI.Texture.fromImage(result);
      return window.textures[itemSlug];
    }
  }

  // Our Texture has never been loaded.
  let imageURL = resolveImage(itemSlug);
  let texture = PIXI.Texture.fromImage(imageURL);

  if (texture === undefined) {
    throw(`Error locating texture: ${ itemSlug }`);
  }

  window.textures[itemSlug] = texture;

  // Try to store in localStorage for next time.
  if (typeof(Storage) !== 'undefined') {
    let promise = getDataURI(imageURL);
    promise.then((dataURI) => {
      localStorage.setItem("saylua_texture_" + itemSlug, dataURI);
    });
  }

  // Return image.
  return window.textures[itemSlug];
}
