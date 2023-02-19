const title = document.getElementById("title-post");
const date = document.getElementById("date-post");
const select = document.getElementById("level-post");
const content = document.getElementById("post-content");
const file = document.getElementById("input_post_by_file");
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

function sendData(e) {
  const data = {
    title: title.value,
    date: date.value,
    level: select.value,
    content: content.value,
  };

  url = window.location.href;

  const markdownFile = file.files[0];

  const formData = new FormData();
  formData.append("post_file", markdownFile);
  formData.append("post", data);

  const fetchOptions = {
    method: "POST",
    body: formData,
  };

  fetch(url, fetchOptions).then((response) => {
    if (response.ok) whatchAlert(data.title, dateCode);
    setTimeout(() => hiddenAlert(), 13000);
  });
}
