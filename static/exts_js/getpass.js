$(document).ready(function(){
  $('#alert-box').hide();
});

$('#alert-box').click(function (){
  $('#alert-box').fadeToggle('slow');
});

var form_info;

$('#form').submit(function(e){
  e.preventDefault();
  form_info = $('#form').serialize();

  $.ajax({
    type:'POST',
    url:location.pathname,
    dataType:'json',
    data: form_info,
    success: function(data){
      // if change
      if(data.msg == 'change'){
        $('#alert-box').hide();
        $('#off').hide();
        window.location.href='/login/';
      }

      // else it
      else{
        $('#alert-box').show();
        $('.info').text(' ' + data.msg);
      }},

    error: function(xhr,){
      $('#alert-box').show();
      $('.info').text(' ' + '网络不佳～～ 请稍后重试!');}
  });

});
