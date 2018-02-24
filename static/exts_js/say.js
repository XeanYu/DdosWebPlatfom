var say;
$('#say').submit(function (e) {
    e.preventDefault();
    say = $('#say').serialize();

    $.ajax({
        type: 'POST',
        url: location.pathname,
        dataType: 'json',
        data: say,
        success: function (data) {
            if(data.msg == 'addsay'){
                swal('留言','留言成功,请刷新!','success');
            }
            if(data.msg == 'e1'){
                swal('警示','不可以留空!');
            }
        },
        error: function () {
            swal('错误','请稍后重试!','error');
        }

    });
});

$(document).on('click','.submit',function () {
    var id = $(this).attr('id');
    var del = {'id':id};

    $.ajax({
        type: 'POST',
        url: '/user/say_del/',
        dataType: 'json',
        data: del,
        success: function (data) {
            if(data.msg == 'saydel'){
                $('#'+id).remove();
                swal('成功','删除成功！','success');
            }
            if(data.msg == 'e1'){
                swal('警示','不可以有空的表单!');
            }
            if(data.msg == 'e2'){
                swal('警示','没有此留言!');
            }
        },
        error: function () {
            swal('错误','请刷新后重试！','error');
        }
    });


});