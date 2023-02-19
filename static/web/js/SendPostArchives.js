const inputPost = document.getElementById("input_post_by_file");
const inputImages = document.getElementById("input_post_images_by_files");
const buttonSubmitFilesPost = document.getElementById("submit-files-of-post");
const alert = document.getElementById("alert");
const textAlert = document.getElementById("text-alert");
const dateAlert = document.getElementById("alert-date");

const dateCode = new Date();

const whatchAlert = (title, date) => {
  alert.style.transform = "translateY(0%)";
  textAlert.innerHTML = `The post "${title}" was sent correctly`;
  dateAlert.innerHTML = `${date.getDate()}/${
    date.getMonth() + 1
  }/${date.getFullYear()}`;
};

const hiddenAlert = () => (alert.style.transform = "translateY(-150%)");

buttonSubmitFilesPost.addEventListener("click", () => {
  /** File post */
  let post_file = inputPost.files[0];
  /** Images post */
  let images = inputImages.files;
  let images_list = [];

  let formData = new FormData();
  formData.append("type", "file");
  formData.append("post", post_file);

  for (let i = 0; i < images.length; i++) formData.append("assets", images[i]);

  url = window.location.href;

  fetch(url, {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      whatchAlert(post_file.name, dateCode);
      setTimeout(() => hiddenAlert(), 7000);
    })
    .catch((error) => {
      alert.style.transform = "translateY(0%)";
      textAlert.innerHTML = `An error occurred while sending the "${post_file.name}"`;
      dateAlert.innerHTML = `${date.getDate()}/${
        date.getMonth() + 1
      }/${date.getFullYear()}`;
      setTimeout(() => hiddenAlert(), 7000);
    });
});
