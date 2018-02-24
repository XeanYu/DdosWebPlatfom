$(document).ready(function(){
  $('.text-warning').hide();
});

// 对用户输入的特效
$('#username').focus(function(){
  $('.alert_user').fadeIn('slow');
});
$('#username').blur(function(){
  $('.alert_user').fadeOut('slow');
});

// 对邮箱输入的特效
$('#email').focus(function(){
  $('.alert_email').fadeIn('slow');
});
$('#email').blur(function(){
  $('.alert_email').fadeOut('slow');
});

// 对密码输入的特效
$('#password').focus(function(){
  $('.alert_pass').fadeIn('slow');
});
$('#password').blur(function(){
  $('.alert_pass').fadeOut('slow');
});

// 对密码输入的特效
$('#code').focus(function(){
  $('.alert_code').fadeIn('slow');
});
$('#code').blur(function(){
  $('.alert_code').fadeOut('slow');
});


var form_info; // form_info's type are undefined
var form = $('#user_info');
form.submit(function(e){
  e.preventDefault();
  form_info = $('#user_info').serialize();
  $.ajax({
    type: 'POST',
    url: location.pathname,
    dataType: 'json',
    data: form_info,
    success: function(data){
      // 如果为True，则跳转到登录页面
      if(data.msg == 'redirect'){
        window.location.href ='/login/';
      }

      // 不为True，则返回信息
      else {
        $('#alert').text(data.msg);
      }

    },
    error: function(){
      $('#alert').text('网络不佳～～ 请稍后重试.');
    }
  });
});
