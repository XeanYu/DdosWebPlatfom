$(document).on('click','.submit',function () {
    var id = $(this).attr('id');
    var dict = {'id':id};
    $.ajax({
        type: 'POST',
        url: location.pathname,
        dataType: 'json',
        data: dict,
        success: function (data) {
            if(data.msg == 'look'){

                swal('成功','已处理!' + ' 浏览与:' + data.date,'success');
            }
            if (data.msg == 'e1'){
                swal('警告','无此留言');
            }
        },
        error: function () {
            swal('错误','请稍后重试！','error');
        }
    });
});