var form;

$("#placard").submit(function (e) {
    e.preventDefault();
    form = $("#placard").serialize();

    $.ajax({
        type: 'POST',
        url: location.pathname,
        dataType: 'json',
        data:form,
        success: function (data) {
            if(data.msg == 'add') {

                var append = ("<tr class="+ data.title
                            + "><td>" + data.title + "</td>"
                            + "<td>"+ data.context +"</td>"
                            + "<td>"+ data.author +"</td>"
                            + "<td>"+ data.date +"</td>"
                            + "<td><button class='delplacard del mdui-btn mdui-btn-raised mdui-ripple' id='"+ data.title +"' >Delete</button></td>"
                            + "</tr>");
                $('#tbody').append(append);
                swal('成功', '成功新建公告', 'success');
            }

            if (data.msg == 'e1'){
                swal('标识','已有此公告');
            }},

        error: function () {
            swal('Error','请稍后重试','error');
        }
    });
});


$(document).on('click','.delplacard',function () {
    var id = $(this).attr('id');
    var dict = {'title':id};
    $.ajax({
        type: 'POST',
        url: '/user/del_placard/',
        dataType: 'json',
        data: dict,
        success: function (data) {
          if(data.msg == 'del'){
              $('tbody .' + id).remove();
              swal('成功','成功删除公告','success');
          }
          if(data.msg == '0'){
              swal('标识','请刷新页面后重试');
          }

        },

        error: function () {
            swal('Error','请重新登录','error');
        }
    });
});