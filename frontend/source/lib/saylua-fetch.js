import 'whatwg-fetch';

var token = null;

export function slFetch(url, request) {
  token = getCsrfToken();

  if (request) {
    if (request.headers) {
      request.headers['X-CSRF-Token'] = token;
    } else {
      request.headers = {'X-CSRF-Token': token};
    }
  }

  return fetch(url, request);
}

export function getCsrfToken() {
  if (!token) {
    token = document.querySelector('meta[name="csrf-token"]').content;
  }
  return token;
}
