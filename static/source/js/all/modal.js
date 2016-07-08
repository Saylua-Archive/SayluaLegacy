(function (g) {
  g.Modal = function (modalSettings) {
    // A reference to the modal in the dom
    this.modal = null;
    this.overlay = null;
    this.closeButton = null;

    // Initialized to all of the defaults for this thing!
    this.settings = {
      className: "zoom",
      hasCloseButton: true,
      content: "",
      title: null,
      maxWidth: 800,
      minWidth: 200,
      hasOverlay: true,
      isFixed: true,
      linkSelector: null
    };

    var self = this;

    if (modalSettings && typeof modalSettings === "object") {
      for (var key in this.settings) {
        if (modalSettings.hasOwnProperty(key)) {
          this.settings[key] = modalSettings[key]
        }
      }
    }

    var content = this.settings.content;
    if (content && content.innerHTML) {
      content = content.innerHTML;
      removeElement(this.settings.content);
      this.settings.content = content;
    }

    if (this.settings.linkSelector !== null) {
      var links = document.querySelectorAll(this.settings.linkSelector);

      for (var i = 0; i < links.length; i++) {
        links[i].addEventListener("click", function (e) {
          e.preventDefault();
          self.open();
        });
      }
    }
  };

  Modal.prototype.open = function () {
    buildModal.call(this);
    initializeEvents.call(this);

    // For animations
    window.getComputedStyle(this.modal).height;

    this.modal.className += this.modal.offsetHeight > window.innerHeight ?
      " modal-active modal-anchored" : " modal-active";
    if (this.overlay) {
      this.overlay.className += " modal-active";
    }
  };

  Modal.prototype.close = function () {
    var self = this;

    this.modal.className = this.modal.className.replace(" modal-active", "");

    this.modal.addEventListener(transitionEnd(), function () {
      removeElement(self.modal);
    });

    if (this.overlay) {
      this.overlay.className = this.overlay.className.replace(" modal-active", "");

      this.overlay.addEventListener(transitionEnd(), function () {
        removeElement(self.overlay);
      });
    }
  }

  function buildModal () {
    var fragment = document.createDocumentFragment();
    this.modal = document.createElement("div");
    this.modal.className = "modal " + this.settings.className;
    this.modal.style.minWidth = this.settings.minWidth + "px";
    this.modal.style.maxWidth = this.settings.maxWidth + "px";

    if (this.settings.hasCloseButton === true) {
      this.closeButton = document.createElement("button");
      this.closeButton.className = "modal-close modal-close-button";
      this.closeButton.innerHTML = "×";
      this.modal.appendChild(this.closeButton);
    }

    if (this.settings.hasOverlay === true) {
      this.overlay = document.createElement("div");
      this.overlay.className = "modal-overlay " + this.settings.className;
      fragment.appendChild(this.overlay);
    }

    if (this.settings.title !== null) {
      var title = document.createElement("h2");
      title.className = "modal-title";
      title.innerHTML = this.settings.title;
      this.modal.appendChild(title);
    }

    var content = document.createElement("div");
    content.className = "modal-content";
    content.innerHTML = this.settings.content;
    this.modal.appendChild(content);

    fragment.appendChild(this.modal);

    document.body.appendChild(fragment);
  }

  function initializeEvents() {
    if (this.closeButton) {
      this.closeButton.addEventListener('click', this.close.bind(this));
    }

    if (this.overlay) {
      this.overlay.addEventListener('click', this.close.bind(this));
    }
  }

  function transitionEnd() {
    var el = document.createElement("div");
    if (el.style.WebkitTransition) return "webkitTransitionEnd";
    if (el.style.OTransition) return "oTransitionEnd";
    return 'transitionend';
  }

  function removeElement (obj) {
    if (obj.parentElement) {
      obj.parentElement.removeChild(obj);
    }
  }
}(window));
