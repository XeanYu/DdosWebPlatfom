var form;
$('#cards').submit(function (e) {
    e.preventDefault();
    form = $('#cards').serialize();

    $.ajax({
        type: 'POST',
        url: location.pathname,
        dataType: 'json',
        data: form,
        beforeSend: function () {
            
        },
        success: function (data) {
            if(data.msg == 'make'){
                location.reload();
                swal('成功',"成功创建！",'success');
            }
            if(data.msg == 'e1'){
                swal('请输入完整');
            }
        },
        error: function () {
            swal('Error','error -.-','error')
        }
    });
});