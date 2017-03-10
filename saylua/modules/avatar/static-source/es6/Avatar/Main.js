import {arrayRemove} from 'Utils';
import 'whatwg-fetch';

var haImage = document.getElementById('preview-ha');
var clothingContainer = document.getElementById('clothing');
var wardrobeEndpoint = '/api/ha/wardrobe/';
var haEndpoint = '/api/ha/m/';

var wearing = [];
fetch(wardrobeEndpoint, {
  'credentials': 'include'
}).then((response) => {
  if (response.ok) {
    return response.json();
  }
}).then((clothing) => {
  for (let i = 1; i < clothing.length; i++) {
    let el = document.createElement('div');
    let img = document.createElement('img');
    img.src = '/static/img/ha/' + clothing[i];
    img.style.height = '100px';
    el.style.cursor = 'pointer';
    el.style.float = 'left';
    el.setAttribute('data-item', i);
    el.onclick = wear;
    el.appendChild(img);
    el.innerHTML += clothing[i];
    clothingContainer.appendChild(el);
  }
});

function wear() {
  var item = this.getAttribute('data-item');
  var alreadyWearing = arrayRemove(wearing, item);
  if (!alreadyWearing) {
    wearing.push(item);
  }

  var img_url = haEndpoint + wearing.join(',');
  haImage.src = img_url;
  document.getElementById('ha-image-url').value = img_url;
}
