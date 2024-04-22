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
        liElement.innerHTML = `Uploaded Photo ${image.filename.split("/")[1]}`;
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
