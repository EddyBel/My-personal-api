const inputTag = document.getElementById("input-tag-name");
const buttonAddTag = document.getElementById("button-add-tag");
const buttonRemoveTag = document.getElementById("button-remove-tag");
const list = document.getElementById("list-tags");

/** Container of all labels */
let tags = [];

/** This function updates the tags in the dom to list them correctly. */
const updateDomList = () => {
  list.innerHTML = "";
  tags.map(
    (tag) => (list.innerHTML += ` <li class="list-group-item">${tag}</li>`)
  );
};

/** When the add button is clicked according to the value of the input to the list of labels. */
buttonAddTag.addEventListener("click", () => {
  const value = inputTag.value.toUpperCase();
  tags.push(value);
  updateDomList();
});

/** When the button is clicked, all tags that match the value of the input are searched for and deleted. */
buttonRemoveTag.addEventListener("click", () => {
  const value = inputTag.value.toUpperCase();
  const newTags = [];
  tags.map((tag) =>
    tag.toUpperCase() != value ? newTags.push(tag.toUpperCase()) : ""
  );
  tags = newTags;
  updateDomList();
});
