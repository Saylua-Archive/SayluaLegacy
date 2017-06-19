import BaseModel from "Models/BaseModel";

import { slFetch } from "saylua-fetch";


export default class InventoryModel extends BaseModel {
  constructor(category_id=0, current_page=1) {
    super();

    this.category_id = category_id;
    this.current_page = current_page;
    this.items = [];
    this.index = -1;

    this.fetchData();
  }

  fetchData() {
    let model = this;
    slFetch('/api/inventory/' + this.category_id + '/' + this.current_page + '/', {
      credentials: 'include'
    }).then((response) => {
      if (response.ok) {
        return response.json();
      }
      console.error('Fetching inventory failed!');
    }).then((json) => {
      model.items = json.items;
      model.pages = json.pages;
      model.triggerUpdate();
    });
  }

  getItem() {
    if (this.index < 0 || this.index >= this.items.length) return null;
    return this.items[this.index];
  }

  setIndex(index) {
    this.index = index;
    this.triggerUpdate();
  }

  setCategory(category_id) {
    this.category_id = category_id;
    this.fetchData();
  }

  setCurrentPage(current_page) {
    this.current_page = current_page;
    this.fetchData();
  }
}
