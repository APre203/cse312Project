document.getElementById("image-upload-form").addEventListener("submit", () => {
  //const formData = new FormData(this);
  fetchImageList();
});

function fetchImageList() {
  fetch("/images")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      const imageListDiv = document.getElementById("imageList");
      imageListDiv.innerHTML = "";

      data.forEach((image) => {
        const liElement = document.createElement("li");
        random_num = Math.round(Math.random() * 5);
        liElement.innerHTML = `Uploaded Photo ${random_num}`;
        liElement.addEventListener("click", function () {
          displayImage(image.filename);
        });
        imageListDiv.appendChild(liElement);
      });
    });
}
function displayImage(url) {
  const imageDisplayDiv = document.getElementById("imageDisplay");
  imageDisplayDiv.innerHTML = `<img src="${url}" alt="Clicked Image">`;
}
