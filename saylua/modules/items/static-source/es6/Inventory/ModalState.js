import BaseModel from "Models/BaseModel";


export default class ModalState extends BaseModel {
  constructor(closed) {
    super();
    this.closed = closed;
    this.item = null;
  }

  close() {
    this.closed = true;
  }

  open() {
    this.closed = false;
  }

  setItem(image, name, category, description) {
    this.item = {
      'image': image,
      'name': name,
      'category': category,
      'description': description,
    }
  }
}
