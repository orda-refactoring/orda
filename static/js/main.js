$(document).ready(function() {
  $(".owl-carousel").owlCarousel({
    // OwlCarousel 옵션 설정
    items: 4, // 한 번에 표시할 아이템 수
    loop: false, // 무한 루프 여부
    margin: 0, // 아이템 간의 간격
    dots: true, // 도트 표시 여부
    animateIn: 'fadeIn',
    autoplay: true,
    rewind: true,
    autoplayTimeout: 4500,
    smartSpeed: 500,
    responsive: {
      // 반응형 옵션 설정
      0: {
        items: 1 // 0px 이상일 때, 1개의 아이템 표시
      },
      450: {
        items: 2
      },
      760: {
        items: 3
      },
      1280: {
        items: 4
      },
    }
  });
});