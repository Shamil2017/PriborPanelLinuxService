export const page = document.body;
export const imageElement = page.querySelector('.malfunctions__img');
export const description = page.querySelector('.malfunctions__description');
export const formElement = page.querySelector('.form');
export const lists = page.querySelectorAll('.malfunctions__sublist');
export const submitList = page.querySelector('.page__list');
export const addSignalButton = formElement.querySelector('.form__add-signal');
export const submitButton = formElement.querySelector('.form__submit');
export const menuList = formElement.querySelector('.malfunctions__list');
export const responceElement = formElement.querySelector('.malfunctions__responce');
export const menuItems = menuList.querySelectorAll('.malfunctions__item');
export const loaderElement = page.querySelector('.loader');
export var Colors;
(function (Colors) {
    Colors["Green"] = "green";
    Colors["Red"] = "red";
    Colors["Yellow"] = "yellow";
})(Colors || (Colors = {}));
