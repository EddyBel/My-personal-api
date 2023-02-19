const images_files_input = document.getElementById(
  "input_post_images_by_files"
);
const list_imgs = document.getElementById("list_files_imgs");

/** This function is executed every time it detects an event on the send file button. */
function onHandleAddImages() {
  // Gets the list of images from the input
  const images = images_files_input.files;
  // Clean the dom list before starting.
  list_imgs.innerHTML = "";

  // Scroll through all input images
  for (let i = 0; i < images.length; i++) {
    // Get the image
    const file = images[i];
    // Create the url to use in the images.
    const url = URL.createObjectURL(file);
    // Create item list
    const render = `<li class="list-group-item">
            <img
              src="${url}"
              class="img-preview"
            />${file.name}
          </li>`;
    // Add item in the dom
    list_imgs.innerHTML += render;
  }
}
