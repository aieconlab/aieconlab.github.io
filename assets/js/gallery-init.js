window.addEventListener('load', function () {
  if (document.querySelector('.glightbox')) {
    GLightbox();
  }

  if (document.querySelector('.popupable')) {
    GLightbox({ selector: '.popupable' });
  }

  var galleryItems = document.querySelectorAll('.gallery .gallery-item');
  if (!galleryItems.length) {
    return;
  }

  var justifyScale = screen.height * 0.25;
  galleryItems.forEach(function (item) {
    var image = item.querySelector('img');
    if (!image || !image.height) {
      return;
    }
    var ratio = image.width / image.height;
    item.style.width = justifyScale * ratio + 'px';
    item.style.flexGrow = ratio;
  });
});
