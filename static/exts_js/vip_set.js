var form;

$('#vip').submit(function (e) {
    e.preventDefault();
    form = $('#vip').serialize();
    $.ajax({
        type: 'POST',
        url: location.pathname,
        dataType: 'json',
        data: form,
        success: function (data) {

            if(data.msg == 'new'){
                swal('新建成功','成功新建套餐','success');
                var append = $("<tr class="+ $('#name').val() +"><td>" + $('#name').val() +
                    "</td><td>"+ $('#attack_num').val() +
                    "</td><td>"+ $('#use_time').val() +
                    "</td><td>"+ $('#yuan').val() +
                    "</td><td><a href='"+ $('#pay_url').val() +
                    "'><i class='mdui-icon material-icons'>add_shopping_cart</i></a></td>"+
                    "<td><button class='del mdui-btn mdui-btn-raised mdui-ripple' id="+ $('#name').val() +
                    ">Delete</button></td>" +
                    "</tr>");
                $('#tbody').append(append);

            }

            if(data.msg == 'old'){
                swal('已重新修改','已经成功修改!','success');
                $('tbody .'+$('#name').val()).empty();
                var append = $("<tr class="+ $('#name').val() +"><td>" + $('#name').val() +
                    "</td><td>"+ $('#attack_num').val() +

                    "</td><td>"+ $('#use_time').val() +
                    "</td><td>"+ $('#yuan').val() +
                    "</td><td><a href='"+ $('#pay_url').val() +
                    "'><i class='mdui-icon material-icons'>add_shopping_cart</i></a></td>"+
                    "<td><button class='del mdui-btn mdui-btn-raised mdui-ripple' id="+ $('#name').val() +
                    ">Delete</button></td>" +
                    "</tr>");

                $('#tbody').append(append);
            }
            if(data.msg == '0'){
                swal('不要留空！','请认真填写!')
            }

            },
        error: function () {
            swal('错误!','请稍后重试','error');
        }
    });
});


$(document).on("click",'.del',function () {
    var id = $(this).attr('id');
    var del_vip = {name: id};
    $.ajax({
        type: 'POST',
        url: '/user/vip_del/',
        dataType: 'json',
        data: del_vip,
        success: function (data) {
            if(data.msg == 'del'){
                $('tbody .' + id).remove();
                swal('删除','删除成功','success');

            } else{
              swal('Error',data.msg,'error');
            }
        },
        error: function () {
            swal('Error','请稍后重试','error');
        }
    });
});


