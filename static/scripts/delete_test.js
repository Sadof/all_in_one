$('.delete_test_button').click(function(){
    let question = confirm("Are u sure");
    if (question){
        let test_id = $(this).data('id');
        let url = $(this).data('url');
        let self = $(this);
        $.ajax({
            type: "POST",
            url: url,
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            data: JSON.stringify(test_id),
            success: function(data){
                console.log(data, self);
                self.parent().parent().remove();
            }
        });
    }
})