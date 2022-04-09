$(document).ready(function () {
  $('#showDiv1').click(function () {
    $('#div1').stop(true, true).slideDown();
    $('#div2').slideUp();
    $('#div3').slideUp();
  });
  $('#showDiv2').click(function () {
    $('#div2').stop(true, true).slideDown();
    $('#div1').slideUp();
    $('#div3').slideUp();
  });
    $('#showDiv3').click(function () {
    $('#div3').stop(true, true).slideDown();
    $('#div1').slideUp();
    $('#div2').slideUp();
  });
});
