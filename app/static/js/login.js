$(document).ready(function() {

  // flash an alert
  // remove previous alerts by default
  // set clean to false to keep old alerts
  function flash_alert(message, category, clean) {
    if (typeof(clean) === "undefined") clean = true;
    if(clean) {
      remove_alerts();
    }
    var htmlString = '<div class="alert alert-' + category + ' alert-dismissible" role="alert">'
    htmlString += '<button type="button" class="close" data-dismiss="alert" aria-label="Close">'
    htmlString += '<span aria-hidden="true">&times;</span></button>' + message + '</div>'
    $(htmlString).prependTo("#mainContent").hide().slideDown();
  }

  function remove_alerts() {
    $(".alert").slideUp("normal", function() {
      $(this).remove();
    });
  }

  function check_job_status(status_url,id) {
    $.getJSON(status_url, function(data) {
      console.log(data);
      switch (data.status) {
        case "unknown":
            flash_alert("Unknown job id", "danger");
            $("#submit").removeAttr("disabled");
            break;
        case "finished":
            flash_alert("😀😎🤩💯", "success");
            $("#submit").removeAttr("disabled");
            var dURL = "/download/"+ id;
            console.log(dURL);
            window.open (dURL,'_self',false)
            break;
        case "failed":
            flash_alert("Job failed: " + data.message, "danger");
            $("#submit").removeAttr("disabled");
            break;
        default:
          // queued/started/deferred
          setTimeout(function() {
            check_job_status(status_url,id);
          }, 500);
      }
    });
  }
  // submit form
  $("#submit").on('click', function() {

    $.ajax({
      url: $SCRIPT_ROOT + "/_runProgram",
      data: $("#taskForm").serialize(),
      method: "POST",
      dataType: "json",
      success: function(data, status, request) {
        $("#submit").attr("disabled", "disabled");
        flash_alert("Hacking into Mr. Grubagh's Computer ...", "info");
        var status_url = request.getResponseHeader('Location');
        console.log(status_url);
        console.log(request.getResponseHeader('id') );
        check_job_status(status_url, request.getResponseHeader('id'));
      },
      error: function(jqXHR, textStatus, errorThrown) {
        flash_alert("Failed to start " + task, "danger");
      }
    });
  });

});
