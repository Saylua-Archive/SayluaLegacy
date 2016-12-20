import Reqwest from "reqwest";

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

function resolveImage(itemSlug) {
  let [type, ...parts] = itemSlug.split("_");

  // Hardcoded for now, these should use a resolving API in the future.
  if (type == "entity") {
    if (parts[0] == "player") {
      return `/static/img/velbird.png`;
    } else if (parts[0] == "portal") {
      return `/static/img/tiles/test/portal.png`;
    } else if (parts[0] == "item") {
      return `/static/img/item/${ parts.slice(-1) }.png`;
    } else if (parts[0] == "enemy") {
      return `/static/img/enemies/${ parts.slice(-1) }.png`;
    }
  } else if (type == "tile") {
    return `/static/img/tiles/test/${ parts.join("_") }.png`;
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
  if (typeof(Storage) !== "undefined") {
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
  if (typeof(Storage) !== "undefined") {
    let promise = getDataURI(imageURL);
    promise.then((dataURI) => {
      localStorage.setItem("saylua_texture_" + itemSlug, dataURI);
    });
  }

  // Return image.
  return window.textures[itemSlug];
}
