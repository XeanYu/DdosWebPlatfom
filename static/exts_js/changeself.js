var selfform;

$('#self').submit(function (e) {
    e.preventDefault();
    selfform = $('#self').serialize();

    $.ajax({
        type: 'POST',
        url:location.pathname,
        dataType: 'json',
        data: selfform,
        success:function (data) {
            if(data.msg == 'change'){swal("成功", "修改成功","success");}

            else{swal("提示!", data.msg);}
            },
        error: function () {
            swal('错误','快请稍后重试','error');
        }
    });

});