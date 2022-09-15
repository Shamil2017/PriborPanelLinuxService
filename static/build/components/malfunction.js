class Malfunction {
  constructor(templateSelector, src, description) {
    this.template = templateSelector;
    this.src = src;
    this.description = description;
  }
  getElementFromTemplate() {
    return document.body.querySelector(this.template).content.cloneNode(true);
  }
  getView() {
    const element = this.getElementFromTemplate().children[0];
    const imageElement = element.children[0];
    imageElement.src = this.src;
    imageElement.alt = this.description;
    const descriptionElement = imageElement.nextElementSibling;
    descriptionElement.textContent = this.description;
    return element;
  }
}
export default Malfunction;
