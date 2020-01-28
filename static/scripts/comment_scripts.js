
    var deleteCommentButton = $(".deleteCommentButton");
    var editCommentButtons = $(".editCommentButton");
    var editCommentSubmit = $(".editCommentSubmit");
    deleteCommentButton.click(function(event){
        let id = $(this).attr('id');
        $.ajax({
            url: 'commentdelete/',
            method: 'POST',
            data: {'comment_id': id},
            success: function(data){
                event.target.parentNode.parentNode.parentNode.remove();
                if (data["result"]){
                    $("#"+data["result"]).remove();
                    }
            },
            error: function(errorData){
                console.log("Error");
                console.log(errorData);
            }
        })
    })

    editCommentButtons.click(function() {
        let id = $(this).attr('id'); // $(this) refers to button that was clicked
        console.log(id);
        this.nextSibling.nextSibling.style.display = 'block';
        this.style.display = 'None';
        commentp =  $('#'+ "commentText"+id);
        commentText = commentp.text();
        let input = document.createElement("input");
        input.type = "text";
        input.id = "commentText"+id; // set the CSS class
        input.value = commentText;
        commentp.replaceWith(input);

    });
    editCommentSubmit.click(function(event){
        let id = $(this).attr('id');
        let submit = this;
        let comment = $("#" + "commentText" + id);
        var formData = comment.val();
        $.ajax({
            url: "commentedit/",
            method: 'POST',
            data: {
            'comment_id':id,
            'text': formData},
            success: function(data){
                if (data == 'Ok'){
                    commentText = comment.val();
                    let input = document.createElement("p");
                    input.id = "commentText"+id;
                    input.innerHTML = commentText;
                    comment.replaceWith(input);
                    submit.style.display = 'None';
                    submit.previousSibling.previousSibling.style.display = 'block';
                    }
            },
            error: function(errorData){
                console.log("Error");
                console.log(errorData);
            }
        })
    })
//    editCommentForm.submit(function(e){
//        e.preventDefault();
//        let id ="commentText" + 12;
//        var formData = $("#" + id).val();
//        $.post(
//        "{% url 'comment_edit_url'  slug=post.slug pk=comment.id %}",
//        {data: formData},
//        function(data){
//         if (data['status'] == 'Ok'){
//            console.log('Edited')
//         }})
//    })
