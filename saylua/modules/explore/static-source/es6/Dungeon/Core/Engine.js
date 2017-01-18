// Currently a placeholder, future as of yet undetermined.

export default class Engine {
  constructor(store) {
    // Store store
    this.store = store.getState();

    // Store store store store.
    // This will be triggered any time the store state changes.
    this.unsubscribe = store.subscribe(() => {
      this.store = store.getState();
    });

  }
}
