import Reqwest from "reqwest";

function getDataURI(url, callback) {
  var image = new Image();

  image.onload = () => {
    var canvas = document.createElement('canvas');
    canvas.width = this.naturalWidth;
    canvas.height = this.naturalHeight;

    canvas.getContext('2d').drawImage(this, 0, 0);
    callback(canvas.toDataURL('image/png'));
  };

  image.src = url;
}

function resolveImage(itemSlug) {
  let [type, ...parts] = itemSlug.split("_");

  // Hardcoded for now, these should use a resolving API in the future.
  if (type == "player") {
    return "/static/img/loxi.png";
  } else if (type == "entity") {
    if (parts[0] == "item") {
      return "/static/img/item/" + parts.slice(-1) + ".png";
    } else if (parts[0] == "enemy") {
      return "/static/img/enemies/" + parts.slice(-1) + ".png";
    }
  } else if (type == "tile") {
    return "/static/img/tiles/test/" + parts.join("_");
  }
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
    let result = localStorage.getItem("saylua_item_" +  itemSlug);

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
  window.textures[itemSlug] = texture;

  // Try to store in localStorage for next time.
  if (typeof(Storage) !== "undefined") {
    let dataURI = getDataURI(imageURL);
    localStorage.setItem("saylua_item_" + itemSlug, dataURI);
  }

  // Return image.
  return window.textures[itemSlug];
}

