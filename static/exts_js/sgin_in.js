var form_info;

$('#user_info').submit(function(e){
  e.preventDefault();
  form_info = $('#user_info').serialize();

  $.ajax({
    type: 'POST',
    url: location.pathname,
    dataType:'json',
    data:form_info,
    success: function(data){
      // 判断是否登录成功，成功则跳转
      if(data.msg == 'login'){
        window.location.href = '/user/';
      }
      // 未登录成功，返回信息
      else{
        $('.sgin_pass').text(data.msg);
      }},

      error: function(){
        $('.sgin_pass').text('网络不佳～～ 请稍后重试.');
      }
    }); // ajax的后括号
});
