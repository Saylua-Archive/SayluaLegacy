import BaseModel from "Models/BaseModel";

import { slFetch } from "saylua-fetch";


export default class InventoryModel extends BaseModel {
  constructor(categoryId=0, currentPage=1) {
    super();

    this.categoryId = categoryId;
    this.currentPage = currentPage;
    this.items = [];
    this.index = -1;
    this.pageCount = 1;

    this.fetchData();
  }

  fetchData() {
    let model = this;
    slFetch('/api/inventory/' + this.categoryId + '/' + this.currentPage + '/', {
      credentials: 'include'
    }).then((response) => {
      if (response.ok) {
        return response.json();
      }
      console.error('Fetching inventory failed!');
    }).then((json) => {
      model.items = json.items;
      model.pageCount = json.pages;
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

  prevItem() {
    this.setIndex((this.index - 1 + this.items.length) % this.items.length);
  }

  nextItem() {
    this.setIndex((this.index + 1) % this.items.length);
  }

  setCategory(categoryId) {
    this.categoryId = categoryId;
    this.fetchData();
  }

  setCurrentPage(currentPage) {
    this.currentPage = currentPage;
    this.fetchData();
  }
}
